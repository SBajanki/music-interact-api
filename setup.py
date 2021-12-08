from setuptools import setup

setup(
    name='Avg words in lyrics',
    version=1.0,
    description='Avg words in lyrics',
    author='Sirisha Bajanki',
    author_email='bssiri@gmail.com',
    packages=['musicapi'],
    scripts=['lyricsavgwordcount.py'],
    install_requires=['requests'],
    python_requires='~=3.6',
)
