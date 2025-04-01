import streamlit as st
import pytube
import yt_dlp
import re
import os
import time

@st.cache_data
def get_video_info(url):
    try:
        # Clean the URL to ensure proper format
        if "youtu.be" in url:
            video_id = url.split("/")[-1].split("?")[0]
            url = f"https://www.youtube.com/watch?v={video_id}"
        elif "youtube.com" in url:
            # Extract video ID using regex to handle any YouTube URL format
            pattern = r'(?:v=|\/)([0-9A-Za-z_-]{11}).*'
            match = re.search(pattern, url)
            if match:
                video_id = match.group(1)
                url = f"https://www.youtube.com/watch?v={video_id}"
        
        # First try with pytube
        try:
            # Create YouTube object with additional options to bypass some restrictions
            yt = pytube.YouTube(
                url,
                use_oauth=False,
                allow_oauth_cache=True
            )
            
            # Test if we can access title
            title = yt.title
                
            return {
                "title": yt.title,
                "thumbnail": yt.thumbnail_url,
                "length": yt.length,
                "author": yt.author,
                "publish_date": yt.publish_date,
                "views": yt.views,
                "yt_object": yt,
                "source": "pytube"
            }
        except Exception as pytube_error:
            st.warning(f"Initial method failed, trying alternative...")
            
            # Fallback to yt-dlp
            ydl_opts = {
                'quiet': True,
                'no_warnings': True,
                'skip_download': True,
                'format': 'best',
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=False)
                
            if info:
                video_info = {
                    "title": info.get('title', 'Unknown Title'),
                    "thumbnail": info.get('thumbnail', ''),
                    "length": info.get('duration', 0),
                    "author": info.get('uploader', 'Unknown'),
                    "publish_date": None,  # yt-dlp stores date differently
                    "views": info.get('view_count', 0),
                    "yt_object": None,  # We'll handle this differently
                    "yt_dlp_info": info,  # Store the yt-dlp info for later use
                    "source": "yt-dlp"
                }
                st.success("Video information retrieved successfully!")
                return video_info
            else:
                raise Exception("Failed to retrieve video information")
                
    except Exception as e:
        st.error(f"Error fetching video info: {str(e)}")
        
        # Provide a more detailed error message and suggestions
        st.markdown("""
        <div style="background-color: #382121; padding: 15px; border-radius: 5px; margin-top: 10px;">
            <h4 style="color: #ff6b6b; margin-top: 0;">Troubleshooting Tips:</h4>
            <ul>
                <li>Make sure the video isn't private or age-restricted</li>
                <li>Try copying the URL directly from YouTube's address bar</li>
                <li>Check your internet connection</li>
                <li>YouTube occasionally blocks automated requests - try again in a few minutes</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        return None

def download_video(video_info, url, output_dir):
    """Download the video using the appropriate method based on the source."""
    try:
        if video_info.get("source") == "pytube" and video_info.get("yt_object"):
            # Download using pytube
            stream = video_info["yt_object"].streams.filter(progressive=True).order_by('resolution').desc().first()
            
            # If no progressive stream is available, try adaptive streams
            if not stream:
                st.info("Using adaptive streams. This might take longer...")
                stream = video_info["yt_object"].streams.filter(adaptive=True, file_extension="mp4").order_by('resolution').desc().first()
            
            # Last resort - try any available stream
            if not stream:
                stream = video_info["yt_object"].streams.first()
                
            # Add timeout for download to prevent hanging
            download_path = stream.download(output_path=output_dir, timeout=180)
            return download_path
            
        elif video_info.get("source") == "yt-dlp" and video_info.get("yt_dlp_info"):
            # Download using yt-dlp
            st.info("Using enhanced downloader. This might take a moment...")
            
            # Create a unique filename for the downloaded video
            timestamp = int(time.time())
            safe_title = re.sub(r'[^\w\-_]', '_', video_info["title"])
            safe_title = safe_title[:50] if len(safe_title) > 50 else safe_title
            filename = f"{safe_title}_{timestamp}.mp4"
            filepath = os.path.join(output_dir, filename)
            
            # Configure yt-dlp options for downloading
            ydl_opts = {
                'format': 'bestvideo[height<=720][ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': filepath,
                'quiet': True,
                'no_warnings': True,
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            return filepath
        else:
            raise Exception("No valid video source found")
    except Exception as e:
        st.error(f"Error downloading video: {str(e)}")
        st.markdown("""
        <div style="background-color: #382121; padding: 15px; border-radius: 5px; margin-top: 10px;">
            <h4 style="color: #ff6b6b; margin-top: 0;">Download Failed</h4>
            <p>YouTube may be blocking this download. This can happen due to:</p>
            <ul>
                <li>Video restrictions (age-restricted, private, or copyrighted content)</li>
                <li>YouTube's anti-scraping protections</li>
                <li>Regional restrictions on the video</li>
            </ul>
            <p>Try a different video or try again later.</p>
        </div>
        """, unsafe_allow_html=True)
        return None