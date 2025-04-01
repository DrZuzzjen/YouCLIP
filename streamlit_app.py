import streamlit as st

# Set page configuration - MUST be the first Streamlit command
st.set_page_config(
    page_title="YouClip - YouTube Video Clipper",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Then import all other modules
from youtube_utils import get_video_info, download_video
from ffmpeg_utils import clip_video, format_time
from ui_components import (
    apply_styling, render_header, render_sidebar, render_footer, 
    render_video_preview, success_message, info_message, error_message,
    progress_bar, get_download_link
)
from subtitle_utils import extract_audio, create_srt_file, embed_subtitles, transcribe_audio

import tempfile
import os
import re
import time
import base64

# Initialize session state variables
if 'current_step' not in st.session_state:
    st.session_state.current_step = 1  # 1 = Source, 2 = Clip, 3 = Enhance

if 'clip_path' not in st.session_state:
    st.session_state.clip_path = None
if 'clip_filename' not in st.session_state:
    st.session_state.clip_filename = None
if 'clip_temp_dir' not in st.session_state:
    st.session_state.clip_temp_dir = None
if 'clip_format' not in st.session_state:
    st.session_state.clip_format = None
if 'selected_format' not in st.session_state:
    st.session_state.selected_format = "MP4"
if 'subtitle_generated' not in st.session_state:
    st.session_state.subtitle_generated = False
if 'srt_path' not in st.session_state:
    st.session_state.srt_path = None
if 'processing_subtitles' not in st.session_state:
    st.session_state.processing_subtitles = False
if 'processing_clip' not in st.session_state:
    st.session_state.processing_clip = False
if 'subtitled_video_path' not in st.session_state:
    st.session_state.subtitled_video_path = None
if 'video_info' not in st.session_state:
    st.session_state.video_info = None
# Add a flag to prevent the infinite loop with rerun
if 'url_processed' not in st.session_state:
    st.session_state.url_processed = False

# Apply custom styling
apply_styling()

# Render header
render_header()

# Render sidebar
render_sidebar()

# Main layout - two column design
col1, col2 = st.columns([6, 4])

with col1:
    # Video preview area - always visible
    if st.session_state.subtitled_video_path and os.path.exists(st.session_state.subtitled_video_path):
        # Show subtitled video if available
        render_video_preview(
            video_path=st.session_state.subtitled_video_path
        )
    elif st.session_state.clip_path and os.path.exists(st.session_state.clip_path) and not st.session_state.processing_clip:
        # Show clip if available and not in processing state
        render_video_preview(
            video_path=st.session_state.clip_path
        )
    else:
        # Show video info or placeholder
        render_video_preview(
            video_info=st.session_state.video_info
        )

with col2:
    # Workflow tabs
    tabs = st.tabs(["1. Source", "2. Create Clip", "3. Add Subtitles"])
    
    # Tab 1: Source - Enter YouTube URL
    with tabs[0]:
        st.markdown("### Enter YouTube URL")
        url = st.text_input(
            "Paste a YouTube video URL:", 
            placeholder="https://www.youtube.com/watch?v=...",
            key="youtube_url"
        )
        
        # Check if URL was entered
        if url:
            # Validate URL
            if not re.match(r'https?://(www\.)?youtube\.com/watch\?v=.+|https?://youtu\.be/.+', url):
                error_message("Please enter a valid YouTube URL")
                st.session_state.url_processed = False  # Reset the flag for invalid URLs
            else:
                # Check if this URL has already been processed
                already_processed = st.session_state.url_processed
                
                if not already_processed:
                    with st.spinner("Fetching video information..."):
                        video_info = get_video_info(url)
                        if video_info:
                            # Update session state with new video info
                            st.session_state.video_info = video_info
                            st.session_state.url_processed = True
                            st.session_state.current_step = 2
                            
                            # After getting video info, display success message
                            success_message("Video information retrieved successfully!")
                            info_message("Click on the 'Create Clip' tab to continue")
                            
                            # Force a rerun to refresh the UI with the video preview
                            st.rerun()
                
                # If URL was already processed, just show the success messages again
                elif already_processed and st.session_state.video_info:
                    success_message("Video information retrieved successfully!")
                    info_message("Click on the 'Create Clip' tab to continue")
                    
        # If URL is cleared or changed, reset the processed flag
        elif st.session_state.url_processed:
            st.session_state.url_processed = False
    
    # Tab 2: Create Clip - Set timing, format, quality
    with tabs[1]:
        if st.session_state.video_info:
            st.markdown("### Set Clip Timing")
            
            video_length = st.session_state.video_info["length"]
            
            # Time selection with simplified controls (no nested columns)
            st.markdown("**Start Time**")
            start_min = st.number_input("Minutes", min_value=0, max_value=int(video_length/60), step=1, key="start_min")
            start_sec = st.number_input("Seconds", min_value=0, max_value=59, step=1, key="start_sec")
            
            st.markdown("**End Time**")
            end_min = st.number_input("Minutes", min_value=0, max_value=int(video_length/60), value=min(1, int(video_length/60)), step=1, key="end_min")
            end_sec = st.number_input("Seconds", min_value=0, max_value=59, value=0, step=1, key="end_sec")
            
            # Calculate total seconds
            start_time_sec = start_min * 60 + start_sec
            end_time_sec = end_min * 60 + end_sec
            
            # Validate time selection
            if end_time_sec <= start_time_sec:
                error_message("End time must be after start time")
                valid_time_selection = False
            elif end_time_sec > video_length:
                error_message(f"End time exceeds video length ({format_time(video_length)})")
                valid_time_selection = False
            else:
                valid_time_selection = True
                success_message(f"Selected clip length: {format_time(end_time_sec - start_time_sec)}")
            
            st.markdown("### Choose Format & Quality")
            
            # Format selection with simplified UI
            st.markdown("Select video format:")
            format_option = st.radio(
                "Video Format",
                options=["MP4", "WebM", "MKV"],
                horizontal=True,
                help="MP4: Most compatible | WebM: Better compression | MKV: High quality container",
                label_visibility="collapsed"
            )
            st.session_state.selected_format = format_option
            
            st.markdown(f"**Selected format:** {st.session_state.selected_format}")
            
            # Quality selection with more visual slider
            quality = st.select_slider(
                "Select video quality:",
                options=["Low", "Medium", "High"],
                value="Medium",
                key="quality_slider"
            )
            
            # Quality info
            quality_info = {
                "Low": "360p resolution, smaller file size",
                "Medium": "480p resolution, balanced quality and size",
                "High": "720p resolution, best quality"
            }
            info_message(quality_info[quality])
            
            # Generate clip button
            if valid_time_selection:
                if st.button("Generate Clip", key="generate_clip_btn", use_container_width=True):
                    try:
                        # Set processing flag to keep showing the thumbnail during processing
                        st.session_state.processing_clip = True
                        
                        with st.spinner("Processing your clip..."):
                            # Create temp directory
                            temp_dir = tempfile.mkdtemp()
                            
                            # Show progress
                            progress_placeholder = st.empty()
                            progress_placeholder.markdown("Downloading video...")
                            progress_bar(25, "Downloading video")
                            
                            # Download video
                            download_path = download_video(st.session_state.video_info, url, temp_dir)
                            
                            if not download_path:
                                error_message("Failed to download video. Please try again.")
                                st.session_state.processing_clip = False  # Reset processing flag
                                st.stop()
                            
                            # Update progress
                            progress_placeholder.markdown("Processing clip...")
                            progress_bar(50, "Processing clip")
                            
                            # Format times for ffmpeg
                            def format_ffmpeg_time(seconds):
                                hours, remainder = divmod(seconds, 3600)
                                minutes, seconds = divmod(remainder, 60)
                                return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
                            
                            start_time_fmt = format_ffmpeg_time(start_time_sec)
                            end_time_fmt = format_ffmpeg_time(end_time_sec)
                            
                            # Create output filename
                            safe_title = re.sub(r'[^\w\-_]', '_', st.session_state.video_info["title"])
                            safe_title = safe_title[:50] if len(safe_title) > 50 else safe_title
                            safe_title = safe_title.strip()
                            timestamp = int(time.time())
                            output_filename = f"{safe_title}_{timestamp}.{st.session_state.selected_format.lower()}"
                            output_path = os.path.join(temp_dir, output_filename)
                            
                            # Clip video
                            success = clip_video(download_path, output_path, start_time_fmt, end_time_fmt, st.session_state.selected_format, quality)
                            
                            # Update progress
                            progress_placeholder.markdown("Finalizing...")
                            progress_bar(100, "Complete")
                            
                            if success:
                                # Update session state
                                st.session_state.clip_path = output_path
                                st.session_state.clip_filename = output_filename
                                st.session_state.clip_temp_dir = temp_dir
                                st.session_state.clip_format = st.session_state.selected_format
                                
                                # Reset subtitle related states
                                st.session_state.subtitle_generated = False
                                st.session_state.processing_subtitles = False
                                st.session_state.srt_path = None
                                st.session_state.subtitled_video_path = None
                                
                                # Reset processing flag after successful clip generation
                                st.session_state.processing_clip = False
                                
                                # Success message
                                success_message("Clip generated successfully!")
                                
                                # Update tab guidance
                                st.info("Click on the 'Add Subtitles' tab to enhance your clip with AI-generated subtitles")
                                
                                # Force rerun to show the clip in the preview area
                                st.rerun()
                            else:
                                # Reset processing flag if failed
                                st.session_state.processing_clip = False
                                error_message("Failed to generate clip. Please try again.")
                    
                    except Exception as e:
                        # Reset processing flag on error
                        st.session_state.processing_clip = False
                        error_message(f"An error occurred: {str(e)}")
        else:
            # Prompt user to first enter a YouTube URL
            info_message("Please enter a YouTube URL in the Source tab first.")
    
    # Tab 3: Add Subtitles
    with tabs[2]:
        if st.session_state.clip_path and os.path.exists(st.session_state.clip_path):
            st.markdown("### Add AI-Generated Subtitles")
            st.write("Enhance your clip with automatically generated subtitles.")
            
            # Language selection with simplified UI
            st.markdown("Select subtitle language:")
            subtitle_language = st.radio(
                "Subtitle Language",
                options=["English", "Spanish"],
                horizontal=True,
                label_visibility="collapsed"
            )
            st.session_state.subtitle_language = subtitle_language
            
            # Generate subtitles button
            if st.button("Generate Subtitles", key="generate_subtitles_btn", use_container_width=True):
                st.session_state.processing_subtitles = True
            
            # Process subtitles if button was clicked
            if st.session_state.processing_subtitles and not st.session_state.subtitle_generated:
                with st.spinner("Processing subtitles..."):
                    # Step 1: Extract audio
                    progress_placeholder = st.empty()
                    progress_placeholder.markdown("Extracting audio...")
                    progress_bar(20, "Extracting audio")
                    
                    audio_path = extract_audio(st.session_state.clip_path, st.session_state.clip_temp_dir)
                    
                    if audio_path:
                        # Step 2: Transcribe audio
                        progress_placeholder.markdown("Transcribing audio...")
                        progress_bar(50, "Transcribing audio")
                        
                        lang_code = "en" if subtitle_language == "English" else "es"
                        transcription = transcribe_audio(audio_path, language=lang_code)
                        
                        # Step 3: Create SRT file
                        progress_placeholder.markdown("Creating subtitle file...")
                        progress_bar(80, "Creating subtitles")
                        
                        base_filename = os.path.splitext(os.path.basename(st.session_state.clip_path))[0]
                        srt_path = create_srt_file(transcription, st.session_state.clip_temp_dir, base_filename)
                        
                        if srt_path:
                            progress_placeholder.markdown("Complete!")
                            progress_bar(100, "Complete")
                            
                            st.session_state.srt_path = srt_path
                            st.session_state.subtitle_generated = True
                            st.rerun()
                    else:
                        error_message("Failed to extract audio from video.")
                        st.session_state.processing_subtitles = False
            
            # Display subtitle results if generated
            if st.session_state.subtitle_generated and st.session_state.srt_path:
                srt_filename = os.path.basename(st.session_state.srt_path)
                success_message("Subtitles generated successfully!")
                
                # Show subtitle preview in expander
                with st.expander("View subtitle text", expanded=False):
                    with open(st.session_state.srt_path, "r", encoding="utf-8") as f:
                        srt_content = f.read()
                    
                    st.text_area("Generated subtitles:", srt_content, height=150, key="subtitle_preview")
                    
                    # Download SRT file button
                    st.markdown(
                        get_download_link(
                            st.session_state.srt_path, 
                            srt_filename, 
                            f"Download {subtitle_language} SRT File"
                        ),
                        unsafe_allow_html=True
                    )
                
                # Embed subtitles section
                st.markdown("### Add Subtitles to Video")
                
                if st.button("Embed Subtitles in Video", key="embed_subtitles_btn", use_container_width=True):
                    with st.spinner("Embedding subtitles..."):
                        progress_placeholder = st.empty()
                        progress_placeholder.markdown("Embedding subtitles in video...")
                        progress_bar(50, "Processing video")
                        
                        subtitle_video_path = embed_subtitles(
                            st.session_state.clip_path, 
                            st.session_state.srt_path,
                            st.session_state.clip_temp_dir,
                            st.session_state.clip_format
                        )
                        
                        if subtitle_video_path:
                            progress_bar(100, "Complete")
                            st.session_state.subtitled_video_path = subtitle_video_path
                            success_message("Subtitles embedded successfully!")
                            st.rerun()
                        else:
                            error_message("Failed to embed subtitles. Please check the logs.")
                
                # Display download buttons for videos
                if st.session_state.subtitled_video_path and os.path.exists(st.session_state.subtitled_video_path):
                    subtitle_filename = os.path.basename(st.session_state.subtitled_video_path)
                    
                    st.markdown(
                        get_download_link(
                            st.session_state.clip_path, 
                            st.session_state.clip_filename, 
                            "Download Original Clip"
                        ),
                        unsafe_allow_html=True
                    )
                    
                    st.markdown(
                        get_download_link(
                            st.session_state.subtitled_video_path, 
                            subtitle_filename, 
                            f"Download Clip with Subtitles"
                        ),
                        unsafe_allow_html=True
                    )
        else:
            # Prompt user to first create a clip
            info_message("Please generate a clip in the Create Clip tab first.")

# Footer
render_footer()