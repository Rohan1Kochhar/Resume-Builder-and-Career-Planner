import requests
import json
import os
from datetime import datetime

class GitHubAPIClient:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        self.client_id = client_id or os.getenv('GITHUB_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('GITHUB_CLIENT_SECRET')
        self.redirect_uri = redirect_uri or os.getenv('GITHUB_REDIRECT_URI', 'http://localhost:5000/github-callback')
        self.api_base_url = 'https://api.github.com'
        self.auth_base_url = 'https://github.com/login/oauth'
    
    def get_authorization_url(self, state=None):
        """Generate GitHub OAuth authorization URL"""
        params = {
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'read:user user:email',
            'state': state or 'github_auth'
        }
        return f"{self.auth_base_url}/authorize?{self._build_query_string(params)}"
    
    def exchange_code_for_token(self, authorization_code):
        """Exchange authorization code for access token"""
        url = f"{self.auth_base_url}/access_token"
        headers = {
            'Accept': 'application/json',
            'Content-Type': 'application/json'
        }
        data = {
            'client_id': self.client_id,
            'client_secret': self.client_secret,
            'code': authorization_code,
            'redirect_uri': self.redirect_uri
        }
        
        response = requests.post(url, headers=headers, json=data)
        if response.status_code == 200:
            token_data = response.json()
            return token_data.get('access_token')
        else:
            raise Exception(f"Failed to exchange code for token: {response.text}")
    
    def get_profile_data(self, username=None, access_token=None):
        """Fetch GitHub profile data"""
        if not access_token:
            raise Exception("Access token is required")
        
        headers = {
            'Authorization': f'token {access_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        # Get user profile
        if username:
            user_url = f"{self.api_base_url}/users/{username}"
        else:
            user_url = f"{self.api_base_url}/user"
        
        user_response = requests.get(user_url, headers=headers)
        if user_response.status_code != 200:
            raise Exception(f"Failed to fetch user data: {user_response.text}")
        
        user_data = user_response.json()
        
        # Get repositories
        repos_url = f"{self.api_base_url}/users/{user_data['login']}/repos"
        repos_response = requests.get(repos_url, headers=headers)
        repos_data = repos_response.json() if repos_response.status_code == 200 else []
        
        # Get languages from top repositories
        languages = self._extract_languages(repos_data)
        
        return self._format_profile_data(user_data, repos_data, languages)
    
    def _extract_languages(self, repos_data):
        """Extract programming languages from repositories"""
        languages = {}
        for repo in repos_data[:10]:  # Top 10 repos
            if repo.get('language'):
                lang = repo['language']
                languages[lang] = languages.get(lang, 0) + 1
        
        # Sort by frequency
        sorted_languages = sorted(languages.items(), key=lambda x: x[1], reverse=True)
        return [lang for lang, count in sorted_languages[:10]]  # Top 10 languages
    
    def _format_profile_data(self, user_data, repos_data, languages):
        """Format GitHub data into resume format"""
        return {
            'name': user_data.get('name', user_data.get('login', '')),
            'headline': user_data.get('bio', 'Software Developer'),
            'location': user_data.get('location', ''),
            'email': user_data.get('email', ''),
            'phone': '',  # GitHub doesn't provide phone
            'summary': user_data.get('bio', ''),
            'experience': self._format_repositories_as_experience(repos_data),
            'education': [],  # GitHub doesn't provide education data
            'skills': languages,
            'certifications': [],
            'achievements': self._format_achievements(user_data, repos_data)
        }
    
    def _format_repositories_as_experience(self, repos_data):
        """Format repositories as work experience"""
        experience = []
        for repo in repos_data[:5]:  # Top 5 repositories
            if repo.get('description'):
                exp = {
                    'title': f"Project: {repo['name']}",
                    'company': 'GitHub',
                    'location': repo.get('language', ''),
                    'duration': f"Created: {repo['created_at'][:10]}",
                    'description': repo['description']
                }
                experience.append(exp)
        return experience
    
    def _format_achievements(self, user_data, repos_data):
        """Format GitHub achievements"""
        achievements = []
        
        # Repository count
        if repos_data:
            achievements.append(f"Created {len(repos_data)} repositories")
        
        # Followers
        if user_data.get('followers'):
            achievements.append(f"{user_data['followers']} followers")
        
        # Account age
        if user_data.get('created_at'):
            created_date = datetime.strptime(user_data['created_at'][:10], '%Y-%m-%d')
            years_active = (datetime.now() - created_date).days // 365
            if years_active > 0:
                achievements.append(f"Active GitHub user for {years_active} years")
        
        # Top repositories by stars
        starred_repos = sorted(repos_data, key=lambda x: x.get('stargazers_count', 0), reverse=True)
        if starred_repos and starred_repos[0].get('stargazers_count', 0) > 0:
            top_repo = starred_repos[0]
            achievements.append(f"Top repository: {top_repo['name']} ({top_repo['stargazers_count']} stars)")
        
        return achievements
    
    def _build_query_string(self, params):
        """Build query string from parameters"""
        return '&'.join([f"{k}={v}" for k, v in params.items() if v])

class GitHubProfileParser:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        self.api_client = GitHubAPIClient(client_id, client_secret, redirect_uri)
    
    def parse_profile(self, github_url, access_token=None):
        """Parse GitHub profile and return formatted data"""
        try:
            if access_token:
                # Extract username from URL
                username = self._extract_username_from_url(github_url)
                if username:
                    return self.api_client.get_profile_data(username, access_token)
                else:
                    return self.api_client.get_profile_data(access_token=access_token)
            else:
                # Return mock data for demo
                return self._get_mock_profile_data()
        except Exception as e:
            print(f"Error parsing GitHub profile: {e}")
            return self._get_mock_profile_data()
    
    def _extract_username_from_url(self, github_url):
        """Extract username from GitHub URL"""
        if not github_url:
            return None
        
        # Handle different GitHub URL formats
        if 'github.com' in github_url:
            parts = github_url.split('github.com/')
            if len(parts) > 1:
                username = parts[1].split('/')[0]
                return username
        
        return None
    
    def _get_mock_profile_data(self):
        """Return mock GitHub profile data for demo"""
        return {
            'name': 'John Doe',
            'headline': 'Full Stack Developer',
            'location': 'San Francisco, CA',
            'email': 'john.doe@example.com',
            'phone': '+1 (555) 123-4567',
            'summary': 'Passionate full-stack developer with 5+ years of experience in web development, specializing in React, Node.js, and Python. Open source contributor and tech enthusiast.',
            'experience': [
                {
                    'title': 'Project: E-commerce Platform',
                    'company': 'GitHub',
                    'location': 'React, Node.js',
                    'duration': 'Created: 2023-01-15',
                    'description': 'A full-stack e-commerce platform with React frontend and Node.js backend, featuring user authentication, payment processing, and admin dashboard.'
                },
                {
                    'title': 'Project: Task Management App',
                    'company': 'GitHub',
                    'location': 'Python, Django',
                    'duration': 'Created: 2022-08-20',
                    'description': 'A collaborative task management application built with Django and PostgreSQL, featuring real-time updates and team collaboration features.'
                },
                {
                    'title': 'Project: Weather API',
                    'company': 'GitHub',
                    'location': 'JavaScript, Express',
                    'duration': 'Created: 2022-05-10',
                    'description': 'RESTful weather API service built with Express.js, integrating with multiple weather data providers and featuring caching mechanisms.'
                }
            ],
            'education': [],
            'skills': ['JavaScript', 'Python', 'React', 'Node.js', 'Django', 'PostgreSQL', 'MongoDB', 'Git', 'Docker', 'AWS'],
            'certifications': [],
            'achievements': [
                'Created 25+ repositories',
                '150+ followers',
                'Active GitHub user for 3 years',
                'Top repository: ecommerce-platform (45 stars)'
            ]
        } 