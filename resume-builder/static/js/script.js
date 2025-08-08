// LinkedIn Resume Builder - Frontend JavaScript

class ResumeBuilder {
    constructor() {
        this.profileData = null;
        this.resumeFilename = null;
        this.initializeEventListeners();
    }

    initializeEventListeners() {
        // LinkedIn form submission
        const linkedinForm = document.getElementById('linkedinForm');
        if (linkedinForm) {
            linkedinForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.parseLinkedInProfile();
            });
        }

        // Generate resume button
        const generateBtn = document.getElementById('generateBtn');
        if (generateBtn) {
            generateBtn.addEventListener('click', () => {
                this.generateResume();
            });
        }

        // Edit information button
        const editBtn = document.getElementById('editBtn');
        if (editBtn) {
            editBtn.addEventListener('click', () => {
                this.showEditForm();
            });
        }

        // Download button
        const downloadBtn = document.getElementById('downloadBtn');
        if (downloadBtn) {
            downloadBtn.addEventListener('click', () => {
                this.downloadResume();
            });
        }

        // Template selection change
        const templateSelect = document.getElementById('templateSelect');
        if (templateSelect) {
            templateSelect.addEventListener('change', () => {
                this.updateTemplatePreview();
            });
        }

        // LinkedIn API checkbox change
        const useApiCheck = document.getElementById('useApiCheck');
        if (useApiCheck) {
            useApiCheck.addEventListener('change', (e) => {
                this.handleApiCheckboxChange(e.target.checked);
            });
        }

        // Mode selection
        document.querySelectorAll('input[name="buildMode"]').forEach(radio => {
            radio.addEventListener('change', (e) => {
                this.switchMode(e.target.value);
            });
        });

        // Manual resume form submission
        const manualResumeForm = document.getElementById('manualResumeForm');
        if (manualResumeForm) {
            manualResumeForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.generateManualResume();
            });
        }

        // Manual template selection change
        const manualTemplateSelect = document.getElementById('manualTemplateSelect');
        if (manualTemplateSelect) {
            manualTemplateSelect.addEventListener('change', () => {
                this.updateManualPreview();
            });
        }

        // Add dynamic entries
        const addExperience = document.getElementById('addExperience');
        if (addExperience) {
            addExperience.addEventListener('click', () => {
                this.addExperienceEntry();
            });
        }

        const addEducation = document.getElementById('addEducation');
        if (addEducation) {
            addEducation.addEventListener('click', () => {
                this.addEducationEntry();
            });
        }

        const addCertification = document.getElementById('addCertification');
        if (addCertification) {
            addCertification.addEventListener('click', () => {
                this.addCertificationEntry();
            });
        }

        // Real-time preview updates
        this.setupRealTimePreview();

        // GitHub form submission
        const githubForm = document.getElementById('githubForm');
        if (githubForm) {
            githubForm.addEventListener('submit', (e) => {
                e.preventDefault();
                this.parseGitHubProfile();
            });
        }

        // GitHub generate resume button
        const generateGitHubBtn = document.getElementById('generateGitHubBtn');
        if (generateGitHubBtn) {
            generateGitHubBtn.addEventListener('click', () => {
                this.generateGitHubResume();
            });
        }

        // GitHub edit information button
        const editGitHubBtn = document.getElementById('editGitHubBtn');
        if (editGitHubBtn) {
            editGitHubBtn.addEventListener('click', () => {
                this.showEditForm();
            });
        }

        // GitHub API checkbox change
        const useGitHubApiCheck = document.getElementById('useGitHubApiCheck');
        if (useGitHubApiCheck) {
            useGitHubApiCheck.addEventListener('change', (e) => {
                this.handleGitHubApiCheckboxChange(e.target.checked);
            });
        }

        // Check LinkedIn authentication status on page load
        this.checkLinkedInAuthStatus();
        // Check GitHub authentication status on page load
        this.checkGitHubAuthStatus();
    }

    async parseLinkedInProfile() {
        const linkedinUrl = document.getElementById('linkedinUrl').value;
        const template = document.getElementById('templateSelect').value;
        const useApi = document.getElementById('useApiCheck').checked;

        if (!linkedinUrl) {
            this.showError('Please enter a LinkedIn profile URL');
            return;
        }

        // Show loading state
        this.showLoading(true);
        this.hideError();

        try {
            const response = await fetch('/upload-linkedin', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    linkedin_url: linkedinUrl,
                    template: template,
                    use_api: useApi
                })
            });

            const data = await response.json();

            if (data.success) {
                this.profileData = data.profile_data;
                this.showProfilePreview();
                
                if (data.api_used) {
                    this.showSuccess('LinkedIn profile parsed successfully using LinkedIn API!');
                } else {
                    this.showSuccess('LinkedIn profile parsed successfully using demo data!');
                }
            } else {
                this.showError(data.error || 'Failed to parse LinkedIn profile');
            }
        } catch (error) {
            console.error('Error parsing LinkedIn profile:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.showLoading(false);
        }
    }

    async generateResume() {
        if (!this.profileData) {
            this.showError('No profile data available');
            return;
        }
        try {
            this.showLoading(true);
            const template = document.getElementById('templateSelect')?.value || 'modern';
            const format = document.getElementById('linkedinFormatSelect')?.value || 'docx';
            const response = await fetch('/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    profile_data: this.profileData,
                    template: template,
                    format: format
                })
            });
            const data = await response.json();
            if (data.success) {
                this.resumeFilename = data.filename;
                this.showResults();
                this.showSuccess('Resume generated successfully!');
                await this.suggestJobs(this.profileData);
            } else {
                this.showError(data.error || 'Failed to generate resume');
            }
        } catch (error) {
            console.error('Error generating resume:', error);
            this.showError('Failed to generate resume');
        } finally {
            this.showLoading(false);
        }
    }

    showProfilePreview() {
        const previewSection = document.getElementById('previewSection');
        const initialSection = document.getElementById('initialSection');
        const profilePreview = document.getElementById('profilePreview');

        // Hide initial section and show preview
        initialSection.classList.add('d-none');
        previewSection.classList.remove('d-none');

        // Populate profile preview
        let previewHTML = '';

        if (this.profileData.personal_info) {
            const info = this.profileData.personal_info;
            previewHTML += `
                <div class="profile-item">
                    <div class="profile-label">Name:</div>
                    <div class="profile-value">${info.name}</div>
                </div>
                <div class="profile-item">
                    <div class="profile-label">Headline:</div>
                    <div class="profile-value">${info.headline}</div>
                </div>
                <div class="profile-item">
                    <div class="profile-label">Location:</div>
                    <div class="profile-value">${info.location}</div>
                </div>
                <div class="profile-item">
                    <div class="profile-label">Email:</div>
                    <div class="profile-value">${info.email}</div>
                </div>
            `;
        }

        if (this.profileData.experience && this.profileData.experience.length > 0) {
            previewHTML += `
                <div class="profile-item">
                    <div class="profile-label">Experience:</div>
                    <div class="profile-value">${this.profileData.experience.length} positions</div>
                </div>
            `;
        }

        if (this.profileData.education && this.profileData.education.length > 0) {
            previewHTML += `
                <div class="profile-item">
                    <div class="profile-label">Education:</div>
                    <div class="profile-value">${this.profileData.education.length} degree(s)</div>
                </div>
            `;
        }

        if (this.profileData.skills && this.profileData.skills.length > 0) {
            previewHTML += `
                <div class="profile-item">
                    <div class="profile-label">Skills:</div>
                    <div class="profile-value">${this.profileData.skills.length} skills listed</div>
                </div>
            `;
        }

        profilePreview.innerHTML = previewHTML;
    }

    showResults() {
        const resultsSection = document.getElementById('resultsSection');
        resultsSection.style.display = 'block';
        
        // Scroll to results
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    // Add this method to show files in generated_resumes
    async showResumeFiles() {
        try {
            const res = await fetch('/list-resumes');
            const data = await res.json();
            alert('Files in generated_resumes:\n' + data.files.join('\n'));
        } catch (e) {
            alert('Failed to list files: ' + e);
        }
    }

    downloadResume() {
        if (!this.resumeFilename) {
            this.showError('No resume file available for download');
            return;
        }
        // Always extract just the filename
        let filename = this.resumeFilename;
        if (filename.includes('/')) {
            filename = filename.split('/').pop();
        }
        const downloadUrl = `/download-resume/${filename}`;
        console.log('[DEBUG] Downloading resume:', downloadUrl);
        // Create a temporary link and trigger download
        const link = document.createElement('a');
        link.href = downloadUrl;
        link.download = filename;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        // Add error handling for failed downloads
        setTimeout(() => {
            fetch(downloadUrl, { method: 'HEAD' })
                .then(res => {
                    if (!res.ok) {
                        this.showError('Resume file not found. Please try generating again.');
                        this.showResumeFiles();
                    }
                })
                .catch(() => {
                    this.showError('Resume file not found. Please try generating again.');
                    this.showResumeFiles();
                });
        }, 500);
        this.showSuccess('Resume download started!');
    }

    showEditForm() {
        // This would open a modal or form to edit the profile data
        // For now, just show an alert
        alert('Edit functionality would be implemented here. You can modify the profile data before generating the resume.');
    }

    updateTemplatePreview() {
        const template = document.getElementById('templateSelect').value;
        // This could update a preview of the selected template
        console.log('Template changed to:', template);
    }

    showLoading(show) {
        const loadingSection = document.getElementById('loadingSection');
        const parseBtn = document.getElementById('parseBtn');
        const generateBtn = document.getElementById('generateBtn');

        if (show) {
            loadingSection.classList.remove('d-none');
            parseBtn.disabled = true;
            if (generateBtn) generateBtn.disabled = true;
            parseBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        } else {
            loadingSection.classList.add('d-none');
            parseBtn.disabled = false;
            if (generateBtn) generateBtn.disabled = false;
            parseBtn.innerHTML = '<i class="fas fa-search me-2"></i>Parse LinkedIn Profile';
        }
    }

    showError(message) {
        this.hideError();
        const errorDiv = document.createElement('div');
        errorDiv.className = 'alert alert-danger mt-3';
        errorDiv.innerHTML = `<i class="fas fa-exclamation-triangle me-2"></i>${message}`;
        
        const form = document.getElementById('linkedinForm');
        form.appendChild(errorDiv);
    }

    showSuccess(message) {
        this.hideSuccess();
        const successDiv = document.createElement('div');
        successDiv.className = 'alert alert-success mt-3';
        successDiv.innerHTML = `<i class="fas fa-check-circle me-2"></i>${message}`;
        
        const form = document.getElementById('linkedinForm');
        form.appendChild(successDiv);
    }

    hideError() {
        const errorAlerts = document.querySelectorAll('.alert-danger');
        errorAlerts.forEach(alert => alert.remove());
    }

    hideSuccess() {
        const successAlerts = document.querySelectorAll('.alert-success');
        successAlerts.forEach(alert => alert.remove());
    }

    // Utility function to validate LinkedIn URL
    validateLinkedInUrl(url) {
        const linkedinPattern = /^https?:\/\/(www\.)?linkedin\.com\/in\/[a-zA-Z0-9-]+\/?$/;
        return linkedinPattern.test(url);
    }

    // Utility function to format profile data for display
    formatProfileData(data) {
        const formatted = {};
        
        if (data.personal_info) {
            formatted.personal = {
                name: data.personal_info.name || 'N/A',
                headline: data.personal_info.headline || 'N/A',
                location: data.personal_info.location || 'N/A',
                email: data.personal_info.email || 'N/A'
            };
        }
        
        if (data.experience) {
            formatted.experience = data.experience.map(exp => ({
                title: exp.title || 'N/A',
                company: exp.company || 'N/A',
                duration: exp.duration || 'N/A'
            }));
        }
        
        if (data.education) {
            formatted.education = data.education.map(edu => ({
                degree: edu.degree || 'N/A',
                school: edu.school || 'N/A',
                duration: edu.duration || 'N/A'
            }));
        }
        
        return formatted;
    }

    async checkLinkedInAuthStatus() {
        try {
            const response = await fetch('/check-linkedin-auth');
            const data = await response.json();
            
            if (data.authenticated) {
                this.updateLinkedInAuthUI(true);
            } else {
                this.updateLinkedInAuthUI(false);
            }
        } catch (error) {
            console.error('Error checking LinkedIn auth status:', error);
            this.updateLinkedInAuthUI(false);
        }
    }

    updateLinkedInAuthUI(authenticated) {
        const apiCheckbox = document.getElementById('useApiCheck');
        const authBtn = document.getElementById('linkedinAuthBtn');
        
        if (authenticated) {
            apiCheckbox.disabled = false;
            authBtn.innerHTML = '<i class="fas fa-check me-2"></i>LinkedIn Connected';
            authBtn.className = 'btn btn-success w-100';
            authBtn.href = '#';
            authBtn.onclick = (e) => {
                e.preventDefault();
                this.showSuccess('LinkedIn is already connected!');
            };
        } else {
            apiCheckbox.disabled = true;
            apiCheckbox.checked = false;
            authBtn.innerHTML = '<i class="fab fa-linkedin me-2"></i>Connect with LinkedIn';
            authBtn.className = 'btn btn-outline-primary w-100';
            authBtn.href = '/linkedin-auth';
            authBtn.onclick = null;
        }
    }

    handleApiCheckboxChange(checked) {
        if (checked) {
            // Check if user is authenticated
            this.checkLinkedInAuthStatus().then(() => {
                const apiCheckbox = document.getElementById('useApiCheck');
                if (apiCheckbox.disabled) {
                    this.showError('Please connect with LinkedIn first to use the API');
                    apiCheckbox.checked = false;
                }
            });
        }
    }

    // Mode switching
    switchMode(mode) {
        const linkedinSection = document.getElementById('linkedinModeSection');
        const githubSection = document.getElementById('githubModeSection');
        const manualSection = document.getElementById('manualModeSection');
        
        // Hide all sections first
        linkedinSection.classList.add('d-none');
        githubSection.classList.add('d-none');
        manualSection.classList.add('d-none');
        
        if (mode === 'linkedin') {
            linkedinSection.classList.remove('d-none');
        } else if (mode === 'github') {
            githubSection.classList.remove('d-none');
        } else if (mode === 'manual') {
            manualSection.classList.remove('d-none');
            this.updateManualPreview(); // Initialize preview
        }
    }

    async suggestJobs(profileData) {
        try {
            const res = await fetch('/suggest-jobs', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ profile_data: profileData })
            });
            const data = await res.json();
            this.renderJobSuggestions(data.jobs || []);
        } catch (e) {
            this.renderJobSuggestions([]);
        }
    }

    renderJobSuggestions(jobs) {
        let html = '';
        if (!jobs || jobs.length === 0) {
            html = '<div class="alert alert-warning">No job suggestions found. Try updating your skills or experience.</div>';
        } else {
            html = '<h5 class="mt-4 mb-3"><i class="fas fa-briefcase me-2"></i>Suggested Jobs for You</h5>';
            html += '<div class="list-group">';
            jobs.forEach(job => {
                html += `<a href="${job.url}" target="_blank" class="list-group-item list-group-item-action mb-2">
                    <div class="fw-bold">${job.title}</div>
                    <div class="small text-muted">${job.company} &mdash; ${job.location}</div>
                    <div class="small mt-1">${job.description}</div>
                </a>`;
            });
            html += '</div>';
        }
        let jobSection = document.getElementById('jobSuggestionsSection');
        if (!jobSection) {
            jobSection = document.createElement('div');
            jobSection.id = 'jobSuggestionsSection';
            const resultsSection = document.getElementById('resultsSection');
            resultsSection.parentNode.insertBefore(jobSection, resultsSection.nextSibling);
        }
        jobSection.innerHTML = html;
    }

    // Call suggestJobs after resume generation in all relevant places
    async generateManualResume() {
        const formData = this.collectManualFormData();
        if (!formData.personal_info.name) {
            this.showError('Please enter your name');
            return;
        }
        try {
            const template = document.getElementById('manualTemplateSelect').value;
            const format = document.getElementById('manualFormatSelect').value;
            const response = await fetch('/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    profile_data: formData,
                    template: template,
                    format: format
                })
            });
            const data = await response.json();
            if (data.success) {
                this.resumeFilename = data.filename;
                this.showResults();
                this.showSuccess('Resume generated successfully!');
                await this.suggestJobs(formData);
            } else {
                this.showError(data.error || 'Failed to generate resume');
            }
        } catch (error) {
            console.error('Error generating resume:', error);
            this.showError('Network error. Please try again.');
        }
    }

    // Collect manual form data
    collectManualFormData() {
        const formData = {
            personal_info: {
                name: document.getElementById('fullName').value,
                headline: document.getElementById('headline').value,
                location: document.getElementById('location').value,
                email: document.getElementById('email').value,
                phone: document.getElementById('phone').value,
                summary: document.getElementById('summary').value
            },
            experience: this.collectExperienceData(),
            education: this.collectEducationData(),
            skills: this.collectSkillsData(),
            certifications: this.collectCertificationData(),
            achievements: this.collectAchievementsData()
        };

        return formData;
    }

    // Collect experience data
    collectExperienceData() {
        const experiences = [];
        const entries = document.querySelectorAll('.experience-entry');
        
        entries.forEach(entry => {
            const title = entry.querySelector('.exp-title').value;
            const company = entry.querySelector('.exp-company').value;
            const location = entry.querySelector('.exp-location').value;
            const duration = entry.querySelector('.exp-duration').value;
            const description = entry.querySelector('.exp-description').value;
            
            if (title && company) {
                experiences.push({
                    title: title,
                    company: company,
                    location: location,
                    duration: duration,
                    description: description
                });
            }
        });
        
        return experiences;
    }

    // Collect education data
    collectEducationData() {
        const educations = [];
        const entries = document.querySelectorAll('.education-entry');
        
        entries.forEach(entry => {
            const degree = entry.querySelector('.edu-degree').value;
            const school = entry.querySelector('.edu-school').value;
            const location = entry.querySelector('.edu-location').value;
            const duration = entry.querySelector('.edu-duration').value;
            const gpa = entry.querySelector('.edu-gpa').value;
            
            if (degree && school) {
                educations.push({
                    degree: degree,
                    school: school,
                    location: location,
                    duration: duration,
                    gpa: gpa
                });
            }
        });
        
        return educations;
    }

    // Collect skills data
    collectSkillsData() {
        const skillsInput = document.getElementById('skills').value;
        return skillsInput.split(',').map(skill => skill.trim()).filter(skill => skill);
    }

    // Collect certification data
    collectCertificationData() {
        const certifications = [];
        const entries = document.querySelectorAll('.certification-entry');
        
        entries.forEach(entry => {
            const name = entry.querySelector('.cert-name').value;
            const issuer = entry.querySelector('.cert-issuer').value;
            const date = entry.querySelector('.cert-date').value;
            
            if (name && issuer) {
                certifications.push({
                    name: name,
                    issuer: issuer,
                    date: date
                });
            }
        });
        
        return certifications;
    }

    // Collect achievements data
    collectAchievementsData() {
        const achievementsInput = document.getElementById('achievements').value;
        return achievementsInput.split('\n').map(achievement => achievement.trim()).filter(achievement => achievement);
    }

    // Add experience entry
    addExperienceEntry() {
        const container = document.getElementById('experienceContainer');
        const entryId = 'exp-' + Date.now();
        
        const entryHTML = `
            <div class="dynamic-entry experience-entry" id="${entryId}">
                <button type="button" class="btn-remove" onclick="resumeBuilder.removeEntry('${entryId}')">
                    <i class="fas fa-times"></i>
                </button>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Job Title</label>
                            <input type="text" class="form-control exp-title" placeholder="Software Engineer">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Company</label>
                            <input type="text" class="form-control exp-company" placeholder="Tech Corp">
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Location</label>
                            <input type="text" class="form-control exp-location" placeholder="San Francisco, CA">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Duration</label>
                            <input type="text" class="form-control exp-duration" placeholder="Jan 2022 - Present">
                        </div>
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Description</label>
                    <textarea class="form-control exp-description" rows="3" placeholder="Describe your responsibilities and achievements..."></textarea>
                </div>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', entryHTML);
        this.setupRealTimePreview();
    }

    // Add education entry
    addEducationEntry() {
        const container = document.getElementById('educationContainer');
        const entryId = 'edu-' + Date.now();
        
        const entryHTML = `
            <div class="dynamic-entry education-entry" id="${entryId}">
                <button type="button" class="btn-remove" onclick="resumeBuilder.removeEntry('${entryId}')">
                    <i class="fas fa-times"></i>
                </button>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Degree</label>
                            <input type="text" class="form-control edu-degree" placeholder="Bachelor of Science in Computer Science">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">School</label>
                            <input type="text" class="form-control edu-school" placeholder="University of California">
                        </div>
                    </div>
                </div>
                <div class="row">
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label class="form-label">Location</label>
                            <input type="text" class="form-control edu-location" placeholder="Berkeley, CA">
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label class="form-label">Duration</label>
                            <input type="text" class="form-control edu-duration" placeholder="2015 - 2019">
                        </div>
                    </div>
                    <div class="col-md-4">
                        <div class="mb-3">
                            <label class="form-label">GPA</label>
                            <input type="text" class="form-control edu-gpa" placeholder="3.8/4.0">
                        </div>
                    </div>
                </div>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', entryHTML);
        this.setupRealTimePreview();
    }

    // Add certification entry
    addCertificationEntry() {
        const container = document.getElementById('certificationContainer');
        const entryId = 'cert-' + Date.now();
        
        const entryHTML = `
            <div class="dynamic-entry certification-entry" id="${entryId}">
                <button type="button" class="btn-remove" onclick="resumeBuilder.removeEntry('${entryId}')">
                    <i class="fas fa-times"></i>
                </button>
                <div class="row">
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Certification Name</label>
                            <input type="text" class="form-control cert-name" placeholder="AWS Certified Solutions Architect">
                        </div>
                    </div>
                    <div class="col-md-6">
                        <div class="mb-3">
                            <label class="form-label">Issuing Organization</label>
                            <input type="text" class="form-control cert-issuer" placeholder="Amazon Web Services">
                        </div>
                    </div>
                </div>
                <div class="mb-3">
                    <label class="form-label">Date Obtained</label>
                    <input type="text" class="form-control cert-date" placeholder="2023">
                </div>
            </div>
        `;
        
        container.insertAdjacentHTML('beforeend', entryHTML);
        this.setupRealTimePreview();
    }

    // Remove entry
    removeEntry(entryId) {
        const entry = document.getElementById(entryId);
        if (entry) {
            entry.remove();
            this.updateManualPreview();
        }
    }

    // Setup real-time preview
    setupRealTimePreview() {
        const inputs = document.querySelectorAll('#manualResumeForm input, #manualResumeForm textarea');
        inputs.forEach(input => {
            input.addEventListener('input', () => {
                this.updateManualPreview();
            });
        });
    }

    // Update manual preview
    updateManualPreview() {
        const formData = this.collectManualFormData();
        const preview = document.getElementById('livePreview');
        
        if (!formData.personal_info.name) {
            preview.innerHTML = '<div class="text-center text-muted mt-5"><i class="fas fa-file-alt fa-3x mb-3"></i><p>Start entering your information to see the live preview</p></div>';
            return;
        }
        
        preview.innerHTML = this.generatePreviewHTML(formData);
    }

    // Generate preview HTML
    generatePreviewHTML(data) {
        let html = `
            <h1>${data.personal_info.name || 'Your Name'}</h1>
            <div class="contact-info">
                ${data.personal_info.headline ? `<div>${data.personal_info.headline}</div>` : ''}
                ${data.personal_info.email ? `<div>${data.personal_info.email}</div>` : ''}
                ${data.personal_info.phone ? `<div>${data.personal_info.phone}</div>` : ''}
                ${data.personal_info.location ? `<div>${data.personal_info.location}</div>` : ''}
            </div>
        `;
        
        if (data.personal_info.summary) {
            html += `<div class="summary"><p>${data.personal_info.summary}</p></div>`;
        }
        
        if (data.experience && data.experience.length > 0) {
            html += '<h2>EXPERIENCE</h2>';
            data.experience.forEach(exp => {
                html += `
                    <div class="experience-item">
                        <h3 class="experience-title">${exp.title}</h3>
                        <div class="experience-company">${exp.company}</div>
                        <div class="experience-duration">${exp.duration}</div>
                        ${exp.description ? `<p>${exp.description}</p>` : ''}
                    </div>
                `;
            });
        }
        
        if (data.education && data.education.length > 0) {
            html += '<h2>EDUCATION</h2>';
            data.education.forEach(edu => {
                html += `
                    <div class="education-item">
                        <h3 class="education-title">${edu.degree}</h3>
                        <div class="education-school">${edu.school}</div>
                        <div class="education-duration">${edu.duration}${edu.gpa ? ` | GPA: ${edu.gpa}` : ''}</div>
                    </div>
                `;
            });
        }
        
        if (data.skills && data.skills.length > 0) {
            html += '<h2>SKILLS</h2>';
            html += '<div class="skills-list">';
            data.skills.forEach(skill => {
                html += `<span class="skill-tag">${skill}</span>`;
            });
            html += '</div>';
        }
        
        if (data.certifications && data.certifications.length > 0) {
            html += '<h2>CERTIFICATIONS</h2>';
            html += '<div class="certifications-list">';
            data.certifications.forEach(cert => {
                html += `<div class="certification-item">${cert.name} - ${cert.issuer} (${cert.date})</div>`;
            });
            html += '</div>';
        }
        
        if (data.achievements && data.achievements.length > 0) {
            html += '<h2>ACHIEVEMENTS</h2>';
            html += '<div class="achievements-list">';
            data.achievements.forEach(achievement => {
                html += `<div class="achievement-item">${achievement}</div>`;
            });
            html += '</div>';
        }
        
        return html;
    }

    // GitHub-specific methods
    async parseGitHubProfile() {
        const githubUrl = document.getElementById('githubUrl').value;
        const template = document.getElementById('githubTemplateSelect').value;
        const useApi = document.getElementById('useGitHubApiCheck').checked;

        if (!githubUrl) {
            this.showError('Please enter a GitHub profile URL');
            return;
        }

        // Show loading state
        this.showGitHubLoading(true);
        this.hideError();

        try {
            const response = await fetch('/upload-github', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    github_url: githubUrl,
                    template: template,
                    use_api: useApi
                })
            });

            const data = await response.json();

            if (data.success) {
                this.profileData = data.profile_data;
                this.showGitHubProfilePreview();
                this.showGitHubSuccess(`GitHub profile parsed successfully! ${data.api_used ? 'Using GitHub API' : 'Using demo data'}`);
                // Auto-generate resume
                await this.generateGitHubResume();
            } else {
                this.showError(data.error || 'Failed to parse GitHub profile');
            }
        } catch (error) {
            console.error('Error parsing GitHub profile:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.showGitHubLoading(false);
        }
    }

    async generateGitHubResume() {
        if (!this.profileData) {
            this.showError('No profile data available. Please parse a GitHub profile first.');
            return;
        }
        try {
            const template = document.getElementById('githubTemplateSelect').value;
            const format = document.getElementById('githubFormatSelect').value;
            const response = await fetch('/generate-resume', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    profile_data: this.profileData,
                    template: template,
                    format: format
                })
            });
            const data = await response.json();
            if (data.success) {
                this.resumeFilename = data.filename;
                this.showGitHubResults();
                this.showGitHubSuccess('Resume generated successfully!');
                await this.suggestJobs(this.profileData);
            } else {
                this.showError(data.error || 'Failed to generate resume');
            }
        } catch (error) {
            console.error('Error generating resume:', error);
            this.showError('Network error. Please try again.');
        } finally {
            this.showGitHubLoading(false);
        }
    }

    showGitHubProfilePreview() {
        const previewSection = document.getElementById('githubPreviewSection');
        const initialSection = document.getElementById('githubInitialSection');
        const profilePreview = document.getElementById('githubProfilePreview');

        previewSection.classList.remove('d-none');
        initialSection.classList.add('d-none');

        // Improved preview rendering
        const data = this.profileData;
        let html = `<div class='card shadow-sm mb-3'>`;
        html += `<div class='card-body'>`;
        html += `<div class='d-flex align-items-center mb-3'>`;
        html += `<div class='me-3'><i class='fab fa-github fa-3x'></i></div>`;
        html += `<div>`;
        html += `<h3 class='mb-0'>${data.name || ''}</h3>`;
        html += `<div class='text-muted'>${data.headline || ''}</div>`;
        html += `<div class='small'>${data.location || ''}</div>`;
        html += `</div></div>`;
        if (data.summary) {
            html += `<div class='mb-2'><strong>Bio:</strong> ${data.summary}</div>`;
        }
        if (data.skills && data.skills.length > 0) {
            html += `<div class='mb-2'><strong>Top Skills:</strong> `;
            html += data.skills.map(skill => `<span class='badge bg-primary me-1'>${skill}</span>`).join(' ');
            html += `</div>`;
        }
        if (data.experience && data.experience.length > 0) {
            html += `<div class='mb-2'><strong>Top Projects:</strong><ul class='mb-0'>`;
            data.experience.slice(0, 3).forEach(exp => {
                html += `<li><strong>${exp.title}</strong> <span class='text-muted'>(${exp.duration})</span><br><span class='small'>${exp.description}</span></li>`;
            });
            html += `</ul></div>`;
        }
        if (data.achievements && data.achievements.length > 0) {
            html += `<div class='mb-2'><strong>Achievements:</strong><ul class='mb-0'>`;
            data.achievements.forEach(ach => {
                html += `<li>${ach}</li>`;
            });
            html += `</ul></div>`;
        }
        html += `</div></div>`;
        // Always show download button if resume is generated
        if (this.resumeFilename) {
            html += `<div class='text-center mt-3'><button class='btn btn-lg btn-success' onclick='resumeBuilder.downloadResume()'><i class='fas fa-download me-2'></i>Download Resume</button></div>`;
        }
        profilePreview.innerHTML = html;
    }

    showGitHubResults() {
        const resultsSection = document.getElementById('githubPreviewSection');
        resultsSection.style.display = 'block';
        resultsSection.scrollIntoView({ behavior: 'smooth' });
    }

    showGitHubLoading(show) {
        const loadingSection = document.getElementById('githubLoadingSection');
        const parseBtn = document.getElementById('parseGitHubBtn');
        const generateBtn = document.getElementById('generateGitHubBtn');

        if (show) {
            loadingSection.classList.remove('d-none');
            parseBtn.disabled = true;
            if (generateBtn) generateBtn.disabled = true;
            parseBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Processing...';
        } else {
            loadingSection.classList.add('d-none');
            parseBtn.disabled = false;
            if (generateBtn) generateBtn.disabled = false;
            parseBtn.innerHTML = '<i class="fas fa-search me-2"></i>Parse GitHub Profile';
        }
    }

    showGitHubSuccess(message) {
        this.hideError();
        const successDiv = document.createElement('div');
        successDiv.className = 'alert alert-success mt-3';
        successDiv.innerHTML = `<i class="fas fa-check-circle me-2"></i>${message}`;
        
        const form = document.getElementById('githubForm');
        form.appendChild(successDiv);
    }

    async checkGitHubAuthStatus() {
        try {
            const response = await fetch('/check-github-auth');
            const data = await response.json();
            this.updateGitHubAuthUI(data.authenticated);
        } catch (error) {
            console.error('Error checking GitHub auth status:', error);
            this.updateGitHubAuthUI(false);
        }
    }

    updateGitHubAuthUI(authenticated) {
        const apiCheckbox = document.getElementById('useGitHubApiCheck');
        const authBtn = document.getElementById('githubAuthBtn');

        if (authenticated) {
            apiCheckbox.disabled = false;
            apiCheckbox.checked = true;
            authBtn.innerHTML = '<i class="fab fa-github me-2"></i>Connected with GitHub';
            authBtn.className = 'btn btn-success w-100';
            authBtn.href = '#';
            authBtn.onclick = (e) => {
                e.preventDefault();
                alert('Already connected with GitHub');
            };
        } else {
            apiCheckbox.disabled = true;
            apiCheckbox.checked = false;
            authBtn.innerHTML = '<i class="fab fa-github me-2"></i>Connect with GitHub';
            authBtn.className = 'btn btn-outline-primary w-100';
            authBtn.href = '/github-auth';
            authBtn.onclick = null;
        }
    }

    handleGitHubApiCheckboxChange(checked) {
        if (checked) {
            // Check if user is authenticated
            this.checkGitHubAuthStatus().then(() => {
                const apiCheckbox = document.getElementById('useGitHubApiCheck');
                if (apiCheckbox.disabled) {
                    this.showError('Please connect with GitHub first to use the API');
                    apiCheckbox.checked = false;
                }
            });
        }
    }

    validateGitHubUrl(url) {
        if (!url) return false;
        return url.includes('github.com/');
    }
}

// Initialize the application when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new ResumeBuilder();
    const jobSearchForm = document.getElementById('jobSearchForm');
    if (jobSearchForm) {
        jobSearchForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const skills = document.getElementById('jobSkills').value;
            const experience = document.getElementById('jobExperience').value;
            const location = document.getElementById('jobLocation').value;
            const jobType = document.getElementById('jobType').value;
            const res = await fetch('/job-search', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ skills, experience, location, jobType })
            });
            const data = await res.json();
            renderJobSearchResults(data.jobs || []);
        });
    }
});

function renderJobSearchResults(jobs) {
    const resultsDiv = document.getElementById('jobSearchResults');
    if (!resultsDiv) return;
    if (!jobs.length) {
        resultsDiv.innerHTML = '<div class="alert alert-warning">No jobs found for your criteria.</div>';
        return;
    }
    let html = '';
    jobs.forEach(job => {
        html += `<div class="col-md-6 col-lg-4 mb-4">
            <div class="card h-100 shadow border-info">
                <div class="card-body">
                    <div class="d-flex align-items-center mb-2">
                        ${job.logo ? `<img src="${job.logo}" alt="logo" class="me-2" style="width:40px;height:40px;object-fit:contain;border-radius:6px;">` : ''}
                        <div>
                            <h5 class="card-title mb-0">${job.title}</h5>
                            <h6 class="card-subtitle text-muted">${job.company}</h6>
                        </div>
                    </div>
                    <p class="card-text mb-1"><i class="fas fa-map-marker-alt me-1"></i> ${job.location || 'Remote'}</p>
                    <p class="mb-1"><span class="badge bg-info">${job.type || 'N/A'}</span> ${job.category ? `<span class='badge bg-secondary ms-1'>${job.category}</span>` : ''}</p>
                    ${job.salary ? `<p class='mb-1'><i class='fas fa-money-bill-wave me-1'></i> <span class='text-success'>${job.salary}</span></p>` : ''}
                    <p class="card-text small">${job.description ? job.description.substring(0, 120) + '...' : ''}</p>
                    <a href="${job.url}" target="_blank" class="btn btn-outline-info w-100">Apply</a>
                </div>
            </div>
        </div>`;
    });
    resultsDiv.innerHTML = html;
}

// Add some additional utility functions
window.ResumeBuilderUtils = {
    // Format date for display
    formatDate: (dateString) => {
        if (!dateString) return 'N/A';
        try {
            return new Date(dateString).toLocaleDateString();
        } catch {
            return dateString;
        }
    },

    // Truncate text for preview
    truncateText: (text, maxLength = 100) => {
        if (!text) return 'N/A';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    },

    // Capitalize first letter
    capitalize: (text) => {
        if (!text) return '';
        return text.charAt(0).toUpperCase() + text.slice(1);
    }
}; 