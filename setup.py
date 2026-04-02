"""Setup script that triggers rickroll during pip install."""

import subprocess
import sys
import tempfile
import webbrowser
from pathlib import Path
from setuptools import setup
from setuptools.command.install import install
from setuptools.command.develop import develop
from setuptools.command.egg_info import egg_info


def rickroll():
    """Never gonna give you up!"""
    url = "https://www.youtube.com/watch?v=dQw4w9WgXcQ"
    
    print("\n" + "=" * 60)
    print("🎵 You just got rickrolled! 🎵")
    print("=" * 60)
    print("\nThis is an educational demonstration about PyPI security.")
    print("When you ran 'pip install', this package executed code on your system.")
    print("\nLesson: Always verify packages before installing them!")
    print("=" * 60 + "\n")
    
    if not play_video_directly(url):
        print("Falling back to browser...")
        try:
            webbrowser.open(url)
        except Exception:
            print(f"Open this URL: {url}")


def play_video_directly(url):
    """Download and play the video using yt-dlp and pygame."""
    try:
        import yt_dlp
        import pygame
    except ImportError:
        return False
    
    try:
        with tempfile.TemporaryDirectory() as tmpdir:
            video_path = Path(tmpdir) / "rickroll.mp4"
            
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
                return False
            
            print("Playing video... Close the window to continue.")
            play_video_with_pygame(str(video_path))
            return True
            
    except Exception as e:
        print(f"Direct playback failed: {e}")
        return False


def play_video_with_pygame(video_path):
    """Play video using pygame's movie module or ffmpeg fallback."""
    import pygame
    
    try:
        pygame.init()
        pygame.mixer.quit()
        
        # Try using pygame with moviepy as a backend
        try:
            from moviepy.editor import VideoFileClip
            
            clip = VideoFileClip(video_path)
            
            screen = pygame.display.set_mode(clip.size)
            pygame.display.set_caption("🎵 Never Gonna Give You Up 🎵")
            
            clip.preview()
            clip.close()
            return
        except ImportError:
            pass
        
        # Fallback: use system default video player
        open_with_system_player(video_path)
        
    except Exception as e:
        print(f"Pygame playback failed: {e}")
        open_with_system_player(video_path)
    finally:
        pygame.quit()


def open_with_system_player(video_path):
    """Open video with system default player."""
    import platform
    import shutil
    
    # Copy to a location that won't be deleted immediately
    persistent_path = Path(tempfile.gettempdir()) / "rickroll_surprise.mp4"
    shutil.copy2(video_path, persistent_path)
    
    system = platform.system()
    try:
        if system == "Darwin":
            subprocess.Popen(["open", str(persistent_path)])
        elif system == "Windows":
            subprocess.Popen(["start", "", str(persistent_path)], shell=True)
        else:
            subprocess.Popen(["xdg-open", str(persistent_path)])
        print(f"Video opened in system player.")
    except Exception as e:
        print(f"Could not open video: {e}")


class RickrollInstall(install):
    def run(self):
        rickroll()
        install.run(self)


class RickrollDevelop(develop):
    def run(self):
        rickroll()
        develop.run(self)


class RickrollEggInfo(egg_info):
    def run(self):
        rickroll()
        egg_info.run(self)


setup(
    cmdclass={
        'install': RickrollInstall,
    },
)
