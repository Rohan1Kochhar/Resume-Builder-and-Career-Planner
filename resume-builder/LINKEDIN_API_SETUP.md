# LinkedIn API Integration Setup Guide

This guide will help you set up proper LinkedIn API integration for the Resume Builder application.

## Prerequisites

1. A LinkedIn account
2. Python 3.7+ installed
3. The Resume Builder application set up

## Step 1: Create a LinkedIn App

1. Go to [LinkedIn Developers](https://www.linkedin.com/developers/)
2. Click "Create App"
3. Fill in the required information:
   - **App Name**: Resume Builder (or your preferred name)
   - **LinkedIn Page**: Your company page (or create a new one)
   - **App Logo**: Upload a logo (optional)
4. Click "Create App"

## Step 2: Configure OAuth 2.0 Settings

1. In your LinkedIn app dashboard, go to "Auth" tab
2. Add the following redirect URLs:
   - `http://localhost:5000/linkedin-callback` (for development)
   - `https://yourdomain.com/linkedin-callback` (for production)
3. Save the changes

## Step 3: Get API Credentials

1. In your LinkedIn app dashboard, go to "Settings" tab
2. Copy the following values:
   - **Client ID**
   - **Client Secret**

## Step 4: Configure Environment Variables

1. Copy `env_example.txt` to `.env`:
   ```bash
   cp env_example.txt .env
   ```

2. Edit the `.env` file and add your LinkedIn credentials:
   ```env
   # LinkedIn API Configuration
   LINKEDIN_CLIENT_ID=your-actual-client-id
   LINKEDIN_CLIENT_SECRET=your-actual-client-secret
   LINKEDIN_REDIRECT_URI=http://localhost:5000/linkedin-callback
   ```

## Step 5: Install Dependencies

Run the setup script to install the required dependencies:
```bash
python -m pip install -r requirements.txt
```

## Step 6: Test the Integration

1. Start the application:
   ```bash
   python app.py
   ```

2. Open your browser and go to `http://localhost:5000`

3. Click "Connect with LinkedIn" to test the OAuth flow

## API Features

### Available Scopes

The application requests the following LinkedIn API scopes:

- **r_liteprofile**: Read basic profile information (name, headline, location, etc.)
- **r_emailaddress**: Read email address

### Data Retrieved

The LinkedIn API integration retrieves:

- **Personal Information**: Name, headline, location, email
- **Experience**: Job titles, companies, durations, descriptions
- **Education**: Degrees, schools, durations, GPAs
- **Skills**: Endorsed skills from LinkedIn profile
- **Summary**: Profile summary/about section

## Security Considerations

1. **Never commit your `.env` file** to version control
2. **Keep your Client Secret secure** and don't share it publicly
3. **Use HTTPS in production** for secure OAuth redirects
4. **Implement proper session management** for production use

## Troubleshooting

### Common Issues

1. **"Invalid redirect URI" error**:
   - Make sure the redirect URI in your LinkedIn app matches exactly
   - Check for trailing slashes or protocol mismatches

2. **"Client ID not found" error**:
   - Verify your Client ID is correct
   - Check that the `.env` file is in the correct location

3. **"Access token expired" error**:
   - The application will automatically refresh tokens when possible
   - Users may need to re-authenticate if refresh fails

### API Limits

LinkedIn API has rate limits:
- **Profile API**: 100 requests per day per user
- **Email API**: 100 requests per day per user

## Production Deployment

For production deployment:

1. **Update redirect URIs** in LinkedIn app to use your production domain
2. **Set environment variables** on your production server
3. **Use HTTPS** for all OAuth redirects
4. **Implement proper error handling** and logging
5. **Add rate limiting** to respect LinkedIn API limits

## Alternative: Demo Mode

If you don't want to set up LinkedIn API credentials, the application will fall back to demo mode with mock data. This is useful for:

- Development and testing
- Demonstrations
- Users who don't want to connect their LinkedIn account

## Support

For issues with LinkedIn API integration:

1. Check the [LinkedIn API Documentation](https://developer.linkedin.com/docs)
2. Review the [LinkedIn API Status Page](https://developer.linkedin.com/status)
3. Check the application logs for detailed error messages 