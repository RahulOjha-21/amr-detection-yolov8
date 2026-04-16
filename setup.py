"""
Setup configuration for AMR Detection System.

This package provides tools for detecting and analyzing Antimicrobial Resistance (AMR)
using YOLOv8 object detection and computer vision techniques.
"""

from setuptools import setup, find_packages
import os

# Read long description from README
with open("README_NEW.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Read requirements from requirements.txt (filter out comments and empty lines)
def get_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as f:
        requirements = []
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith("#"):
                requirements.append(line)
        return requirements

setup(
    name="amr-detection",
    version="1.0.0",
    author="Rahul Ojha",
    author_email="your.email@example.com",
    description="Real-time AMR Detection System using YOLOv8 and Computer Vision",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/amr-detection",
    packages=find_packages(include=["src", "src.*"]),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Healthcare Industry",
        "Intended Audience :: Science/Research",
        "Topic :: Scientific/Engineering :: Artificial Intelligence",
        "Topic :: Scientific/Engineering :: Medical Science Apps.",
        "Topic :: Multimedia :: Graphics :: Viewers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8",
    install_requires=get_requirements(),
    entry_points={
        "console_scripts": [
            "amr-detect=src.streaming.app:main",
        ],
    },
    include_package_data=True,
    project_urls={
        "Bug Reports": "https://github.com/yourusername/amr-detection/issues",
        "Source Code": "https://github.com/yourusername/amr-detection",
        "Documentation": "https://github.com/yourusername/amr-detection#usage",
    },
)
