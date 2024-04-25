import os
import pytube
import msvcrt
from colorama import init, Fore, Style


init()

def clear_screen():
    """Clears the terminal screen."""
    os.system('cls' if os.name == 'nt' else 'clear')

def download_video(yt, resolution='720p'):
    """Downloads the YouTube video with the specified resolution."""
    stream = yt.streams.filter(res=resolution, progressive=True).first()
    if stream:
        stream.download()
        print("Video downloaded successfully!")
    else:
        print(f"No video stream found for resolution {resolution}.")

def download_audio(yt):
    """Downloads the audio of the YouTube video."""
    stream = yt.streams.filter(only_audio=True).first()
    if stream:
        stream.download(filename_prefix='audio_')
        print("Audio downloaded successfully!")
    else:
        print("No audio stream found.")

def show_menu(options, current_option):
    """Displays the menu options."""
    clear_screen()
    print(Fore.GREEN + "╔════════════════════════╗")
    print("║   Welcome to YouTube   ║")
    print("║    Video Downloader!   ║")
    print("║    By CranFused-Real   ║")
    print("╚════════════════════════╝" + Style.RESET_ALL)
    print()
    print("Use the arrow keys to navigate and press Enter to select:")
    for idx, option in enumerate(options):
        if idx == current_option:
            print(Fore.GREEN + "►", option + Style.RESET_ALL)
        else:
            print("  ", option)

def get_input():
    """Get keyboard input."""
    while True:
        key = msvcrt.getch()
        if key == b'\xe0':  # Arrow keys are represented by b'\xe0' followed by the actual key code
            key = msvcrt.getch()
            if key == b'H':  # UP arrow
                return "UP"
            elif key == b'P':  # DOWN arrow
                return "DOWN"
        elif key in [b'\r', b'\n']:  # Enter
            return "ENTER"

def main():
    """Main function to run the program."""
    options = ["Download Video (MP4)", "Download Audio (MP3)", "Exit"]
    current_option = 0

    while True:
        show_menu(options, current_option)

        key = get_input()

        if key == "UP":
            current_option = (current_option - 1) % len(options)
        elif key == "DOWN":
            current_option = (current_option + 1) % len(options)
        elif key == "ENTER":
            clear_screen()
            if current_option == 0:
                video_url = input("Enter the YouTube video URL: ")
                try:
                    yt = pytube.YouTube(video_url)
                except pytube.exceptions.VideoUnavailable:
                    print("The provided video is not available.")
                    continue
                print("\nAvailable Resolutions:")
                for stream in yt.streams.filter(progressive=True):
                    print(stream)
                resolution = input("\nEnter desired resolution for video (e.g., 720p): ").strip()
                download_video(yt, resolution)
                input("\nPress Enter to continue...")
            elif current_option == 1:
                video_url = input("Enter the YouTube video URL: ")
                try:
                    yt = pytube.YouTube(video_url)
                except pytube.exceptions.VideoUnavailable:
                    print("The provided video is not available.")
                    continue
                download_audio(yt)
                input("\nPress Enter to continue...")
            elif current_option == 2:
                print("Exiting...")
                break

if __name__ == "__main__":
    main()
