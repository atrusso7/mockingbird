from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import JSONFormatter

def extract_transcript(video_url):
    try:
        # Extract the video ID from the URL
        if 'youtube.com' in video_url:
            video_id = video_url.split('v=')[-1].split('&')[0]
        elif 'youtu.be' in video_url:
            video_id = video_url.split('/')[-1]
        else:
            return "Error: Invalid YouTube URL format"

        # Get the transcript
        transcript = YouTubeTranscriptApi.get_transcript(video_id)
        full_transcript = ' '.join([t['text'] for t in transcript])
        return full_transcript
    except Exception as e:
        return f"Error extracting transcript: {e}"

if __name__ == "__main__":
    # Test the function
    video_url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"  # Replace with any video URL for testing
    print(extract_transcript(video_url))
