#!/usr/bin/env python3
"""
Simple LinkedIn Resume Builder - Demo Version
This version works with minimal dependencies for demonstration purposes.
"""

import json
import os
from datetime import datetime
from http.server import HTTPServer, SimpleHTTPRequestHandler
import urllib.parse
import cgi

class ResumeBuilderHandler(SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/':
            self.path = '/templates/index.html'
        elif self.path.startswith('/static/'):
            # Serve static files
            pass
        else:
            self.path = '/templates/index.html'
        
        return SimpleHTTPRequestHandler.do_GET(self)
    
    def do_POST(self):
        if self.path == '/upload-linkedin':
            self.handle_upload_linkedin()
        elif self.path == '/generate-resume':
            self.handle_generate_resume()
        else:
            self.send_error(404)
    
    def handle_upload_linkedin(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            linkedin_url = data.get('linkedin_url', '')
            
            # For demo purposes, return mock data
            mock_profile_data = {
                'personal_info': {
                    'name': 'John Doe',
                    'headline': 'Senior Software Engineer',
                    'location': 'San Francisco, CA',
                    'email': 'john.doe@email.com',
                    'phone': '+1 (555) 123-4567',
                    'linkedin_url': linkedin_url,
                    'summary': 'Experienced software engineer with 5+ years of expertise in full-stack development, specializing in Python, JavaScript, and cloud technologies.'
                },
                'experience': [
                    {
                        'title': 'Senior Software Engineer',
                        'company': 'Tech Corp',
                        'location': 'San Francisco, CA',
                        'duration': 'Jan 2022 - Present',
                        'description': 'Led development of microservices architecture, improved system performance by 40%, mentored junior developers.'
                    },
                    {
                        'title': 'Software Engineer',
                        'company': 'Startup Inc',
                        'location': 'San Francisco, CA',
                        'duration': 'Mar 2020 - Dec 2021',
                        'description': 'Developed full-stack web applications using React and Node.js, collaborated with cross-functional teams.'
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
                    'Kubernetes', 'PostgreSQL', 'MongoDB', 'Git', 'REST APIs'
                ]
            }
            
            response = {
                'success': True,
                'profile_data': mock_profile_data
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def handle_generate_resume(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        
        try:
            data = json.loads(post_data.decode('utf-8'))
            profile_data = data.get('profile_data', {})
            template = data.get('template', 'modern')
            
            # Create a simple text-based resume
            resume_content = self.generate_text_resume(profile_data, template)
            
            # Save to file
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"resume_{template}_{timestamp}.txt"
            
            os.makedirs('generated_resumes', exist_ok=True)
            filepath = os.path.join('generated_resumes', filename)
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(resume_content)
            
            response = {
                'success': True,
                'resume_path': filename
            }
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(json.dumps(response).encode())
            
        except Exception as e:
            self.send_response(500)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'error': str(e)}).encode())
    
    def generate_text_resume(self, profile_data, template):
        """Generate a simple text-based resume"""
        resume = []
        
        # Header
        if profile_data.get('personal_info'):
            info = profile_data['personal_info']
            resume.append(f"{'='*50}")
            resume.append(f"{info.get('name', 'N/A').upper()}")
            resume.append(f"{info.get('headline', 'N/A')}")
            resume.append(f"{'='*50}")
            resume.append("")
            
            # Contact info
            resume.append("CONTACT INFORMATION")
            resume.append(f"Email: {info.get('email', 'N/A')}")
            resume.append(f"Phone: {info.get('phone', 'N/A')}")
            resume.append(f"Location: {info.get('location', 'N/A')}")
            resume.append("")
            
            # Summary
            if info.get('summary'):
                resume.append("PROFESSIONAL SUMMARY")
                resume.append(info['summary'])
                resume.append("")
        
        # Experience
        if profile_data.get('experience'):
            resume.append("PROFESSIONAL EXPERIENCE")
            resume.append("-" * 30)
            for exp in profile_data['experience']:
                resume.append(f"{exp.get('title', 'N/A')} - {exp.get('company', 'N/A')}")
                resume.append(f"{exp.get('duration', 'N/A')} | {exp.get('location', 'N/A')}")
                resume.append(f"{exp.get('description', 'N/A')}")
                resume.append("")
        
        # Education
        if profile_data.get('education'):
            resume.append("EDUCATION")
            resume.append("-" * 30)
            for edu in profile_data['education']:
                resume.append(f"{edu.get('degree', 'N/A')}")
                resume.append(f"{edu.get('school', 'N/A')} | {edu.get('duration', 'N/A')}")
                if edu.get('gpa'):
                    resume.append(f"GPA: {edu['gpa']}")
                resume.append("")
        
        # Skills
        if profile_data.get('skills'):
            resume.append("TECHNICAL SKILLS")
            resume.append("-" * 30)
            resume.append(", ".join(profile_data['skills']))
            resume.append("")
        
        return "\n".join(resume)

def run_server(port=8000):
    """Run the simple HTTP server"""
    server_address = ('', port)
    httpd = HTTPServer(server_address, ResumeBuilderHandler)
    print(f"LinkedIn Resume Builder Demo Server")
    print(f"Server running on http://localhost:{port}")
    print(f"Press Ctrl+C to stop the server")
    print(f"=" * 50)
    
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nShutting down server...")
        httpd.server_close()

if __name__ == '__main__':
    # Create necessary directories
    os.makedirs('generated_resumes', exist_ok=True)
    os.makedirs('templates', exist_ok=True)
    os.makedirs('static', exist_ok=True)
    os.makedirs('static/css', exist_ok=True)
    os.makedirs('static/js', exist_ok=True)
    
    print("Starting LinkedIn Resume Builder Demo...")
    run_server() 