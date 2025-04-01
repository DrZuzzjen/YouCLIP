import streamlit as st

def apply_styling():
    """Apply custom CSS styling to the app."""
    st.markdown("""
    <style>
        /* Main colors and variables */
        :root {
            --primary: #FF0000;
            --primary-light: #ff6666;
            --secondary: #121212;
            --text: #FFFFFF;
            --bg: #1E1E1E;
            --card-bg: #2D2D2D;
            --accent: #3EA6FF;
        }
        
        /* General page styling */
        .stApp {
            background-color: var(--bg);
            color: var(--text);
        }
        
        /* Header styling */
        h1, h2, h3 {
            color: var(--text) !important;
            font-family: 'Roboto', sans-serif;
        }
        
        /* Main title styling */
        .title-container {
            display: flex;
            align-items: center;
            margin-bottom: 20px;
        }
        
        .app-title {
            font-size: 3rem !important;
            font-weight: 700 !important;
            background: linear-gradient(90deg, #FF0000, #FF6B6B);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin: 0;
            padding: 0;
        }
        
        .subtitle {
            font-size: 1.2rem;
            opacity: 0.8;
            margin-top: -5px;
        }
        
        /* Card styling */
        .card {
            background-color: var(--card-bg);
            border-radius: 10px;
            padding: 20px;
            margin-bottom: 20px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        }
        
        /* Button styling */
        .stButton > button {
            background-color: var(--primary);
            color: white;
            border: none;
            border-radius: 5px;
            padding: 10px 24px;
            font-weight: 600;
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            background-color: var(--primary-light);
            box-shadow: 0 4px 8px rgba(255, 0, 0, 0.2);
            transform: translateY(-2px);
        }
        
        /* Input styling */
        .stTextInput > div > div > input {
            background-color: #383838;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
            padding: 10px 15px;
        }
        
        /* Slider styling */
        .stSlider > div > div {
            color: var(--accent) !important;
        }
        
        /* Selectbox styling */
        .stSelectbox > div > div {
            background-color: #383838;
            color: white;
            border: 1px solid rgba(255, 255, 255, 0.2);
            border-radius: 5px;
        }
        
        /* Video container */
        .video-container {
            border-radius: 10px;
            overflow: hidden;
            border: 1px solid rgba(255, 255, 255, 0.1);
            box-shadow: 0 4px 20px rgba(0, 0, 0, 0.3);
        }
        
        /* Progress bar */
        .stProgress > div > div > div {
            background-color: var(--accent);
        }
        
        /* Features section */
        .features-container {
            display: grid;
            grid-template-columns: repeat(3, 1fr);
            gap: 20px;
            margin-top: 20px;
        }
        
        .feature-card {
            background-color: rgba(45, 45, 45, 0.7);
            border-radius: 8px;
            padding: 15px;
            border: 1px solid rgba(255, 255, 255, 0.1);
            text-align: center;
        }
        
        .feature-icon {
            font-size: 2rem;
            margin-bottom: 10px;
            color: var(--accent);
        }
        
        /* Footer styling */
        .footer {
            text-align: center;
            margin-top: 40px;
            padding-top: 20px;
            border-top: 1px solid rgba(255, 255, 255, 0.1);
            font-size: 0.8rem;
            opacity: 0.7;
        }
        
        /* Download button */
        .download-btn {
            display: inline-block;
            background: linear-gradient(90deg, var(--primary), var(--primary-light));
            color: white;
            text-decoration: none;
            padding: 10px 20px;
            border-radius: 5px;
            font-weight: 600;
            margin-top: 10px;
            transition: all 0.3s ease;
            text-align: center;
        }
        
        .download-btn:hover {
            box-shadow: 0 4px 12px rgba(255, 0, 0, 0.3);
            transform: translateY(-2px);
        }
        
        /* Format selection cards */
        .format-container {
            display: flex;
            gap: 10px;
            margin-top: 15px;
            flex-wrap: wrap;
        }
        
        .format-card {
            background-color: #383838;
            border: 1px solid rgba(255, 255, 255, 0.1);
            border-radius: 5px;
            padding: 15px;
            text-align: center;
            min-width: 100px;
            cursor: pointer;
            transition: all 0.3s ease;
        }
        
        .format-card:hover, .format-card.selected {
            background-color: rgba(62, 166, 255, 0.2);
            border-color: var(--accent);
            transform: translateY(-2px);
        }
        
        .format-card .format-name {
            font-weight: 600;
            font-size: 1.1rem;
            margin-bottom: 5px;
        }
        
        .format-card .format-desc {
            font-size: 0.8rem;
            opacity: 0.7;
        }
        
        /* Loading animation */
        @keyframes pulse {
            0% {
                opacity: 0.6;
            }
            50% {
                opacity: 1;
            }
            100% {
                opacity: 0.6;
            }
        }
        
        .loading {
            animation: pulse 1.5s infinite;
            text-align: center;
            padding: 20px;
        }
        
        /* Hide excessive debug output */
        .stDebug {
            display: none;
        }
    </style>
    """, unsafe_allow_html=True)

def render_sidebar():
    """Render the sidebar content."""
    with st.sidebar:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("## How to use YouClip")
        st.write("1. Enter a YouTube URL")
        st.write("2. Set start and end times for your clip")
        st.write("3. Choose video format and quality")
        st.write("4. Click 'Generate Clip' and download")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.write("## About YouClip")
        st.write("YouClip is a powerful tool that allows you to create custom clips from YouTube videos. It's perfect for creating highlights, sharing specific parts of videos, or extracting content for your projects.")
        
        # Features section
        st.markdown("""
        <div class="features-container">
            <div class="feature-card">
                <div class="feature-icon">⚡</div>
                <div>Fast Processing</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🎨</div>
                <div>Multiple Formats</div>
            </div>
            <div class="feature-card">
                <div class="feature-icon">🔄</div>
                <div>Quality Options</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

def render_footer():
    """Render the footer content."""
    st.markdown("""
    <div class="footer">
        <p>YouClip - Create beautiful clips from YouTube videos with ease.</p>
        <p>© 2025 YouClip</p>
    </div>
    """, unsafe_allow_html=True)