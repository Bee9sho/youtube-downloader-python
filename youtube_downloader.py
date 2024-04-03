import os
from pytube import YouTube, Playlist

def ensure_directory(directory_path):
    if not os.path.exists(directory_path):
        os.makedirs(directory_path)

def get_available_resolutions(youtube):
    streams = youtube.streams.filter(progressive=True).order_by('resolution').desc()
    available_resolutions = [stream.resolution for stream in streams]
    unique_resolutions = sorted(set(available_resolutions), key=available_resolutions.index)
    return unique_resolutions

def download_video_with_resolution(youtube, resolution, download_directory, log_file_path):
    if resolution is None:
        # auto choose the heighest reso
        video_stream = youtube.streams.filter(progressive=True).order_by('resolution').desc().first()
    else:
        video_stream = youtube.streams.filter(res=resolution, progressive=True).first()
    
    if video_stream:
        output_path = video_stream.download(output_path=download_directory)
        print(f'Downloaded: {youtube.title} in {video_stream.resolution} to {download_directory}')

        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f"Title: {youtube.title}\nURL: {youtube.watch_url}\nResolution: {video_stream.resolution}\nDownload Path: {output_path}\n\n")
    else:
        print(f'Resolution {resolution} not available.')

    
def parse_resolution_input(input_str):
    if 'p' in input_str:
        return int(input_str.replace('p', ''))
    else:
        return int(input_str)

def download_single_video(youtube, download_directory, log_file_path):
    resolutions = get_available_resolutions(youtube)
    print("Available resolutions:", ", ".join(resolutions))
    resolution_choice = input("Enter desired resolution (e.g., 720p): ")
    resolution = f"{parse_resolution_input(resolution_choice)}p"
    download_video_with_resolution(youtube, resolution, download_directory, log_file_path)

def download_entire_playlist(playlist_url, download_directory, log_file_path):
    playlist = Playlist(playlist_url)
    print(f'Downloading playlist: {playlist.title}')
    for video in playlist.videos:
        try:
            # Ensure the resolution argument is provided correctly, set to None for highest resolution
            download_video_with_resolution(video, None, download_directory, log_file_path)
        except Exception as e:
            print(f'An error occurred while downloading video from the playlist: {e}')

def download_audio_only(youtube, download_directory, log_file_path):
    audio_stream = youtube.streams.filter(only_audio=True).first()
    if audio_stream:
        output_path = audio_stream.download(output_path=download_directory)
        print(f'Downloaded: {youtube.title} (Audio) to {download_directory}')

        with open(log_file_path, 'a', encoding='utf-8') as log_file:
            log_file.write(f'Title: {youtube.title}\nURL: {youtube.watch_url}\nType: MP3\nDownload Path: {output_path}\n\n')
    else:
        print("MP3 audio download not available for this video.")

def download_youtube_video():
    download_directory = input("Enter the download directory path: ")
    log_file_name = input("Enter the log file name (e.g., download_log.txt): ")
    log_file_path = os.path.join(download_directory, log_file_name)
    ensure_directory(download_directory)

    while True:
        video_url = input("Enter the YouTube video URL (or 'exit' to quit): ")
        if video_url.lower() == "exit":
            break

        try:
            if "playlist?list=" in video_url:
                download_entire_playlist(video_url, download_directory, log_file_path)
            else:
                youtube = YouTube(video_url)
                print(f"Video title: {youtube.title}\n")
                download_type = input("Choose download type: Enter '1' for single video, '2' for entire playlist, or '3' for MP3 audio: ")
                if download_type == '1':
                    download_single_video(youtube, download_directory, log_file_path)
                elif download_type == '3':
                    download_audio_only(youtube, download_directory, log_file_path)
                else:
                    print("Invalid choice. Please enter '1' for a single video or '3' for MP3 audio.")

        except Exception as e:
            print(f'An error occurred: {e}')

if __name__ == "__main__":
    download_youtube_video()
