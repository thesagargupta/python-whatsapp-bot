# WhatsApp Bot Generation Prompt

Use this prompt with your preferred AI assistant to generate a complete WhatsApp bot with menu system, Google Sheets authorization, and Google Drive file sharing.

---

## 🤖 Prompt to Generate WhatsApp Bot

```
Create a complete WhatsApp bot in Python with the following specifications:

### Core Requirements:
1. **Framework**: Use Flask for the web server
2. **Single File Implementation**: All code must be in a single `bot.py` file
3. **WhatsApp Integration**: Use Meta WhatsApp Business API (Graph API v18.0)

### Features to Implement:

#### 1. WhatsApp Service
- Send text messages to users
- Mark messages as read
- Handle incoming webhook messages from Meta
- Use Bearer token authentication

#### 2. Menu System (3-Level Hierarchy)
**Main Menu:**
- Option 1: Academic Resources
- Option 2: Study Sessions
- Option 3: Support & Help

**Menu 1 - Academic Resources Submenus:**
- 1.1: Course Materials
- 1.2: Practice Tests
- 1.3: Study Guides

**Menu 2 - Study Sessions Submenus:**
- 2.1: Schedule Session
- 2.2: Join Live Session
- 2.3: View Recordings

**Menu 3 - Support & Help Submenus:**
- 3.1: Contact Admin
- 3.2: FAQ
- 3.3: Technical Support

**Menu Navigation:**
- Users can type numbers (1, 2, 3) to navigate main menus
- Users can type submenu numbers (1.1, 1.2, etc. or 11, 12, etc.)
- Users can type "back", "menu", or "main" to return to main menu
- Store user session state to track current menu position

#### 3. Google Sheets Integration (Authorization)
- Connect to Google Sheets using service account credentials
- Read authorized phone numbers from Sheet1, Column A
- Compare incoming phone numbers against authorized list
- Handle phone number matching (with/without country codes)
- Send unauthorized message if user not in sheet
- Support testing mode to bypass authorization

#### 4. Google Drive Integration (File Sharing)
- Connect to Google Drive using service account credentials
- Search for user-specific folders by phone number
- Support parent folder ID for organization
- List all files in user's folder
- Return file names and shareable links
- Handle cases where user folder doesn't exist

#### 5. Configuration Management
Use environment variables for:
- WHATSAPP_TOKEN (Meta access token)
- WHATSAPP_PHONE_NUMBER_ID (Phone number ID)
- VERIFY_TOKEN (Webhook verification token)
- WHATSAPP_BUSINESS_ACCOUNT_ID
- APP_ID
- APP_SECRET
- GOOGLE_SHEET_ID
- GOOGLE_SERVICE_ACCOUNT_EMAIL
- GOOGLE_PRIVATE_KEY
- GOOGLE_DRIVE_FOLDER_ID
- PORT (default 3000)
- TESTING_MODE (true/false)

#### 6. API Endpoints

**GET /webhook**
- Webhook verification endpoint
- Verify hub.mode, hub.verify_token, and return hub.challenge

**POST /webhook**
- Receive incoming WhatsApp messages
- Extract message data from nested JSON structure
- Process user authorization
- Handle menu navigation
- Fetch and send Google Drive files for submenus
- Send appropriate responses

**POST /send-test**
- Test endpoint to manually send messages
- Accept JSON: {"to": "phone_number", "message": "text"}

**GET /**
- Health check endpoint
- Return bot status and available endpoints

#### 7. Logging
- Use Python logging module
- Log all important events:
  - Incoming messages
  - Authorization checks
  - API calls
  - Errors and exceptions
- Use emoji prefixes for better readability (✅, ❌, 📩, 🔍, etc.)

#### 8. Error Handling
- Wrap API calls in try-except blocks
- Handle Google API errors gracefully
- Log errors with details
- Continue operation even if optional features fail
- Return appropriate HTTP status codes

#### 9. Code Structure
Organize the code with these classes:
- `Config`: Configuration and environment variables
- `WhatsAppService`: WhatsApp API interactions
- `GoogleSheetsService`: Google Sheets integration
- `GoogleDriveService`: Google Drive integration
- `MenuSystem`: Menu navigation logic

Include proper docstrings for all classes and methods.

#### 10. Additional Requirements
- Use type hints for function parameters and returns
- Add comprehensive comments explaining logic
- Format WhatsApp messages with emojis and markdown (*, _, ~)
- Clean phone numbers before comparison (remove non-digits)
- Initialize Google services on startup
- Validate environment variables on startup

### Expected Output:
Provide a complete, production-ready `bot.py` file that:
1. Can be run with `python bot.py`
2. Handles all error cases gracefully
3. Is well-documented with comments
4. Follows Python best practices
5. Uses proper logging instead of print statements
6. Is modular and maintainable despite being in a single file

Also provide:
1. `requirements.txt` with all necessary Python packages
2. `.env.example` file with all required environment variables
3. `README.md` with setup and deployment instructions
```

---

## 🔧 How to Use This Prompt

### Step 1: Copy the Prompt
Copy the entire prompt above (everything inside the triple backticks).

### Step 2: Paste into AI Assistant
Paste the prompt into your preferred AI assistant:
- ChatGPT (GPT-4 or GPT-3.5)
- Claude
- GitHub Copilot
- Any other code generation AI

### Step 3: Review Generated Code
The AI will generate:
- `bot.py` - Complete bot implementation
- `requirements.txt` - Python dependencies
- `.env.example` - Environment variables template
- `README.md` - Setup instructions

### Step 4: Customize for Your Needs
After generation, customize:
- Menu text and options
- Menu structure (add/remove menus)
- File fetching logic
- Authorization logic
- Any additional features

### Step 5: Add Your Credentials

#### Meta WhatsApp API:
1. Go to [Meta for Developers](https://developers.facebook.com/)
2. Create a new app or select existing
3. Add WhatsApp product
4. Get your credentials:
   - Access Token (WHATSAPP_TOKEN)
   - Phone Number ID (WHATSAPP_PHONE_NUMBER_ID)
   - Create a verify token (VERIFY_TOKEN) - any string
   - Business Account ID (WHATSAPP_BUSINESS_ACCOUNT_ID)
   - App ID (APP_ID)
   - App Secret (APP_SECRET)

#### Google Sheets API:
1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google Sheets API
4. Create a Service Account
5. Download JSON credentials
6. Extract from JSON:
   - client_email → GOOGLE_SERVICE_ACCOUNT_EMAIL
   - private_key → GOOGLE_PRIVATE_KEY (keep \n characters)
7. Create a Google Sheet and get its ID from URL
8. Share the sheet with the service account email

#### Google Drive API:
1. In same Google Cloud project, enable Google Drive API
2. Use same service account credentials
3. Create a parent folder in Google Drive
4. Create subfolders named with phone numbers (e.g., "919876543210")
5. Add files to these subfolders
6. Share the parent folder with the service account email
7. Get parent folder ID from URL

### Step 6: Deploy
Choose a deployment method:
- **Local Testing**: Run with `python bot.py` and expose with ngrok
- **Cloud Hosting**: Deploy to Heroku, Railway, Render, or any cloud platform
- **VPS**: Deploy to DigitalOcean, AWS EC2, or similar

### Step 7: Configure Webhook
1. Expose your server publicly (use ngrok for testing)
2. Go to Meta App Dashboard → WhatsApp → Configuration
3. Set Webhook URL: `https://your-domain.com/webhook`
4. Set Verify Token: Same as your VERIFY_TOKEN
5. Subscribe to messages webhook event

---

## 🎯 Customization Tips

### Modify Menu Structure:
```python
# In MenuSystem class, add/modify methods:
def get_menu_4(self) -> Dict[str, Any]:
    return {
        'text': '🎨 *Your New Menu*\n\nChoose an option...',
        'type': self.MENUS['MENU_4']
    }
```

### Change Authorization Logic:
```python
# In check_authorization function:
def check_authorization(phone_number: str) -> bool:
    # Add your custom logic here
    # Example: check database, API, or hardcoded list
    return True
```

### Add New Features:
- Image/video sending: Modify `send_message` method
- Button menus: Use WhatsApp interactive messages
- Database integration: Add SQLite or PostgreSQL
- Analytics: Track user interactions
- Scheduled messages: Add APScheduler

### Modify File Fetching:
```python
# In GoogleDriveService class:
def get_user_folder_files(self, phone_number: str) -> List[Dict]:
    # Customize folder search logic
    # Filter files by type
    # Sort files by date
    # Add file descriptions
```

---

## 📝 Additional Configuration

### Testing Mode:
Set `TESTING_MODE=true` to:
- Skip Google Sheets authorization
- Allow all users to access the bot
- Useful for development and testing

### Production Mode:
Set `TESTING_MODE=false` to:
- Enable Google Sheets authorization
- Only allow registered phone numbers
- Recommended for live deployment

### Phone Number Format:
The bot automatically handles:
- Numbers with country code: +919876543210
- Numbers without country code: 9876543210
- Numbers with spaces/dashes: +91 98765 43210

Add phone numbers to Google Sheet in any format.

---

## 🔒 Security Best Practices

1. **Never commit .env file** - Add to .gitignore
2. **Use environment variables** - Don't hardcode credentials
3. **Rotate tokens regularly** - Update access tokens periodically
4. **Limit service account permissions** - Only grant necessary scopes
5. **Use HTTPS** - Always use secure connections
6. **Validate webhook signatures** - Add signature verification (optional)
7. **Rate limiting** - Implement rate limiting for API calls
8. **Error messages** - Don't expose sensitive info in error messages

---

## 🐛 Troubleshooting

### Bot not responding:
- Check WHATSAPP_TOKEN is valid
- Verify webhook is configured correctly
- Check server logs for errors
- Ensure VERIFY_TOKEN matches

### Authorization not working:
- Verify Google Sheet is shared with service account
- Check GOOGLE_SHEET_ID is correct
- Verify phone numbers in sheet match format
- Check GOOGLE_PRIVATE_KEY has proper \n characters

### Files not showing:
- Verify Google Drive folder structure
- Check folder names match phone numbers exactly
- Ensure service account has access to folders
- Verify GOOGLE_DRIVE_FOLDER_ID is correct

### Server errors:
- Check all environment variables are set
- Verify Python dependencies are installed
- Check server logs for detailed errors
- Ensure port is not already in use

---

## 📚 Resources

- [Meta WhatsApp Business API Docs](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Google Sheets API Docs](https://developers.google.com/sheets/api)
- [Google Drive API Docs](https://developers.google.com/drive/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)

---

## ✨ Features You Can Add

1. **Database Integration**: Store user data, conversations, analytics
2. **Media Support**: Send/receive images, videos, documents
3. **Button Messages**: Interactive button menus
4. **List Messages**: Scrollable list selections
5. **Scheduled Messages**: Send messages at specific times
6. **Multi-language**: Support multiple languages
7. **Admin Panel**: Web interface for management
8. **Analytics Dashboard**: Track usage statistics
9. **Webhook Verification**: Verify Meta signatures
10. **Rate Limiting**: Prevent API abuse

---

## 🤝 Support

If you encounter issues:
1. Check the troubleshooting section above
2. Review server logs for error messages
3. Verify all credentials are correct
4. Test each component independently
5. Refer to official API documentation

---

**Note**: This prompt is designed to generate a complete, working WhatsApp bot. The generated code should work out-of-the-box once you add your credentials. If you need to modify functionality, refer to the customization tips above.
