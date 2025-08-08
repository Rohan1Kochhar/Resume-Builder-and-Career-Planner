# Quick Start Guide - LinkedIn Resume Builder

## 🚀 Get Started in 3 Easy Steps

### Option 1: Demo Version (No Installation Required)
1. **Open the demo file**: Double-click `demo.html` in your file explorer
2. **Test the interface**: Enter any LinkedIn URL and see the demo in action
3. **Download sample resume**: Generate and download a sample resume

### Option 2: Full Version with Python

#### Prerequisites
- Python 3.7 or higher installed on your system
- Internet connection for downloading dependencies

#### Installation Steps

1. **Install Python Dependencies**
   ```bash
   # Windows
   setup.bat
   
   # Or manually
   python -m pip install -r requirements.txt
   ```

2. **Run the Application**
   ```bash
   # Full Flask version
   python app.py
   
   # Or simple demo version
   python simple_app.py
   ```

3. **Access the Application**
   - Open your web browser
   - Go to: `http://localhost:5000` (Flask) or `http://localhost:8000` (Simple)
   - Start building your resume!

## 📁 Project Structure

```
resume-builder/
├── app.py                 # Main Flask application
├── simple_app.py          # Simple demo server
├── demo.html              # Standalone demo file
├── setup.bat              # Windows setup script
├── run_demo.bat           # Demo runner
├── requirements.txt       # Python dependencies
├── README.md             # Full documentation
├── QUICK_START.md        # This file
├── templates/
│   └── index.html        # Web interface
├── static/
│   ├── css/style.css     # Custom styles
│   └── js/script.js      # Frontend logic
└── generated_resumes/    # Output directory
```

## 🎯 Features Overview

### ✅ What Works Now
- **Modern Web Interface**: Beautiful, responsive design
- **Multiple Templates**: Modern, Classic, and Minimal styles
- **Profile Preview**: See extracted information before generating
- **Download Functionality**: Get your resume as a text file
- **Demo Mode**: Test with sample data

### 🔄 What's Coming (Production Features)
- **Real LinkedIn Integration**: Actual profile scraping
- **Word Document Export**: Professional .docx files
- **PDF Export**: High-quality PDF resumes
- **User Accounts**: Save and manage multiple resumes
- **Custom Templates**: Create your own designs

## 🛠️ Troubleshooting

### Python Not Found
- **Solution**: Install Python from https://python.org
- **Make sure**: Check "Add Python to PATH" during installation

### Dependencies Installation Failed
- **Solution**: Run `python -m pip install --upgrade pip` first
- **Alternative**: Use the demo version (`demo.html`)

### Port Already in Use
- **Solution**: Change the port in the code or stop other services
- **Alternative**: Use the simple demo version

### Browser Issues
- **Solution**: Use a modern browser (Chrome, Firefox, Safari, Edge)
- **Check**: JavaScript is enabled

## 📞 Support

### Quick Help
1. **Demo Issues**: Open `demo.html` directly in browser
2. **Python Issues**: Check Python installation with `python --version`
3. **Dependencies**: Run `setup.bat` for automatic setup

### File Descriptions
- `demo.html` - Standalone demo (works without server)
- `simple_app.py` - Basic Python server (minimal dependencies)
- `app.py` - Full Flask application (requires all dependencies)
- `setup.bat` - Automatic setup script for Windows

## 🎉 Success!

Once you have the application running, you can:
1. Enter any LinkedIn URL (demo uses sample data)
2. Choose your preferred template
3. Preview the extracted information
4. Generate and download your resume

The application is designed to be user-friendly and professional, making resume creation quick and easy! 