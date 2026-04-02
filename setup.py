"""Setup script that triggers rickroll during pip install."""

import subprocess
import sys
import tempfile
import webbrowser
import threading
import time
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


def show_popup_message(title, message):
    """Display a popup message dialog to the user.
    
    Args:
        title: The window title for the popup.
        message: The message text to display.
    """
    import platform
    system = platform.system()
    
    try:
        if system == "Darwin":
            # macOS: use osascript
            script = f'display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK"'
            subprocess.Popen(["osascript", "-e", script])
        elif system == "Windows":
            # Windows: use PowerShell
            ps_script = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("{message}", "{title}")'
            subprocess.Popen(["powershell", "-Command", ps_script])
        else:
            # Linux: try zenity, then kdialog, then xmessage
            for cmd in [
                ["zenity", "--info", f"--title={title}", f"--text={message}"],
                ["kdialog", "--msgbox", message, "--title", title],
                ["xmessage", "-center", f"{title}\n\n{message}"],
            ]:
                try:
                    subprocess.Popen(cmd)
                    return
                except FileNotFoundError:
                    continue
            print(f"\n[POPUP] {title}: {message}\n")
    except Exception as e:
        print(f"\n[POPUP] {title}: {message}\n")


def show_security_warning_after_delay(delay_seconds=3):
    """Show the security warning popup after a delay.
    
    Args:
        delay_seconds: Number of seconds to wait before showing the popup.
    """
    def delayed_popup():
        time.sleep(delay_seconds)
        show_popup_message(
            "⚠️ Security Warning ⚠️",
            "You just got rickrolled!\\n\\n"
            "This is an educational demonstration about PyPI security.\\n\\n"
            "When you ran 'pip install', this package executed arbitrary code "
            "on your system - including downloading and playing a video!\\n\\n"
            "LESSON: Always verify packages before installing them!\\n"
            "Check the source code, verify the publisher, and be cautious "
            "with unfamiliar packages."
        )
    
    thread = threading.Thread(target=delayed_popup, daemon=True)
    thread.start()
    return thread


def rickroll(with_audio=False):
    """Never gonna give you up!
    
    Args:
        with_audio: If True, play video with audio. Default is False (muted).
    """
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("\n" + "=" * 60)
    print("🎵 You just got rickrolled! 🎵")
    print("=" * 60)
    print("\nThis is an educational demonstration about PyPI security.")
    print("When you ran 'pip install', this package executed code on your system.")
    print("\nLesson: Always verify packages before installing them!")
    print("=" * 60 + "\n")
    
    # Start the delayed security popup
    popup_thread = show_security_warning_after_delay(delay_seconds=3)
    
    if not play_video_directly(url, with_audio=with_audio):
        print("Falling back to browser...")
        try:
            webbrowser.open(url)
        except Exception:
            print(f"Open this URL: {url}")


def play_video_directly(url, with_audio=False):
    """Download and play the video using yt-dlp in the background.
    
    Args:
        url: The YouTube URL to download and play.
        with_audio: If True, play with audio. Default is False (muted).
    
    Returns:
        True if video playback was started, False otherwise.
    """
    try:
        import yt_dlp
    except ImportError:
        return False
    
    def download_and_play():
        try:
            # Use a persistent temp directory for the video
            tmpdir = Path(tempfile.gettempdir()) / "rickroll_tmp"
            tmpdir.mkdir(exist_ok=True)
            video_path = tmpdir / "rickroll.mp4"
            
            ydl_opts = {
                'format': 'best[ext=mp4][height<=720]/best[ext=mp4]/best',
                'outtmpl': str(video_path),
                'quiet': True,
                'no_warnings': True,
            }
            
            print("Downloading surprise content...")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            if not video_path.exists():
                return
            
            print("Playing video in background... (installation will continue)")
            play_video_background(str(video_path), with_audio=with_audio)
            
        except Exception as e:
            print(f"Direct playback failed: {e}")
            try:
                webbrowser.open(url)
            except Exception:
                pass
    
    # Start download and playback in a background thread
    thread = threading.Thread(target=download_and_play, daemon=True)
    thread.start()
    
    # Give it a moment to start
    time.sleep(0.5)
    return True


def play_video_background(video_path, with_audio=False):
    """Play video in the background using system player.
    
    Args:
        video_path: Path to the video file.
        with_audio: If True, play with audio. Default is False (muted).
    """
    import platform
    import shutil
    
    # Copy to a persistent location
    persistent_path = Path(tempfile.gettempdir()) / "rickroll_surprise.mp4"
    if Path(video_path) != persistent_path:
        shutil.copy2(video_path, persistent_path)
    
    system = platform.system()
    
    try:
        if system == "Darwin":
            # macOS: use afplay for audio control, open for video
            if with_audio:
                subprocess.Popen(["open", str(persistent_path)])
            else:
                # Use QuickTime with AppleScript to mute
                script = f'''
                tell application "QuickTime Player"
                    open POSIX file "{persistent_path}"
                    set audio volume of document 1 to 0
                    play document 1
                end tell
                '''
                try:
                    subprocess.Popen(["osascript", "-e", script])
                except Exception:
                    subprocess.Popen(["open", str(persistent_path)])
        elif system == "Windows":
            if with_audio:
                subprocess.Popen(["start", "", str(persistent_path)], shell=True)
            else:
                # Try to use VLC with volume 0, fallback to default player
                try:
                    subprocess.Popen(["vlc", "--volume=0", str(persistent_path)])
                except FileNotFoundError:
                    subprocess.Popen(["start", "", str(persistent_path)], shell=True)
        else:
            # Linux: try various players with mute options
            if with_audio:
                subprocess.Popen(["xdg-open", str(persistent_path)])
            else:
                players = [
                    ["vlc", "--volume=0", str(persistent_path)],
                    ["mpv", "--volume=0", str(persistent_path)],
                    ["totem", str(persistent_path)],  # GNOME Videos (no easy mute flag)
                    ["xdg-open", str(persistent_path)],
                ]
                for player_cmd in players:
                    try:
                        subprocess.Popen(player_cmd)
                        print(f"Video opened with {player_cmd[0]}.")
                        return
                    except FileNotFoundError:
                        continue
                print(f"Could not find a video player. Video saved at: {persistent_path}")
                return
        
        print(f"Video opened in system player.")
    except Exception as e:
        print(f"Could not open video: {e}")


class RickrollInstall(install):
    def run(self):
        rickroll(with_audio=False)
        install.run(self)


class RickrollDevelop(develop):
    def run(self):
        rickroll(with_audio=False)
        develop.run(self)


class RickrollEggInfo(egg_info):
    def run(self):
        rickroll(with_audio=False)
        egg_info.run(self)


setup(
    cmdclass={
        'install': RickrollInstall,
    },
)
