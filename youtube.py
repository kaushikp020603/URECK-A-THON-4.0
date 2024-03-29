import streamlit as st
import googleapiclient.discovery
from IPython.display import YouTubeVideo

# Function to fetch video recommendations from YouTube Data API
def fetch_video_recommendations(query, max_results=5):
    youtube = googleapiclient.discovery.build("youtube", "v3", developerKey="AIzaSyC-HokJ01cwFv-8FPLzoZ0ji6ZM23rkAqQ")
    request = youtube.search().list(
        part="snippet",
        q=query,
        type="video",
        maxResults=max_results
    )
    response = request.execute()
    return response.get("items", [])

# Streamlit app
st.title("YouTube Video Recommender")

# Sidebar for user input
search_query = st.text_input("Enter a search query or video ID:")
if st.button("Search"):
    # Fetch video recommendations
    videos = fetch_video_recommendations(search_query)
    
    # Display recommendations
    if videos:
        st.subheader("Recommended Videos:")
        for video in videos:
            title = video["snippet"]["title"]
            video_id = video["id"]["videoId"]
            thumbnail_url = video["snippet"]["thumbnails"]["medium"]["url"]
            
            # Display video preview
            st.write(f"Title: {title}")
            st.write(f"Video ID: {video_id}")
            st.image(thumbnail_url, caption=title, use_column_width=True)
            
            # Embed video preview
            st.subheader("Video Preview:")
            YouTubeVideo(video_id)
            
            # Hyperlink to open video on YouTube
            st.markdown(f"[Watch '{title}' on YouTube](https://www.youtube.com/watch?v={video_id})")
            
            st.write("---")
    else:
        st.write("No videos found.")
