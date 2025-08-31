import streamlit as st
from bs4 import BeautifulSoup

st.set_page_config(
    page_title="HTML Image Replacer",
    page_icon="🖼️"
)

# --- App Description and Text Area ---
st.title("🖼️ HTML Image Replacer")
st.markdown("""
This app helps you find and replace image URLs in an HTML file.
Paste your HTML text below, and you can replace the images with new URLs.
""")

with st.expander("Paste your HTML content here"):
    html_content = st.text_area(
        "Paste HTML text",
        height=300,
        placeholder="<!DOCTYPE html><html><body><img src='...' alt='...'</body></html>",
        label_visibility="collapsed"
    )

if html_content:
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
        st.info(f"Found {len(images)} images. Replace the URLs below.")

        with st.form("image_replacement_form"):
            updates = []
            for i, img in enumerate(images):
                current_src = img.get('src')
                current_width = img.get('width')
                current_height = img.get('height')
                
                col1, col2 = st.columns([1, 3])
                with col1:
                    if current_src:
                        st.image(current_src, caption=f"Original Image {i+1}", width=100)
                    else:
                        st.text(f"Image {i+1}")
                        st.info("No source URL found.")

                with col2:
                    st.text(f"Current URL:")
                    new_src = st.text_input(f"New URL for Image {i+1}", value=current_src, key=f"url_{i}")
                    
                    st.text(f"Width:")
                    new_width = st.text_input(f"New Width for Image {i+1}", value=current_width or "", key=f"width_{i}")
                    
                    st.text(f"Height:")
                    new_height = st.text_input(f"New Height for Image {i+1}", value=current_height or "", key=f"height_{i}")
                    
                    updates.append({'src': new_src, 'width': new_width, 'height': new_height})

            submitted = st.form_submit_button("Replace Images & Generate New HTML")
            
            if submitted:
                st.markdown("---")
                st.header("3. Copy Your Updated HTML Text")
                
                for i, img in enumerate(images):
                    # Update src
                    if updates[i]['src'] and updates[i]['src'] != img.get('src'):
                        img['src'] = updates[i]['src']
                    
                    # Update width
                    if updates[i]['width']:
                        img['width'] = updates[i]['width']
                    elif 'width' in img.attrs:
                        del img['width']
                    
                    # Update height
                    if updates[i]['height']:
                        img['height'] = updates[i]['height']
                    elif 'height' in img.attrs:
                        del img['height']
                
                modified_html = soup.prettify()

                st.code(modified_html, language='html')
                st.success("Your updated HTML is ready to be copied and used.")

else:
    st.info("Please paste HTML content to get started.")
