import traceback
import streamlit as st
import time
import requests
import re
from io import BytesIO
import traceback

def main():
    """
    Main function to create the Streamlit file upload UI.
    """
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
                            "http://localhost:8000/generate-ppt",
                            data={"want_ppt": str(want_ppt)},
                            files={"file":(uploaded_file.name, uploaded_file.getvalue(), "application/pdf")}
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
                    try:
                        response = requests.post(
                            "http://localhost:8000/get-podcast",
                            
                        )

                    except Exception as e:
                        st.error(f"An error occurred while processing the podcast audio: {e}")


if __name__ == "__main__":
    main()
