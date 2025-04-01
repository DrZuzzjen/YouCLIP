import streamlit as st
from youtube_utils import get_video_info, download_video
from ffmpeg_utils import clip_video, format_time
from ui_components import apply_styling, render_sidebar, render_footer
import tempfile
import os
import re
import time
import base64

# Set page configuration
st.set_page_config(
    page_title="YouClip - YouTube Video Clipper",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Apply custom styling
apply_styling()

# Header section
st.markdown('<div class="title-container">', unsafe_allow_html=True)
st.markdown('<h1 class="app-title">YouClip</h1>', unsafe_allow_html=True)
st.markdown('</div>', unsafe_allow_html=True)
st.markdown('<p class="subtitle">Create, customize, and download clips from YouTube videos</p>', unsafe_allow_html=True)

# Render sidebar
render_sidebar()

# Function to get downloadable link
def get_download_link(file_path, download_filename, button_text="Download Video"):
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode()
    href = f'<a href="data:video/mp4;base64,{encoded_file}" download="{download_filename}" class="download-btn">{button_text}</a>'
    return href

# Main content area
st.markdown('<div class="card">', unsafe_allow_html=True)
st.write("## Enter YouTube URL")
url = st.text_input("Paste a YouTube video URL here:", placeholder="https://www.youtube.com/watch?v=...")

video_info = None
if url:
    # Validate URL
    if not re.match(r'https?://(www\.)?youtube\.com/watch\?v=.+|https?://youtu\.be/.+', url):
        st.warning("Please enter a valid YouTube URL")
    else:
        with st.spinner("Fetching video information..."):
            video_info = get_video_info(url)
st.markdown('</div>', unsafe_allow_html=True)

# Display video information and clipping options if video info is available
if video_info:
    # Video information card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("## Video Information")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.image(video_info["thumbnail"], use_column_width=True)
    
    with col2:
        st.write(f"**Title:** {video_info['title']}")
        st.write(f"**Channel:** {video_info['author']}")
        st.write(f"**Duration:** {format_time(video_info['length'])}")
        st.write(f"**Views:** {video_info['views']:,}")
        if video_info['publish_date']:
            st.write(f"**Published:** {video_info['publish_date'].strftime('%B %d, %Y')}")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Video clipping options card
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write("## Create Your Clip")
    
    # Time selection
    st.write("### Set Start and End Times")
    video_length = video_info["length"]
    
    # Allow manual time input
    col1, col2 = st.columns(2)
    with col1:
        start_min = st.number_input("Start Minute", min_value=0, max_value=int(video_length/60), step=1)
        start_sec = st.number_input("Start Second", min_value=0, max_value=59, step=1)
    with col2:
        end_min = st.number_input("End Minute", min_value=0, max_value=int(video_length/60), value=min(1, int(video_length/60)), step=1)
        end_sec = st.number_input("End Second", min_value=0, max_value=59, value=0, step=1)
    
    # Calculate total seconds
    start_time_sec = start_min * 60 + start_sec
    end_time_sec = end_min * 60 + end_sec
    
    # Validate time selection
    if end_time_sec <= start_time_sec:
        st.warning("End time must be after start time")
        valid_time_selection = False
    elif end_time_sec > video_length:
        st.warning(f"End time exceeds video length ({format_time(video_length)})")
        valid_time_selection = False
    else:
        valid_time_selection = True
        st.success(f"Selected clip length: {format_time(end_time_sec - start_time_sec)}")
        
    # Format and quality selection
    st.write("### Choose Format and Quality")
    
    # Initialize session state for format selection
    if 'selected_format' not in st.session_state:
        st.session_state.selected_format = "MP4"
    
    # Format selection with custom cards
    st.markdown("<p>Select video format:</p>", unsafe_allow_html=True)
    format_options = ["MP4", "WebM", "MKV"]
    format_descriptions = {
        "MP4": "Most compatible",
        "WebM": "Better compression",
        "MKV": "High quality container"
    }
    
    col1, col2, col3 = st.columns(3)
    format_cols = [col1, col2, col3]
    
    for i, fmt in enumerate(format_options):
        with format_cols[i]:
            if st.button(f"{fmt}\n{format_descriptions[fmt]}", key=f"fmt_{fmt}"):
                st.session_state.selected_format = fmt
    
    st.write(f"Selected format: **{st.session_state.selected_format}**")
    
    # Quality selection
    quality = st.select_slider(
        "Select video quality:",
        options=["Low", "Medium", "High"],
        value="Medium"
    )
    
    # Quality info display
    quality_info = {
        "Low": "360p resolution, smaller file size",
        "Medium": "480p resolution, balanced quality and size",
        "High": "720p resolution, best quality"
    }
    st.info(quality_info[quality])
    
    # Generate clip button
    if valid_time_selection:
        if st.button("Generate Clip", key="generate_clip"):
            try:
                with st.spinner("Processing your clip..."):
                    # Create temp directory if it doesn't exist
                    temp_dir = tempfile.mkdtemp()
                    
                    # Download video
                    progress_bar = st.progress(0)
                    st.markdown('<div class="loading">Downloading video...</div>', unsafe_allow_html=True)
                    
                    download_path = download_video(video_info, url, temp_dir)
                    
                    if not download_path:
                        st.error("Failed to download video. Please try again.")
                        st.stop()
                        
                    progress_bar.progress(50)
                    
                    # Format times for ffmpeg
                    def format_ffmpeg_time(seconds):
                        hours, remainder = divmod(seconds, 3600)
                        minutes, seconds = divmod(remainder, 60)
                        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
                        
                    start_time_fmt = format_ffmpeg_time(start_time_sec)
                    end_time_fmt = format_ffmpeg_time(end_time_sec)
                    
                    # Create output filename
                    safe_title = re.sub(r'[^\w\-_]', '_', video_info["title"])
                    # Limit filename length to avoid path too long errors
                    safe_title = safe_title[:50] if len(safe_title) > 50 else safe_title
                    # Ensure we don't have trailing or leading spaces
                    safe_title = safe_title.strip()
                    # Use a timestamp to ensure uniqueness
                    timestamp = int(time.time())
                    output_filename = f"{safe_title}_{timestamp}.{st.session_state.selected_format.lower()}"
                    output_path = os.path.join(temp_dir, output_filename)
                    
                    # Update UI
                    st.markdown('<div class="loading">Clipping video...</div>', unsafe_allow_html=True)
                    
                    # Clip video
                    success = clip_video(download_path, output_path, start_time_fmt, end_time_fmt, st.session_state.selected_format, quality)
                    progress_bar.progress(100)
                    
                    if success:
                        st.success("Clip generated successfully!")
                        
                        # Display download button
                        st.markdown(
                            get_download_link(output_path, output_filename, f"Download {st.session_state.selected_format} ({quality} Quality)"),
                            unsafe_allow_html=True
                        )
                        
                        # Display preview if it's small enough
                        file_size = os.path.getsize(output_path) / (1024 * 1024)  # MB
                        if file_size < 50:  # Only show preview for files < 50MB
                            st.markdown('<div class="video-container">', unsafe_allow_html=True)
                            st.video(output_path)
                            st.markdown('</div>', unsafe_allow_html=True)
                        else:
                            st.info("Preview not available for large clips. Please download the file to view.")
                    else:
                        st.error("Failed to generate clip. Please try again.")
            
            except Exception as e:
                st.error(f"An error occurred: {str(e)}")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer
render_footer()