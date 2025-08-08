import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class for the LinkedIn Resume Builder"""
    
    # Flask Configuration
    SECRET_KEY = os.getenv('SECRET_KEY', 'your-secret-key-here')
    DEBUG = os.getenv('DEBUG', 'True').lower() == 'true'
    
    # LinkedIn API Configuration
    LINKEDIN_CLIENT_ID = os.getenv('LINKEDIN_CLIENT_ID')
    LINKEDIN_CLIENT_SECRET = os.getenv('LINKEDIN_CLIENT_SECRET')
    LINKEDIN_REDIRECT_URI = os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:5000/linkedin-callback')
    
    # LinkedIn API Scopes
    LINKEDIN_SCOPES = [
        'r_liteprofile',      # Read basic profile information
        'r_emailaddress',     # Read email address
        'w_member_social'     # Write posts and comments
    ]
    
    # GitHub API Configuration
    GITHUB_CLIENT_ID = os.getenv('GITHUB_CLIENT_ID')
    GITHUB_CLIENT_SECRET = os.getenv('GITHUB_CLIENT_SECRET')
    GITHUB_REDIRECT_URI = os.getenv('GITHUB_REDIRECT_URI', 'http://localhost:5000/github-callback')
    
    # GitHub API Scopes
    GITHUB_SCOPES = [
        'read:user',          # Read user profile information
        'user:email'          # Read user email addresses
    ]
    
    # Application Settings
    UPLOAD_FOLDER = 'generated_resumes'
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    
    # Resume Templates
    AVAILABLE_TEMPLATES = ['modern', 'classic', 'minimal']
    DEFAULT_TEMPLATE = 'modern'
    
    @classmethod
    def is_linkedin_configured(cls):
        """Check if LinkedIn API is properly configured"""
        return bool(cls.LINKEDIN_CLIENT_ID and cls.LINKEDIN_CLIENT_SECRET)
    
    @classmethod
    def is_github_configured(cls):
        """Check if GitHub API is properly configured"""
        return bool(cls.GITHUB_CLIENT_ID and cls.GITHUB_CLIENT_SECRET)
    
    @classmethod
    def get_linkedin_scopes_string(cls):
        """Get LinkedIn scopes as a space-separated string"""
        return ' '.join(cls.LINKEDIN_SCOPES)
    
    @classmethod
    def get_github_scopes_string(cls):
        """Get GitHub scopes as a space-separated string"""
        return ' '.join(cls.GITHUB_SCOPES) 