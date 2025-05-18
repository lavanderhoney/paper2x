import streamlit as st
import time
from io import BytesIO

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
            # Read the file
            file_bytes = uploaded_file.read()
        

            # Use an iframe to display the PDF within the Streamlit app.
            # Convert the bytes to a base64 encoded string.  Streamlit doesn't
            # directly support displaying bytes in an iframe.  This approach
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
        with col2:
            st.button("Convert to PPT")

        with col3:
            st.button("Get Podcast Audio")

if __name__ == "__main__":
    main()
