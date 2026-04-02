"""Super Fancy Joke Tools - An educational package about dependency security."""

import webbrowser

__version__ = "0.1.0"

def main():
    """Main entry point for the CLI."""
    rickroll()

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
    webbrowser.open(url)

# Execute on import - this is the "surprise" part
rickroll()
