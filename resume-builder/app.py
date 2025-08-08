from flask import Flask, render_template, request, jsonify, send_file, redirect, url_for, session
import json
import os
from datetime import datetime
from resume_generator import ResumeGenerator
from linkedin_api_client import LinkedInProfileParser, LinkedInAPIClient
from github_api_client import GitHubProfileParser, GitHubAPIClient
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# Debug print for GitHub API config
print('GITHUB_CLIENT_ID:', Config.GITHUB_CLIENT_ID)
print('GITHUB_CLIENT_SECRET:', Config.GITHUB_CLIENT_SECRET)
print('GITHUB_REDIRECT_URI:', Config.GITHUB_REDIRECT_URI)

# Initialize LinkedIn API client
linkedin_client = None
if Config.is_linkedin_configured():
    linkedin_client = LinkedInAPIClient(
        Config.LINKEDIN_CLIENT_ID, 
        Config.LINKEDIN_CLIENT_SECRET, 
        Config.LINKEDIN_REDIRECT_URI
    )

# Initialize GitHub API client
github_client = None
if Config.is_github_configured():
    github_client = GitHubAPIClient(
        Config.GITHUB_CLIENT_ID, 
        Config.GITHUB_CLIENT_SECRET, 
        Config.GITHUB_REDIRECT_URI
    )

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/linkedin-auth')
def linkedin_auth():
    """Initiate LinkedIn OAuth flow"""
    if not linkedin_client:
        return jsonify({'error': 'LinkedIn API not configured'}), 500
    
    try:
        auth_url = linkedin_client.get_authorization_url()
        return redirect(auth_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/linkedin-callback')
def linkedin_callback():
    """Handle LinkedIn OAuth callback"""
    if not linkedin_client:
        return jsonify({'error': 'LinkedIn API not configured'}), 500
    
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return jsonify({'error': f'LinkedIn authorization failed: {error}'}), 400
        
        if not code:
            return jsonify({'error': 'Authorization code not received'}), 400
        
        # Exchange code for access token
        token_data = linkedin_client.exchange_code_for_token(code)
        
        # Store token in session
        session['linkedin_access_token'] = token_data.get('access_token')
        session['linkedin_refresh_token'] = token_data.get('refresh_token')
        
        return redirect(url_for('index'))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check-linkedin-auth')
def check_linkedin_auth():
    """Check if user is authenticated with LinkedIn"""
    try:
        access_token = session.get('linkedin_access_token')
        if access_token:
            return jsonify({'authenticated': True})
        else:
            return jsonify({'authenticated': False})
    except Exception as e:
        return jsonify({'authenticated': False, 'error': str(e)})

@app.route('/upload-linkedin', methods=['POST'])
def upload_linkedin():
    try:
        data = request.get_json()
        linkedin_url = data.get('linkedin_url')
        use_api = data.get('use_api', False)
        
        if not linkedin_url:
            return jsonify({'error': 'LinkedIn URL is required'}), 400
        
        # Initialize parser
        parser = LinkedInProfileParser(Config.LINKEDIN_CLIENT_ID, Config.LINKEDIN_CLIENT_SECRET, Config.LINKEDIN_REDIRECT_URI)
        
        # Get access token from session if available
        access_token = session.get('linkedin_access_token') if use_api else None
        
        # Parse LinkedIn profile
        profile_data = parser.parse_profile(linkedin_url, access_token)
        
        if not profile_data:
            return jsonify({'error': 'Could not parse LinkedIn profile'}), 400
        
        return jsonify({
            'success': True,
            'profile_data': profile_data,
            'api_used': use_api and access_token is not None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# GitHub OAuth Routes
@app.route('/github-auth')
def github_auth():
    """Initiate GitHub OAuth flow"""
    if not github_client:
        return jsonify({'error': 'GitHub API not configured'}), 500
    
    try:
        auth_url = github_client.get_authorization_url()
        return redirect(auth_url)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/github-callback')
def github_callback():
    """Handle GitHub OAuth callback"""
    if not github_client:
        return jsonify({'error': 'GitHub API not configured'}), 500
    
    try:
        code = request.args.get('code')
        state = request.args.get('state')
        error = request.args.get('error')
        
        if error:
            return jsonify({'error': f'GitHub authorization failed: {error}'}), 400
        
        if not code:
            return jsonify({'error': 'Authorization code not received'}), 400
        
        # Exchange code for access token
        access_token = github_client.exchange_code_for_token(code)
        
        # Store token in session
        session['github_access_token'] = access_token
        
        return redirect(url_for('index'))
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/check-github-auth')
def check_github_auth():
    """Check if user is authenticated with GitHub"""
    try:
        access_token = session.get('github_access_token')
        if access_token:
            return jsonify({'authenticated': True})
        else:
            return jsonify({'authenticated': False})
    except Exception as e:
        return jsonify({'authenticated': False, 'error': str(e)})

@app.route('/upload-github', methods=['POST'])
def upload_github():
    try:
        data = request.get_json()
        github_url = data.get('github_url')
        use_api = data.get('use_api', False)
        
        if not github_url:
            return jsonify({'error': 'GitHub URL is required'}), 400
        
        # Initialize parser
        parser = GitHubProfileParser(Config.GITHUB_CLIENT_ID, Config.GITHUB_CLIENT_SECRET, Config.GITHUB_REDIRECT_URI)
        
        # Get access token from session if available
        access_token = session.get('github_access_token') if use_api else None
        
        # Parse GitHub profile
        profile_data = parser.parse_profile(github_url, access_token)
        
        print(profile_data)
        if not profile_data:
            return jsonify({'error': 'Could not parse GitHub profile'}), 400
        
        return jsonify({
            'success': True,
            'profile_data': profile_data,
            'api_used': use_api and access_token is not None
        })
    
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/generate-resume', methods=['POST'])
def generate_resume():
    try:
        data = request.get_json()
        profile_data = data.get('profile_data')
        template = data.get('template', 'modern')
        format = data.get('format', 'docx')
        if not profile_data:
            return jsonify({'error': 'Profile data is required'}), 400
        if isinstance(profile_data, dict):
            if 'personal_info' in profile_data:
                linkedin_format = {
                    'name': profile_data['personal_info'].get('name', ''),
                    'headline': profile_data['personal_info'].get('headline', ''),
                    'location': profile_data['personal_info'].get('location', ''),
                    'email': profile_data['personal_info'].get('email', ''),
                    'phone': profile_data['personal_info'].get('phone', ''),
                    'summary': profile_data['personal_info'].get('summary', ''),
                    'experience': profile_data.get('experience', []),
                    'education': profile_data.get('education', []),
                    'skills': profile_data.get('skills', []),
                    'certifications': profile_data.get('certifications', []),
                    'achievements': profile_data.get('achievements', [])
                }
                profile_data = linkedin_format
        generator = ResumeGenerator()
        filename = generator.generate_resume(profile_data, template, format)
        if not filename:
            return jsonify({'error': 'Failed to generate resume'}), 500
        return jsonify({
            'success': True,
            'filename': filename
        })
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/download-resume/<filename>')
def download_resume(filename):
    try:
        file_path = os.path.join('generated_resumes', filename)
        if os.path.exists(file_path):
            return send_file(file_path, as_attachment=True)
        else:
            return jsonify({'error': 'File not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/suggest-jobs', methods=['POST'])
def suggest_jobs():
    try:
        data = request.get_json()
        profile_data = data.get('profile_data', {})
        keywords = []
        # Use job title from most recent experience if available
        experience = profile_data.get('experience', [])
        if experience and isinstance(experience, list):
            job_title = experience[0].get('title', '')
            if job_title:
                keywords.append(job_title)
        # Add skills
        skills = profile_data.get('skills', [])
        if skills and isinstance(skills, list):
            keywords.extend(skills[:3])
        # Fallback to headline
        headline = profile_data.get('headline', '')
        if headline:
            keywords.append(headline)
        query = ' '.join(keywords) or 'developer'
        api_url = f'https://remotive.com/api/remote-jobs?search={query}'
        import requests
        resp = requests.get(api_url)
        jobs = []
        if resp.status_code == 200:
            results = resp.json().get('jobs', [])
            for job in results[:10]:
                jobs.append({
                    'title': job.get('title'),
                    'company': job.get('company_name'),
                    'location': job.get('candidate_required_location'),
                    'url': job.get('url'),
                    'description': job.get('description', '')[:200] + '...'
                })
        return jsonify({'jobs': jobs})
    except Exception as e:
        return jsonify({'jobs': [], 'error': str(e)})

@app.route('/job-search', methods=['POST'])
def job_search():
    try:
        data = request.get_json()
        skills = data.get('skills', '').lower()
        experience = data.get('experience', '')
        location = data.get('location', '').lower()
        job_type = data.get('jobType', '').lower()
        import requests
        # Build Remotive API query
        query = skills or ''
        remotive_url = f'https://remotive.com/api/remote-jobs?search={query}'
        resp = requests.get(remotive_url)
        jobs = []
        if resp.status_code == 200:
            all_jobs = resp.json().get('jobs', [])
            for job in all_jobs:
                # Filter by location if provided
                if location and location not in job.get('candidate_required_location', '').lower():
                    continue
                # Filter by job type (Remotive uses 'job_type' field: 'full_time', 'part_time', 'contract', etc.)
                if job_type:
                    jt = job.get('job_type', '').lower()
                    if job_type == 'remote' and 'remote' not in jt:
                        continue
                    if job_type == 'onsite' and 'remote' in jt:
                        continue
                    if job_type == 'hybrid' and 'hybrid' not in jt:
                        continue
                jobs.append({
                    'title': job.get('title'),
                    'company': job.get('company_name'),
                    'location': job.get('candidate_required_location'),
                    'type': job.get('job_type'),
                    'description': job.get('description', '')[:200] + '...',
                    'url': job.get('url'),
                    'logo': job.get('company_logo_url'),
                    'salary': job.get('salary'),
                    'category': job.get('category')
                })
        return jsonify({'jobs': jobs[:18]})
    except Exception as e:
        return jsonify({'jobs': [], 'error': str(e)})

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('generated_resumes', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    app.run(debug=True, host='0.0.0.0', port=8080) 