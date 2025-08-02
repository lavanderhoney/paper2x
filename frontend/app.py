import traceback
import streamlit as st
import time
import requests
import re
import traceback
from io import BytesIO
from appwrite.client import Client
from appwrite.services.account import Account

backend_url = st.secrets["backend"]["url"]  # URL of the backend service (local or deployed)
client = Client()
client.set_endpoint(st.secrets["auth"]["endpoint"])  # Appwrite endpoint
client.set_project(st.secrets["auth"]["PROJECT_ID"])  # Appwrite project ID
client.set_key(st.secrets["auth"]["API_KEY"])  # Appwrite API key

account = Account(client) # to allow new users to register, create session, etc.

#TO-DO: simplify this code with callbacks
def login_ui():
    st.title("Login")
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        try:
            session = account.create_email_password_session(email=email, password=password)
            st.session_state["session"] = session["$id"]
            print("st.user after login: ")
            st.write(st.user)
            st.session_state['logged_in'] = True
            st.success("Login successful!")
            st.rerun()  # Rerun to update the UI after login
        except Exception as e:
            st.error(f"Login failed: {e}")

def register_ui():
    st.title("Register")
    user_name = st.text_input("Username") 
    email = st.text_input("Email")
    password = st.text_input("Password", type="password")
    
    if st.button("Register"):
        try:
            user = account.create(
                user_id="unique()",
                email=email,
                password=password,
                name=user_name,
            )
            st.success("Registration successful! Please proceed to login.")
        except Exception as e:
            st.error(f"Registration failed: {e}")

def main():
    """
    Main function to create the Streamlit file upload UI.
    """ 
    # print(st.user.is_logged_in)
    if 'logged_in' not in st.session_state:
        st.session_state['logged_in'] = False
    
    if not st.session_state['logged_in']:
        st.title("Welcome to paper-2x !")
        option = st.radio("Choose an option", ["Login", "Register"])
        if option == "Login":
            login_ui()
        else:
            register_ui()
        return  # Don't show rest of the app unless logged in
    
    if st.button("Logout"):
        st.session_state['logged_in'] = False
        st.session_state['session'] = None
        st.rerun()
    st.title("PDF File Upload and Preview")

    # File uploader widget, limit to a single PDF
    uploaded_file = st.file_uploader(
        "Upload a PDF file",
        type=["pdf"],
        help="Upload a single PDF file.",
        label_visibility="visible"
    )

    if uploaded_file is not None:
        st.subheader("Uploaded File:")
        file_name = uploaded_file.name
        file_size = uploaded_file.size  # in bytes
        file_type = uploaded_file.type
        st.write(f"**Name:** {file_name}, **Size:** {file_size} bytes, **Type:** {file_type}")

        # Simulate upload progress
        st.write("Uploading...")

        st.success(f"File '{file_name}' uploaded successfully!")

        # Display PDF preview
        st.subheader("PDF Preview")
        try:
            file_bytes = uploaded_file.read()
            # Use an iframe to display the PDF within the Streamlit app.
            # Convert the bytes to a base64 encoded string.  Streamlit doesn't directly support displaying bytes in an iframe.  This approach
            # avoids saving the PDF to a temporary file.
            import base64
            pdf_base64 = base64.b64encode(file_bytes).decode('utf-8')
            pdf_display = f'<iframe src="data:application/pdf;base64,{pdf_base64}" width="100%" height="500" type="application/pdf"></iframe>'
            st.markdown(pdf_display, unsafe_allow_html=True)
        except Exception as e:
            st.error(f"Error displaying PDF: {e}")
            
        st.empty().write("")
        st.markdown("<div style='margin-top: 20px;'></div>", unsafe_allow_html=True)
        
        # Add buttons after successful upload
        col1, col2, col3, col4 = st.columns([1,1,1,1])  # Create three columns for the buttons
        want_ppt: bool = True
        clicked: bool = False
        with col2:
            if st.button("Convert to PPT"):
                want_ppt = True
                clicked = True
        with col3:
            if st.button("Get Podcast Audio"):
                want_ppt = False
                clicked = True
        
        # Send the file to the backend
        if clicked:
            st.write("Sending request...")
            with st.spinner("Processing the PDF..."):
                time.sleep(2)
                if want_ppt:
                    try:
                        response = requests.post(
                            f"{backend_url}/generate",
                            files={
                                "file": (uploaded_file.name, uploaded_file.getvalue(), "application/pdf"),
                                "want_ppt": (None, str(want_ppt)),  # Send as form data
                            },
                        )
                        if response.status_code == 200:
                            # --- Handle the file download ---
                            # The response is now a file, not JSON
                            if "application/vnd.openxmlformats-officedocument.presentationml.presentation" in response.headers.get("Content-Type", ""):
                                # Extract filename from Content-Disposition header, or use a default
                                content_disposition = response.headers.get("Content-Disposition")
                                if content_disposition:
                                    # Example: attachment; filename="generated_presentation.pptx"
                                    filename_match = re.search(r'filename="([^"]+)"', content_disposition)
                                    if filename_match:
                                        download_filename = filename_match.group(1)
                                    else:
                                        download_filename = "generated_presentation.pptx" # Default if not found
                                else:
                                    download_filename = "generated_presentation.pptx" # Default if no header

                                st.download_button(
                                    label="Download Generated PPT",
                                    data=response.content, # The actual file bytes
                                    file_name=download_filename,
                                    mime="application/vnd.openxmlformats-officedocument.presentationml.presentation"
                                )
                            else:
                                # Fallback if the response is not a PPT file (e.g., if you return JSON for podcast audio)
                                try:
                                    st.write(response.json())
                                except ValueError: # Not JSON
                                    st.write(f"Unexpected response content: {response.text}")
                        else:
                            print("--- ERROR STACK TRACE ---")
                            traceback.print_exc() # This prints the traceback to stderr (your console)
                            print("-------------------------")
                            st.error(f"Failed to send PDF: {response.status_code} - {response.text}")
                    except Exception as e:
                       st.error(f"An error occurred: {e}")
                else:
                    print(f"want_ppt: {want_ppt} {type(want_ppt)}")
                    try:
                        response = requests.post(
                            f"{backend_url}/generate",
                            files={
                                "file":(uploaded_file.name, uploaded_file.getvalue(), "application/pdf"),
                                "want_ppt": (None, str(want_ppt)),  # Send as form data
                            },
                        )
                        if response.status_code == 200:
                            # --- Handle the file download ---
                            st.audio(response.content, format="audio/mpeg") # MIME type for MP3
                            # The response is now a file, not JSON
                            if "audio/mpeg" in response.headers.get("Content-Type", ""):
                                download_filename = "generated_podcast.mp3"
                                st.download_button(
                                    label="Download Podcast Audio",
                                    data=response.content,  # The actual file bytes
                                    file_name=download_filename,
                                    mime="audio/mpeg"
                                )
                            else:
                                try:
                                    st.write(response.json())
                                except ValueError: # Not JSON
                                    st.write(f"Unexpected response content: {response.text}")

                    except Exception as e:
                        st.error(f"An error occurred while processing the podcast audio: {e}")


if __name__ == "__main__":
    main()
