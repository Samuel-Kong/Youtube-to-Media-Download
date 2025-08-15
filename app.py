import streamlit as st
from pytube import YouTube
import io
import re

st.set_page_config(page_title="Youtube to Media Download", page_icon="⬇️")

st.title("Youtube to Media Download")
st.write("Enter a YouTube video URL to download it as a video or audio file.")

yt_url = st.text_input("YouTube URL:")
download_format = st.radio("Select Download Format:", ('Video', 'Audio'))

if yt_url:
    try:
        yt = YouTube(yt_url)
        
        st.subheader(f"Video Title: {yt.title}")
        st.image(yt.thumbnail_url, caption="Video Thumbnail", use_column_width=True)

        if download_format == 'Video':
            stream = yt.streams.get_highest_resolution()
            file_name = f"{re.sub(r'[\\/:*?"<>|]', '', yt.title)}.mp4"
            st.info("Downloading highest resolution video stream...")
        else:
            stream = yt.streams.filter(only_audio=True, file_extension='mp4').first()
            file_name = f"{re.sub(r'[\\/:*?"<>|]', '', yt.title)}.mp4"
            st.info("Downloading best quality audio stream...")

        if stream:
            buffer = io.BytesIO()
            stream.stream_to_buffer(buffer)
            buffer.seek(0)
            
            st.success("Download ready!")
            st.download_button(
                label=f"Download {download_format}",
                data=buffer,
                file_name=file_name,
                mime=stream.mime_type
            )
        else:
            st.error("Could not find a suitable stream to download.")

    except Exception as e:
        error_message = f"An error occurred: {e}. Please check the URL and try again."
        if 'HTTP Error 400' in str(e):
            error_message += "\n\nThis often means the `pytube` library is out of date. Try running `pip install --upgrade pytube` to fix this."
        st.error(error_message)
        st.stop()
