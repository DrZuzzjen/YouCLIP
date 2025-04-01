import streamlit as st

# IMPORTANT: Do NOT include st.set_page_config() here, it must only be in the main app.py

def apply_styling():
    """Apply custom CSS styling to the app."""
    st.markdown("""
    <style>
        /* Main colors and variables */
        :root {
            --primary: #FF0066;
            --primary-light: #FF4D94;
            --primary-dark: #CC0052;
            --secondary: #333333;
            --bg-dark: #1A1A1A;
            --bg-card: #2A2A2A;
            --text-light: #FFFFFF;
            --text-muted: #BBBBBB;
            --success: #00CC88;
            --info: #3EA6FF;
            --warning: #FFCC00;
            --border-radius: 12px;
        }
        
        /* Reset and base styles */
        .stApp {
            background-color: var(--bg-dark);
            color: var(--text-light);
            font-family: 'Segoe UI', Roboto, -apple-system, BlinkMacSystemFont, sans-serif;
        }
        
        h1, h2, h3, h4, h5, h6 {
            color: var(--text-light) !important;
            font-family: 'Segoe UI', Roboto, sans-serif;
            font-weight: 600;
        }
        
        /* Header styling */
        .header-container {
            display: flex;
            align-items: center;
            margin-bottom: 30px;
        }
        
        .logo-text {
            font-size: 32px;
            font-weight: 800;
            background: linear-gradient(135deg, var(--primary), #FF3366);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            padding: 0;
        }
        
        .subtitle-text {
            color: var(--text-muted);
            font-size: 14px;
            margin-top: -5px;
            margin-bottom: 20px;
        }
        
        /* Card styling */
        .card {
            background-color: var(--bg-card);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.05);
        }
        
        /* Video container */
        .video-container {
            border-radius: 8px;
            overflow: hidden;
            margin-bottom: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            max-height: 500px;
        }
        
        /* Set fixed height for video display */
        .stVideo {
            max-height: 400px !important;
            margin: 0 auto;
            display: block;
        }
        
        /* Force video container to maintain aspect ratio */
        .stVideo > div {
            position: relative !important;
            width: 100% !important;
            height: 0 !important;
            padding-bottom: 56.25% !important; /* 16:9 aspect ratio */
        }
        
        .stVideo > div > video {
            position: absolute !important;
            top: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 100% !important;
            object-fit: contain !important; /* Ensures the whole video is visible */
            background-color: black !important;
        }
        
        .video-info {
            margin-top: 15px;
        }
        
        .video-title {
            font-size: 18px;
            font-weight: 600;
            margin-bottom: 8px;
        }
        
        .video-metadata {
            display: flex;
            gap: 15px;
            color: var(--text-muted);
            font-size: 14px;
            margin-bottom: 20px;
        }
        
        /* Workflow styles */
        .workflow-step {
            background-color: var(--bg-card);
            border-radius: var(--border-radius);
            padding: 20px;
            margin-bottom: 20px;
        }
        
        .workflow-step h2 {
            margin-top: 0;
            font-size: 18px;
            margin-bottom: 20px;
        }
        
        /* Form elements */
        .stTextInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            color: var(--text-light);
            padding: 12px 15px;
            font-size: 16px;
        }
        
        .stTextInput > div > div > input:focus {
            border-color: var(--primary);
        }
        
        .stNumberInput > div > div > input {
            background-color: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            color: var(--text-light);
            padding: 8px 10px;
            font-size: 14px;
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 6px;
            padding: 12px 20px;
            font-weight: 600;
            transition: all 0.2s;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-light);
            transform: translateY(-2px);
        }
        
        /* Secondary button - used for 'Back' and non-primary actions */
        .secondary-btn {
            background-color: transparent !important;
            border: 1px solid var(--primary) !important;
            color: var(--primary) !important;
        }
        
        .secondary-btn:hover {
            background-color: rgba(255, 0, 102, 0.1) !important;
        }
        
        /* Format selection cards */
        .format-container {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            margin-bottom: 20px;
        }
        
        .format-card {
            flex: 1;
            background-color: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 8px;
            padding: 15px;
            text-align: center;
            cursor: pointer;
            transition: all 0.2s;
        }
        
        .format-card:hover, .format-card.selected {
            background-color: rgba(255, 0, 102, 0.1);
            border-color: var(--primary);
            transform: translateY(-2px);
        }
        
        .format-card .format-name {
            font-weight: 600;
            font-size: 16px;
            margin-bottom: 5px;
        }
        
        .format-card .format-desc {
            font-size: 12px;
            color: var(--text-muted);
        }
        
        /* Slider and range inputs */
        .stSlider > div > div {
            color: var(--primary) !important;
        }
        
        /* Success/info/error messages */
        .success-msg {
            color: var(--success);
            padding: 10px;
            border-radius: 6px;
            background-color: rgba(0, 204, 136, 0.1);
            margin-bottom: 15px;
        }
        
        .info-msg {
            color: var(--info);
            padding: 10px;
            border-radius: 6px;
            background-color: rgba(62, 166, 255, 0.1);
            margin-bottom: 15px;
        }
        
        .error-msg {
            color: #FF6B6B;
            padding: 10px;
            border-radius: 6px;
            background-color: rgba(255, 107, 107, 0.1);
            margin-bottom: 15px;
        }
        
        /* Progress indicators */
        .progress-indicator {
            height: 5px;
            width: 100%;
            background-color: rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            margin-bottom: 15px;
            overflow: hidden;
        }
        
        .progress-bar {
            height: 100%;
            background-color: var(--primary);
            border-radius: 5px;
        }
        
        /* Tabs styling */
        .stTabs [data-baseweb="tab-list"] {
            gap: 8px;
            background-color: var(--bg-card);
            padding: 0 10px;
            border-radius: var(--border-radius) var(--border-radius) 0 0;
        }
        
        .stTabs [data-baseweb="tab"] {
            padding: 15px 20px;
            background-color: transparent;
            border: none;
            color: var(--text-muted);
            font-size: 16px;
        }
        
        .stTabs [aria-selected="true"] {
            background-color: transparent !important;
            color: var(--text-light) !important;
            font-weight: 600;
            border-bottom: 3px solid var(--primary) !important;
        }
        
        /* Tab content padding for better readability */
        .stTabs [data-baseweb="tab-panel"] {
            background-color: var(--bg-card);
            border-radius: 0 0 var(--border-radius) var(--border-radius);
            padding: 20px;
        }
        
        /* Hide Streamlit branding and hamburger menu */
        #MainMenu, footer {
            visibility: hidden;
        }
        
        /* Download button styling */
        .download-btn {
            display: inline-block;
            background: linear-gradient(135deg, var(--primary), var(--primary-light));
            color: white !important;
            text-decoration: none;
            padding: 12px 20px;
            border-radius: 6px;
            font-weight: 600;
            transition: all 0.2s;
            text-align: center;
            margin-top: 10px;
            width: auto;
        }
        
        .download-btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(255, 0, 102, 0.3);
        }
        
        /* Subtitle preview styling */
        .subtitle-preview {
            background-color: rgba(0, 0, 0, 0.2);
            border-radius: 6px;
            padding: 15px;
            max-height: 150px;
            overflow-y: auto;
            font-family: monospace;
            font-size: 12px;
            color: var(--text-muted);
            margin-bottom: 20px;
        }
        
        /* Language selection buttons */
        .language-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
        }
        
        .language-option {
            flex: 1;
            padding: 10px;
            background-color: rgba(0, 0, 0, 0.2);
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 6px;
            text-align: center;
            cursor: pointer;
        }
        
        .language-option.selected {
            background-color: rgba(255, 0, 102, 0.1);
            border-color: var(--primary);
        }
    </style>
    """, unsafe_allow_html=True)

def render_header():
    """Render the app header with logo and subtitle."""
    st.markdown('<div class="header-container">', unsafe_allow_html=True)
    st.markdown('<h1 class="logo-text">YouClip</h1>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle-text">Create, customize, and subtitle YouTube videos in seconds</p>', unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar content with instructions and about section."""
    with st.sidebar:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("## How to use YouClip")
        st.write("1. Enter a YouTube URL")
        st.write("2. Set start and end times for your clip")
        st.write("3. Choose video format and quality")
        st.write("4. Generate your clip")
        st.write("5. Add AI-generated subtitles (optional)")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("## About YouClip")
        st.write("YouClip is a powerful tool that allows you to create custom clips from YouTube videos with optional AI-generated subtitles.")
        
        # Features section
        st.markdown("""
        <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 10px; margin-top: 15px;">
            <div style="text-align: center; padding: 10px; background-color: rgba(0,0,0,0.2); border-radius: 6px;">
                <div style="font-size: 24px; margin-bottom: 5px;">⚡</div>
                <div>Fast Processing</div>
            </div>
            <div style="text-align: center; padding: 10px; background-color: rgba(0,0,0,0.2); border-radius: 6px;">
                <div style="font-size: 24px; margin-bottom: 5px;">🎨</div>
                <div>Multiple Formats</div>
            </div>
            <div style="text-align: center; padding: 10px; background-color: rgba(0,0,0,0.2); border-radius: 6px;">
                <div style="font-size: 24px; margin-bottom: 5px;">🔤</div>
                <div>AI Subtitles</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    """Render the footer content."""
    st.markdown("""
    <div style="text-align: center; margin-top: 40px; padding-top: 20px; border-top: 1px solid rgba(255, 255, 255, 0.1); color: var(--text-muted); font-size: 12px;">
        <p>YouClip - Create beautiful clips from YouTube videos with ease.</p>
        <p>© 2025 YouClip</p>
    </div>
    """, unsafe_allow_html=True)

def render_video_preview(video_info=None, video_path=None, title="Video Preview"):
    """Render the video preview area."""
    st.markdown('<div class="card">', unsafe_allow_html=True)
    st.write(f"## {title}")
    
    if video_path and os.path.exists(video_path):
        # Display video if a path is provided
        file_size = os.path.getsize(video_path) / (1024 * 1024)  # MB
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.video(video_path)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Add download button for the video
        file_name = os.path.basename(video_path)
        st.markdown(
            get_download_link(video_path, file_name, f"Download Video ({int(file_size)}MB)"),
            unsafe_allow_html=True
        )
    elif video_info:
        # Display video thumbnail and info if video_info is provided
        st.markdown('<div class="video-container">', unsafe_allow_html=True)
        st.image(video_info["thumbnail"], use_column_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="video-info">', unsafe_allow_html=True)
        st.markdown(f'<div class="video-title">{video_info["title"]}</div>', unsafe_allow_html=True)
        st.markdown('<div class="video-metadata">', unsafe_allow_html=True)
        st.markdown(f'<span>Channel: {video_info["author"]}</span>', unsafe_allow_html=True)
        st.markdown(f'<span>Duration: {format_time(video_info["length"])}</span>', unsafe_allow_html=True)
        st.markdown(f'<span>Views: {video_info["views"]:,}</span>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    else:
        # Placeholder when no video is selected
        st.markdown("""
        <div style="height: 200px; display: flex; align-items: center; justify-content: center; 
                   background-color: #1A1A1A; border-radius: 8px; color: var(--text-muted);">
            Enter a YouTube URL to get started
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

def format_time(seconds):
    """Format seconds to HH:MM:SS or MM:SS."""
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    if hours > 0:
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"
    else:
        return f"{int(minutes):02d}:{int(seconds):02d}"

def progress_bar(progress_value, label=None):
    """Render a custom progress bar."""
    st.markdown(f"""
    <div class="progress-indicator">
        <div class="progress-bar" style="width: {progress_value}%;"></div>
    </div>
    {f'<div style="text-align: center; font-size: 12px; color: var(--text-muted);">{label}</div>' if label else ''}
    """, unsafe_allow_html=True)

def success_message(message):
    """Display a styled success message."""
    st.markdown(f'<div class="success-msg">{message}</div>', unsafe_allow_html=True)

def info_message(message):
    """Display a styled info message."""
    st.markdown(f'<div class="info-msg">{message}</div>', unsafe_allow_html=True)

def error_message(message):
    """Display a styled error message."""
    st.markdown(f'<div class="error-msg">{message}</div>', unsafe_allow_html=True)

import os

# Required for video preview
def get_download_link(file_path, download_filename, button_text="Download Video"):
    """Generate a download link for files."""
    import base64
    with open(file_path, "rb") as file:
        encoded_file = base64.b64encode(file.read()).decode()
    href = f'<a href="data:video/mp4;base64,{encoded_file}" download="{download_filename}" class="download-btn">{button_text}</a>'
    return href