import streamlit as st
import io
from bs4 import BeautifulSoup
import base64

st.set_page_config(
    page_title="HTML Image Replacer",
    page_icon="🖼️"
)

# --- App Description and File Uploader ---
st.title("🖼️ HTML Image Replacer")
st.markdown("""
This app helps you find and replace image URLs in an HTML file.
Upload your HTML file, see all the images, and replace them with new URLs.
""")

uploaded_file = st.file_uploader("Upload an HTML file", type="html")

if uploaded_file:
    # Read the content of the uploaded file
    file_content = uploaded_file.read()
    html_content = file_content.decode("utf-8")
    
    soup = BeautifulSoup(html_content, 'html.parser')
    images = soup.find_all('img')
    
    st.markdown("---")
    
    # --- Live HTML Preview ---
    st.header("1. Live Preview of Your HTML File")
    with st.expander("Expand to view rendered HTML"):
        st.components.v1.html(html_content, height=600, scrolling=True)

    st.markdown("---")
    
    # --- Image Replacement Form ---
    st.header("2. Replace Images")
    
    if not images:
        st.warning("No image tags found in the HTML file.")
    else:
        st.info("Found {} images. Replace the URLs below.".format(len(images)))

        # Create a form to handle all inputs at once
        with st.form("image_replacement_form"):
            new_urls = []
            for i, img in enumerate(images):
                current_src = img.get('src')
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if current_src:
                        st.image(current_src, caption=f"Original Image {i+1}", width=100)
                    else:
                        st.text(f"Image {i+1}")
                        st.info("No source URL found.")

                with col2:
                    st.text(f"Current URL:")
                    new_url = st.text_input(f"New URL for Image {i+1}", value=current_src, key=f"url_{i}")
                    new_urls.append(new_url)

            submitted = st.form_submit_button("Replace Images & Generate New HTML")
            
            if submitted:
                st.markdown("---")
                st.header("3. Download Your Updated HTML File")
                
                # Update the src attributes in the BeautifulSoup object
                for i, img in enumerate(images):
                    if new_urls[i] and new_urls[i] != img.get('src'):
                        img['src'] = new_urls[i]
                
                # Get the modified HTML content
                modified_html = soup.prettify()

                # Create a download button for the new HTML file
                st.download_button(
                    label="Download Updated HTML",
                    data=modified_html,
                    file_name=uploaded_file.name,
                    mime="text/html"
                )
                st.success("Your file is ready for download! The changes have been applied.")

else:
    st.info("Please upload an HTML file to get started.")
