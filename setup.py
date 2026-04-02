"""Setup script that triggers rickroll during pip install."""

import webbrowser
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
    try:
        webbrowser.open(url)
    except Exception:
        print(f"Open this URL: {url}")


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
        'develop': RickrollDevelop,
        'egg_info': RickrollEggInfo,
    },
)
