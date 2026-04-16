# Contributing to AMR Detection System

First off, thank you for considering contributing to the AMR Detection System! It's people like you that make this project such a great tool.

## Code of Conduct

This project and everyone participating in it is governed by our Code of Conduct. By participating, you are expected to uphold this code.

## How Can I Contribute?

### Reporting Bugs

Before creating bug reports, please check the issue list as you might find out that you don't need to create one.

**How Do I Submit A (Good) Bug Report?**

Bugs are tracked as GitHub issues. When creating a bug report, include as many details as possible:

* **Use a clear and descriptive title**
* **Describe the exact steps which reproduce the problem**
* **Provide specific examples to demonstrate the steps**
* **Describe the behavior you observed after following the steps**
* **Explain which behavior you expected to see instead and why**
* **Include your OS, Python version, and environment details**
* **Include error messages or logs**

### Suggesting Enhancements

Enhancement suggestions are tracked as GitHub issues. When creating an enhancement suggestion, please include:

* **Use a clear and descriptive title**
* **Provide a step-by-step description of the suggested enhancement**
* **Provide specific examples to demonstrate the steps**
* **Describe the current behavior and expected behavior**
* **Explain why this enhancement would be useful**

### Pull Requests

* Fill in the required template
* Follow the Python styleguides
* Include appropriate test cases
* Document new code with docstrings
* Update relevant documentation

## Development Setup

### Prerequisites
- Python 3.8+
- pip or conda
- Git

### Setup Steps

1. **Fork and Clone the Repository**
   ```bash
   git clone https://github.com/yourusername/amr-detection.git
   cd amr-detection
   ```

2. **Create a Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Development Dependencies**
   ```bash
   pip install -r requirements.txt
   pip install -e .
   ```

4. **Create a Feature Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

## Styleguides

### Python Code Style

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) guidelines.

**Key Points:**
- Use 4 spaces for indentation
- Maximum line length: 88 characters
- Use meaningful variable and function names
- Write docstrings for public functions and classes

**Example:**
```python
def extract_frames_from_video(
    video_path: str,
    output_folder: str,
    frame_interval: int = 1
) -> int:
    """
    Extract frames from a video file and save them as images.
    
    Args:
        video_path: Path to the input video file.
        output_folder: Directory to save extracted frames.
        frame_interval: Extract every nth frame (default: 1).
    
    Returns:
        Number of frames successfully extracted.
    
    Raises:
        FileNotFoundError: If video file doesn't exist.
        IOError: If unable to write frames.
    """
```

### Commit Messages

* Use the present tense ("Add feature" not "Added feature")
* Use the imperative mood ("Move cursor to..." not "Moves cursor to...")
* Limit the first line to 50 characters or less
* Reference issues and pull requests liberally after the first line

**Example:**
```
Add real-time detection for IP cameras

- Implement RTSP stream support
- Add stream URL validation
- Include error handling for connection failures

Fixes #234
```

### Documentation

* Use clear and concise language
* Include code examples where applicable
* Update README.md if you add new features
* Add docstrings to all public functions and classes

## Workflow

1. **Make Your Changes**
   - Write clean, well-documented code
   - Test your changes thoroughly
   - Follow the styleguide

2. **Test Your Code**
   ```bash
   # Run any existing tests
   pytest tests/
   ```

3. **Commit and Push**
   ```bash
   git add .
   git commit -m "Your descriptive commit message"
   git push origin feature/your-feature-name
   ```

4. **Create a Pull Request**
   - Provide a clear description of changes
   - Reference any related issues
   - Wait for feedback and make requested changes

## Code Review Process

* At least one maintainer will review your PR
* We may request changes before merging
* Once approved, your code will be merged

## Project Structure

```
src/
├── __init__.py
├── config.py              # Configuration management
├── constants.py           # Application constants
├── data_labeling/         # Data preparation tools
│   ├── __init__.py
│   ├── image_labeling.py
│   ├── video_labeling.py
│   ├── dataset_split.py
│   └── remove_duplicates.py
└── streaming/             # Real-time detection
    ├── __init__.py
    ├── app.py            # Main application
    ├── model.py          # Model utilities
    └── utils.py          # Helper utilities
```

## Adding New Features

### Data Processing Tools
- Add your script to `src/data_labeling/`
- Include proper error handling and logging
- Add docstrings with usage examples

### Detection Features
- Add utility functions to `src/streaming/utils.py`
- Update the Streamlit app in `src/streaming/app.py`
- Test with various input sources

### Core Changes
1. Always add tests
2. Update documentation
3. Update requirements.txt if adding dependencies

## Reporting Security Issues

**Please do not file a public issue for security vulnerabilities.** Instead, email security concerns directly to the maintainers.

## Additional Notes

### Project Philosophy

* Keep it simple and intuitive
* Prioritize code quality over quantity
* Document thoroughly
* Test comprehensively
* Value user experience

### Common Tasks

**Adding a New Dependency:**
1. Install the package: `pip install package_name`
2. Add to requirements.txt with version: `package_name==version`
3. Update setup.py if needed
4. Create a commit with changes

**Creating Tests:**
1. Create file in `tests/` directory
2. Use descriptive test names
3. Test edge cases and errors
4. Keep tests independent

**Updating Documentation:**
1. Edit relevant .md files
2. Keep examples up-to-date
3. Check for broken links
4. Ensure code examples work

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- Project acknowledgments

## Questions?

Feel free to open an issue or contact the maintainers directly.

---

**Thank you for contributing to AMR Detection System! 🎉**
