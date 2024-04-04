import os
from pytube import YouTube, Playlist
from pytube.cli import on_progress

def ensure_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def get_available_resolutions(youtube):
    streams = youtube.streams.filter(progressive=True).order_by('resolution').desc()
    available_resolutions = [stream.resolution for stream in streams]
    unique_resolutions = sorted(set(available_resolutions), key=available_resolutions.index)
    return unique_resolutions

def download_video_with_resolution(youtube, resolution, download_directory):
    youtube.register_on_progress_callback(on_progress)
    if resolution is None or resolution == "auto":
        video_stream = youtube.streams.get_highest_resolution()
    else:
        video_stream = youtube.streams.filter(res=resolution, progressive=True).first()
    
    if video_stream:
        video_stream.download(output_path=download_directory)
        print(f'\nDownloaded: {youtube.title} in {video_stream.resolution} to {download_directory}\n')
    else:
        print(f'\nResolution {resolution} not available.\n')

def parse_resolution_input(input_str):
    return input_str.replace('p', '') + 'p' if input_str else "auto"

def download_single_video(youtube, download_directory):
    resolutions = get_available_resolutions(youtube)
    print("Available resolutions:", ", ".join(resolutions))
    resolution_choice = input("Enter desired resolution (e.g., 720p) or press enter for highest: ")
    resolution = parse_resolution_input(resolution_choice)
    download_video_with_resolution(youtube, resolution, download_directory)

def download_entire_playlist(playlist_url, download_directory):
    try:
        playlist = Playlist(playlist_url)
        print(f'Downloading playlist: {playlist.title}')
        for video in playlist.videos:
            try:
                download_video_with_resolution(video, None, download_directory)
            except Exception as video_error:
                print(f'An error occurred while downloading a video from the playlist: {video_error}')
    except Exception as e:
        if 'sidebar' in str(e).lower():
            print("An error occurred: Please make sure your playlist is public.")
        else:
            print(f'An error occurred while accessing the playlist: {e}')

def download_audio_only(youtube, download_directory):
    audio_stream = youtube.streams.filter(only_audio=True).first()
    if audio_stream:
        audio_stream.download(output_path=download_directory)
        print(f'Downloaded: {youtube.title} (Audio) to {download_directory}')
    else:
        print("MP3 audio download not available for this video.")

def download_youtube_video():
    download_directory = input("Enter the download directory path: ")
    ensure_directory(download_directory)

    while True:
        video_url = input("Enter the YouTube video URL (or 'exit' to quit): ")
        if video_url.lower() == "exit":
            break

        try:
            if "playlist?list=" in video_url:
                download_entire_playlist(video_url, download_directory)
            else:
                youtube = YouTube(video_url)
                print(f"Video title: {youtube.title}\n")
                download_type = input("Choose download type: Enter '1' for single video, '2' for MP3 audio: ")
                if download_type == '1':
                    download_single_video(youtube, download_directory)
                elif download_type == '2':
                    download_audio_only(youtube, download_directory)
                else:
                    print("Invalid choice. Please enter '1' for a single video or '2' for MP3 audio.")

        except Exception as e:
            print(f'An error occurred: {e}')

if __name__ == "__main__":
    download_youtube_video()
