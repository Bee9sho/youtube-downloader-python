from pytube import YouTube
import os

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def list_resolutions(youtube):
    """ 
    
    list availabe resolutions only """
    streams = youtube.streams.filter(progressive = True).order_by('resolution').desc()
    available_resolutions = [stream.resolution for stream in streams]
    unique_resolutions = sorted(set(available_resolutions), key=available_resolutions.index)
    return unique_resolutions


def download_video(youtube, resolution, download_directory, log_file_path):
    video = youtube.streams.filter(res=resolution, progressive=True).first()
    if video:
        output_path = video.download(output_path=download_directory)
        print(f'Downloaded: {youtube.title} in {resolution} to {download_directory}')
        
        # Log download details
        with open(log_file_path, 'a', encoding=' utf-8') as log_file:
            log_file.write(f"Title: {youtube.title}\nURL: {youtube.watch_url}\nResolution: {resolution}\nDownload Path: {output_path}\n\n")
    else:
        print(f"Resolution {resolution} not available.")

def main():
    download_directory = input("Enter the download directory path: ")
    log_file_name = input("Enter the log file name (e.g., download_log.txt): ")
    log_file_path = os.path.join(download_directory, log_file_name)
    ensure_dir(download_directory)

    while True:
        video_url = input("Enter the YouTube video URL (or 'exit' to quit): ")
        if video_url.lower() == "exit":
            break

        try:
            youtube = YouTube(video_url)
            print(f"Video title: {youtube.title}\n")
            resolutions = list_resolutions(youtube)
            print("Available resolutions:", ", ".join(resolutions))
            resolution_choice = input("Enter desired resolution (e.g., 720p): ")
            download_video(youtube, resolution_choice, download_directory, log_file_path)

        except Exception as e:
            print(f'An error occurred: {e}')



if __name__ == "__main__":
    main()