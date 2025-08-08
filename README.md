# LinkedIn Resume Builder

A professional web application that transforms LinkedIn profiles into polished, downloadable resumes. Built with Flask, Python, and modern web technologies.

## Features

- **LinkedIn Profile Integration**: Extract professional information from LinkedIn profiles
- **Multiple Resume Templates**: Choose from Modern, Classic, and Minimal designs
- **Professional Formatting**: Generate Word documents (.docx) with proper formatting
- **Real-time Preview**: See extracted information before generating the resume
- **Responsive Design**: Works seamlessly on desktop and mobile devices
- **Easy Download**: One-click download of generated resumes

## Screenshots

The application features a clean, modern interface with:
- LinkedIn-themed color scheme
- Step-by-step workflow
- Real-time profile preview
- Professional resume templates

## Installation

### Prerequisites

- Python 3.7 or higher
- pip (Python package installer)
- Modern web browser

### Setup Instructions

1. **Clone or download the project**
   ```bash
   # If using git
   git clone <repository-url>
   cd resume-builder
   
   # Or simply navigate to the project directory
   cd resume-builder
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your web browser
   - Navigate to `http://localhost:5000`
   - The application will be ready to use!

## Usage

### Step 1: Enter LinkedIn Profile
1. Enter your LinkedIn profile URL in the input field
2. Select your preferred resume template (Modern, Classic, or Minimal)
3. Click "Parse LinkedIn Profile"

### Step 2: Preview & Generate
1. Review the extracted profile information
2. Make any necessary edits (if needed)
3. Click "Generate Resume" to create your professional resume

### Step 3: Download
1. Once generated, click "Download Resume"
2. Your resume will be downloaded as a Word document (.docx)

## Templates Available

### Modern Template
- Clean, contemporary design
- Professional typography
- Balanced white space
- Ideal for tech and creative industries

### Classic Template
- Traditional business format
- Times New Roman font
- Formal layout
- Perfect for corporate environments

### Minimal Template
- Simple, clean design
- Arial font
- Compact layout
- Great for quick applications

## Technical Details

### Backend Technologies
- **Flask**: Web framework for Python
- **python-docx**: Word document generation
- **BeautifulSoup**: HTML parsing (for LinkedIn integration)
- **Selenium**: Web scraping capabilities
- **Requests**: HTTP library for API calls

### Frontend Technologies
- **Bootstrap 5**: Responsive CSS framework
- **Font Awesome**: Icon library
- **Vanilla JavaScript**: Frontend functionality
- **HTML5/CSS3**: Modern web standards

### Project Structure
```
resume-builder/
├── app.py                 # Main Flask application
├── linkedin_parser.py     # LinkedIn profile parsing
├── resume_generator.py    # Resume generation logic
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── templates/
│   └── index.html        # Main web interface
├── static/
│   ├── css/
│   │   └── style.css     # Custom styles
│   └── js/
│       └── script.js     # Frontend JavaScript
└── generated_resumes/    # Output directory for resumes
```

## API Endpoints

### POST /upload-linkedin
Extract profile data from LinkedIn URL
```json
{
  "linkedin_url": "https://linkedin.com/in/username"
}
```

### POST /generate-resume
Generate resume from profile data
```json
{
  "profile_data": {...},
  "template": "modern"
}
```

### GET /download/<filename>
Download generated resume file

## Configuration

### Environment Variables
- `SECRET_KEY`: Flask secret key for session management
- `LINKEDIN_API_KEY`: LinkedIn API credentials (for production)

### Customization
- Modify `resume_generator.py` to add new templates
- Update `linkedin_parser.py` for different data extraction methods
- Customize styles in `static/css/style.css`

## Production Deployment

### Security Considerations
1. **LinkedIn API Integration**: Use official LinkedIn API instead of web scraping
2. **Rate Limiting**: Implement proper rate limiting for API calls
3. **Input Validation**: Validate all user inputs
4. **File Security**: Secure file uploads and downloads

### Deployment Options
- **Heroku**: Easy deployment with Procfile
- **AWS**: EC2 with Elastic Beanstalk
- **Google Cloud**: App Engine deployment
- **Docker**: Containerized deployment

### Environment Setup
```bash
# Set environment variables
export FLASK_ENV=production
export SECRET_KEY=your-secret-key-here

# Install production dependencies
pip install gunicorn
```

## Limitations & Notes

### Current Implementation
- Uses mock data for demonstration purposes
- LinkedIn scraping requires proper authentication
- Limited to basic profile information

### Production Requirements
- LinkedIn API access and credentials
- Proper error handling and logging
- Database for user management
- File storage solution
- SSL/TLS encryption

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:
- Create an issue in the repository
- Check the documentation
- Review the code comments

## Future Enhancements

- [ ] LinkedIn API integration
- [ ] More resume templates
- [ ] PDF export option
- [ ] Cover letter generation
- [ ] Resume analytics
- [ ] Multi-language support
- [ ] Cloud storage integration
- [ ] User accounts and history

## Acknowledgments

- LinkedIn for professional networking platform
- Flask community for the web framework
- Bootstrap team for the CSS framework
- Font Awesome for the icon library

---

**Note**: This is a demonstration application. For production use, ensure compliance with LinkedIn's terms of service and implement proper security measures. 
