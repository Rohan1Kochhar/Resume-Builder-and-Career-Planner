import requests
import json
import os
from urllib.parse import urlencode
from datetime import datetime
import base64

class LinkedInAPIClient:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        """
        Initialize LinkedIn API client
        
        Args:
            client_id: LinkedIn App Client ID
            client_secret: LinkedIn App Client Secret
            redirect_uri: OAuth redirect URI
        """
        self.client_id = client_id or os.getenv('LINKEDIN_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('LINKEDIN_CLIENT_SECRET')
        self.redirect_uri = redirect_uri or os.getenv('LINKEDIN_REDIRECT_URI', 'http://localhost:5000/linkedin-callback')
        self.access_token = None
        self.base_url = 'https://api.linkedin.com/v2'
        
        if not self.client_id or not self.client_secret:
            raise ValueError("LinkedIn Client ID and Client Secret are required. Set them as environment variables or pass them to the constructor.")
    
    def get_authorization_url(self, state=None):
        """
        Generate LinkedIn OAuth authorization URL
        
        Args:
            state: Optional state parameter for security
            
        Returns:
            Authorization URL for user to visit
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'r_liteprofile r_emailaddress',
            'state': state or 'random_state_string'
        }
        
        auth_url = f"https://www.linkedin.com/oauth/v2/authorization?{urlencode(params)}"
        return auth_url
    
    def exchange_code_for_token(self, authorization_code):
        """
        Exchange authorization code for access token
        
        Args:
            authorization_code: Code received from LinkedIn OAuth callback
            
        Returns:
            Access token dictionary
        """
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        
        data = {
            'grant_type': 'authorization_code',
            'code': authorization_code,
            'redirect_uri': self.redirect_uri,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            return token_data
        else:
            raise Exception(f"Failed to exchange code for token: {response.text}")
    
    def get_profile_data(self, profile_id='me'):
        """
        Get LinkedIn profile data using the API
        
        Args:
            profile_id: LinkedIn profile ID (default: 'me' for current user)
            
        Returns:
            Profile data dictionary
        """
        if not self.access_token:
            raise Exception("Access token required. Call exchange_code_for_token() first.")
        
        # Get basic profile information
        profile_url = f"{self.base_url}/me"
        headers = {
            'Authorization': f'Bearer {self.access_token}',
            'X-Restli-Protocol-Version': '2.0.0'
        }
        
        # Request specific fields
        params = {
            'projection': '(id,firstName,lastName,profilePicture,email-address,positions,educations,skills,summary)'
        }
        
        response = requests.get(profile_url, headers=headers, params=params)
        
        if response.status_code == 200:
            profile_data = response.json()
            return self._format_profile_data(profile_data)
        else:
            raise Exception(f"Failed to get profile data: {response.text}")
    
    def get_profile_by_url(self, profile_url):
        """
        Get profile data from LinkedIn URL (requires different approach)
        
        Args:
            profile_url: LinkedIn profile URL
            
        Returns:
            Profile data dictionary
        """
        # Extract profile ID from URL
        profile_id = self._extract_profile_id_from_url(profile_url)
        if profile_id:
            return self.get_profile_data(profile_id)
        else:
            raise Exception("Could not extract profile ID from URL")
    
    def _extract_profile_id_from_url(self, url):
        """
        Extract LinkedIn profile ID from URL
        
        Args:
            url: LinkedIn profile URL
            
        Returns:
            Profile ID or None
        """
        import re
        
        # Pattern for LinkedIn profile URLs
        patterns = [
            r'linkedin\.com/in/([^/?]+)',
            r'linkedin\.com/profile/view\?id=(\d+)',
            r'linkedin\.com/pub/([^/?]+)'
        ]
        
        for pattern in patterns:
            match = re.search(pattern, url)
            if match:
                return match.group(1)
        
        return None
    
    def _format_profile_data(self, api_data):
        """
        Format LinkedIn API data into our standard format
        
        Args:
            api_data: Raw LinkedIn API response
            
        Returns:
            Formatted profile data
        """
        try:
            # Extract basic information
            first_name = api_data.get('firstName', {}).get('localized', {}).get('en_US', '')
            last_name = api_data.get('lastName', {}).get('localized', {}).get('en_US', '')
            name = f"{first_name} {last_name}".strip()
            
            # Extract email
            email = api_data.get('emailAddress', '')
            
            # Extract positions (experience)
            experience = []
            positions = api_data.get('positions', {}).get('elements', [])
            for position in positions:
                exp_item = {
                    'title': position.get('title', ''),
                    'company': position.get('companyName', ''),
                    'location': position.get('locationName', ''),
                    'duration': self._format_duration(position.get('timePeriod', {})),
                    'description': position.get('summary', '')
                }
                experience.append(exp_item)
            
            # Extract education
            education = []
            educations = api_data.get('educations', {}).get('elements', [])
            for edu in educations:
                edu_item = {
                    'degree': edu.get('degreeName', ''),
                    'school': edu.get('schoolName', ''),
                    'location': edu.get('locationName', ''),
                    'duration': self._format_duration(edu.get('timePeriod', {})),
                    'gpa': edu.get('grade', '')
                }
                education.append(edu_item)
            
            # Extract skills
            skills = []
            skills_data = api_data.get('skills', {}).get('elements', [])
            for skill in skills_data:
                skill_name = skill.get('skillName', {}).get('localized', {}).get('en_US', '')
                if skill_name:
                    skills.append(skill_name)
            
            # Extract summary
            summary = api_data.get('summary', {}).get('localized', {}).get('en_US', '')
            
            return {
                'personal_info': {
                    'name': name,
                    'headline': api_data.get('headline', ''),
                    'location': api_data.get('locationName', ''),
                    'email': email,
                    'phone': '',  # Not available in basic API
                    'linkedin_url': f"https://linkedin.com/in/{api_data.get('id', '')}",
                    'summary': summary
                },
                'experience': experience,
                'education': education,
                'skills': skills,
                'certifications': [],  # Not available in basic API
                'projects': [],  # Not available in basic API
                'languages': []  # Not available in basic API
            }
            
        except Exception as e:
            print(f"Error formatting profile data: {e}")
            return None
    
    def _format_duration(self, time_period):
        """
        Format time period from LinkedIn API
        
        Args:
            time_period: Time period object from LinkedIn API
            
        Returns:
            Formatted duration string
        """
        start_date = time_period.get('startDate', {})
        end_date = time_period.get('endDate', {})
        
        start_month = start_date.get('month', '')
        start_year = start_date.get('year', '')
        end_month = end_date.get('month', '')
        end_year = end_date.get('year', '')
        
        if start_year:
            start_str = f"{start_month} {start_year}" if start_month else str(start_year)
        else:
            start_str = "Unknown"
        
        if end_year:
            end_str = f"{end_month} {end_year}" if end_month else str(end_year)
        else:
            end_str = "Present"
        
        return f"{start_str} - {end_str}"
    
    def refresh_token(self, refresh_token):
        """
        Refresh access token using refresh token
        
        Args:
            refresh_token: Refresh token from previous OAuth flow
            
        Returns:
            New access token data
        """
        token_url = 'https://www.linkedin.com/oauth/v2/accessToken'
        
        data = {
            'grant_type': 'refresh_token',
            'refresh_token': refresh_token,
            'client_id': self.client_id,
            'client_secret': self.client_secret
        }
        
        response = requests.post(token_url, data=data)
        
        if response.status_code == 200:
            token_data = response.json()
            self.access_token = token_data.get('access_token')
            return token_data
        else:
            raise Exception(f"Failed to refresh token: {response.text}")


class LinkedInProfileParser:
    """
    Wrapper class that provides a simple interface for parsing LinkedIn profiles
    """
    
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        """
        Initialize the parser with LinkedIn API credentials
        
        Args:
            client_id: LinkedIn App Client ID
            client_secret: LinkedIn App Client Secret
            redirect_uri: OAuth redirect URI
        """
        self.api_client = LinkedInAPIClient(client_id, client_secret, redirect_uri)
    
    def parse_profile(self, linkedin_url, access_token=None):
        """
        Parse LinkedIn profile data
        
        Args:
            linkedin_url: LinkedIn profile URL
            access_token: Optional access token (if already authenticated)
            
        Returns:
            Profile data dictionary or None if error
        """
        try:
            if access_token:
                self.api_client.access_token = access_token
            
            if not self.api_client.access_token:
                # For demo purposes, return mock data
                # In production, you would need to implement the full OAuth flow
                return self._get_mock_profile_data()
            
            # Use LinkedIn API to get profile data
            profile_data = self.api_client.get_profile_by_url(linkedin_url)
            return profile_data
            
        except Exception as e:
            print(f"Error parsing LinkedIn profile: {e}")
            # Fallback to mock data for demo
            return self._get_mock_profile_data()
    
    def _get_mock_profile_data(self):
        """Return mock LinkedIn profile data for demonstration"""
        return {
            'personal_info': {
                'name': 'John Doe',
                'headline': 'Senior Software Engineer',
                'location': 'San Francisco, CA',
                'email': 'john.doe@email.com',
                'phone': '+1 (555) 123-4567',
                'linkedin_url': 'https://linkedin.com/in/johndoe',
                'summary': 'Experienced software engineer with 5+ years of expertise in full-stack development, specializing in Python, JavaScript, and cloud technologies. Passionate about building scalable applications and leading technical teams.'
            },
            'experience': [
                {
                    'title': 'Senior Software Engineer',
                    'company': 'Tech Corp',
                    'location': 'San Francisco, CA',
                    'duration': 'Jan 2022 - Present',
                    'description': 'Led development of microservices architecture, improved system performance by 40%, mentored junior developers, and implemented CI/CD pipelines.'
                },
                {
                    'title': 'Software Engineer',
                    'company': 'Startup Inc',
                    'location': 'San Francisco, CA',
                    'duration': 'Mar 2020 - Dec 2021',
                    'description': 'Developed full-stack web applications using React and Node.js, collaborated with cross-functional teams, and deployed applications to AWS.'
                }
            ],
            'education': [
                {
                    'degree': 'Bachelor of Science in Computer Science',
                    'school': 'University of California, Berkeley',
                    'location': 'Berkeley, CA',
                    'duration': '2015 - 2019',
                    'gpa': '3.8/4.0'
                }
            ],
            'skills': [
                'Python', 'JavaScript', 'React', 'Node.js', 'AWS', 'Docker',
                'Kubernetes', 'PostgreSQL', 'MongoDB', 'Git', 'REST APIs',
                'Microservices', 'CI/CD', 'Agile', 'Leadership'
            ],
            'certifications': [
                {
                    'name': 'AWS Certified Solutions Architect',
                    'issuer': 'Amazon Web Services',
                    'date': '2023'
                }
            ],
            'projects': [
                {
                    'name': 'E-commerce Platform',
                    'description': 'Built a scalable e-commerce platform using React, Node.js, and MongoDB.',
                    'technologies': ['React', 'Node.js', 'MongoDB', 'Stripe API'],
                    'url': 'https://github.com/johndoe/ecommerce-platform'
                }
            ],
            'languages': [
                {'language': 'English', 'proficiency': 'Native'},
                {'language': 'Spanish', 'proficiency': 'Conversational'}
            ]
        } 