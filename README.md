# WhatsApp Bot with Menu System (Python)

A comprehensive WhatsApp bot built with Python Flask that provides an interactive menu system, user authorization via Google Sheets, and file sharing from Google Drive.

## ✨ Features

- ✅ **Three-level menu system** (3 main menus, each with 3 submenus)
- ✅ **User authorization** via Google Sheets
- ✅ **File sharing** from Google Drive (organized by phone number folders)
- ✅ **Meta WhatsApp Business API** integration
- ✅ **Message read receipts**
- ✅ **Session management** for menu navigation
- ✅ **Testing mode** for development without Google Sheets
- ✅ **Comprehensive logging** with emoji indicators
- ✅ **Single-file implementation** for easy deployment

## 📁 Project Structure

```
python-wat-bot/
├── bot.py              # Main bot implementation (single file)
├── requirements.txt    # Python dependencies
├── .env.example        # Environment variables template
├── prompt.md          # Prompt to regenerate bot with AI
└── README.md          # This file
```

## 🚀 Quick Start

### 1. Prerequisites

- Python 3.8 or higher
- Meta WhatsApp Business Account
- Google Cloud Account (for Sheets & Drive)

### 2. Installation

```bash
# Clone or download the repository
cd python-wat-bot

# Install dependencies
pip install -r requirements.txt

# Create .env file from template
cp .env.example .env
```

### 3. Configure Environment Variables

Edit the `.env` file and add your credentials:

```env
# Meta WhatsApp API
WHATSAPP_TOKEN=your_access_token
WHATSAPP_PHONE_NUMBER_ID=your_phone_number_id
VERIFY_TOKEN=your_custom_verify_token

# Google Sheets (for authorization)
GOOGLE_SHEET_ID=your_sheet_id
GOOGLE_SERVICE_ACCOUNT_EMAIL=your-service-account@project.iam.gserviceaccount.com
GOOGLE_PRIVATE_KEY=-----BEGIN PRIVATE KEY-----\nYourKey\n-----END PRIVATE KEY-----

# Google Drive (for file sharing)
GOOGLE_DRIVE_FOLDER_ID=your_parent_folder_id

# Server
PORT=3000
TESTING_MODE=true
```

### 4. Run the Bot

```bash
python bot.py
```

The server will start on `http://localhost:3000`

### 5. Expose with ngrok (for testing)

```bash
# In a new terminal
ngrok http 3000
```

Copy the HTTPS URL provided by ngrok.

### 6. Configure Webhook in Meta

1. Go to [Meta for Developers](https://developers.facebook.com/apps/)
2. Select your app → WhatsApp → Configuration
3. Set Webhook URL: `https://your-ngrok-url.ngrok.io/webhook`
4. Set Verify Token: Same as your `VERIFY_TOKEN` in `.env`
5. Subscribe to `messages` webhook event

## 📋 Detailed Setup

### Meta WhatsApp Business API Setup

#### Step 1: Create Meta App
1. Go to https://developers.facebook.com/apps/
2. Click "Create App"
3. Select "Business" type
4. Fill in app details

#### Step 2: Add WhatsApp Product
1. In your app dashboard, click "Add Product"
2. Find "WhatsApp" and click "Set Up"
3. Follow the setup wizard

#### Step 3: Get Credentials
- **Phone Number ID**: WhatsApp → API Setup → Phone Number ID
- **Access Token**: WhatsApp → API Setup → Temporary/Permanent Token
- **Business Account ID**: WhatsApp → API Setup → Business Account ID
- **App ID**: Settings → Basic → App ID
- **App Secret**: Settings → Basic → App Secret
- **Verify Token**: Create your own (any random string)

#### Step 4: Test Number (Optional)
- Add test numbers in WhatsApp → API Setup → To
- Test numbers can receive messages for free

### Google Sheets Setup (Authorization)

#### Step 1: Create Google Cloud Project
1. Go to https://console.cloud.google.com/
2. Create new project or select existing
3. Enable "Google Sheets API"

#### Step 2: Create Service Account
1. Go to "IAM & Admin" → "Service Accounts"
2. Click "Create Service Account"
3. Name it (e.g., "whatsapp-bot")
4. Grant "Editor" role
5. Click "Done"

#### Step 3: Create Key
1. Click on the service account email
2. Go to "Keys" tab
3. Click "Add Key" → "Create New Key"
4. Select "JSON" format
5. Download the JSON file

#### Step 4: Extract Credentials
Open the downloaded JSON file and extract:
- `client_email` → `GOOGLE_SERVICE_ACCOUNT_EMAIL`
- `private_key` → `GOOGLE_PRIVATE_KEY` (keep the `\n` characters)

#### Step 5: Create Google Sheet
1. Create a new Google Sheet
2. In Column A, add authorized phone numbers (one per row)
   ```
   919876543210
   918765432109
   917654321098
   ```
3. Get Sheet ID from URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
4. Share sheet with service account email (give "Viewer" permission)

### Google Drive Setup (File Sharing)

#### Step 1: Enable Google Drive API
1. In same Google Cloud project
2. Go to "APIs & Services" → "Library"
3. Search for "Google Drive API"
4. Click "Enable"

#### Step 2: Create Folder Structure
1. Create a parent folder in Google Drive (e.g., "WhatsApp Bot Files")
2. Inside parent folder, create subfolders named with phone numbers:
   ```
   WhatsApp Bot Files/
   ├── 919876543210/
   │   ├── file1.pdf
   │   └── file2.pdf
   ├── 918765432109/
   │   ├── document.docx
   │   └── image.jpg
   └── 917654321098/
       └── video.mp4
   ```
3. Get parent folder ID from URL: `https://drive.google.com/drive/folders/{FOLDER_ID}`
4. Share parent folder with service account email (give "Viewer" permission)

## 🎮 Usage

### For End Users

Once the bot is running and configured:

1. **Send a message** to the WhatsApp number configured in your Meta app
2. **Receive main menu** with three options:
   ```
   🏠 Welcome to Study Cafe Bot!
   
   Please select an option:
   
   1️⃣ Academic Resources
   2️⃣ Study Sessions
   3️⃣ Support & Help
   ```
3. **Reply with a number** (1, 2, or 3) to see submenus
4. **Select submenu** by replying with option number (e.g., 1.1, 1.2, or 11, 12)
5. **Receive files** from your Google Drive folder
6. **Type "back"** to return to main menu

### Menu Structure

```
Main Menu
├── 1. Academic Resources
│   ├── 1.1 Course Materials
│   ├── 1.2 Practice Tests
│   └── 1.3 Study Guides
├── 2. Study Sessions
│   ├── 2.1 Schedule Session
│   ├── 2.2 Join Live Session
│   └── 2.3 View Recordings
└── 3. Support & Help
    ├── 3.1 Contact Admin
    ├── 3.2 FAQ
    └── 3.3 Technical Support
```

### Commands

- `1`, `2`, `3` - Navigate main menus
- `1.1`, `1.2`, `1.3` (or `11`, `12`, `13`) - Select submenus
- `back`, `menu`, `main` - Return to main menu

## 🧪 Testing

### Test Without Google Sheets

Set in `.env`:
```env
TESTING_MODE=true
```

This will authorize all users without checking Google Sheets.

### Test Message Sending

```bash
curl -X POST http://localhost:3000/send-test \
  -H "Content-Type: application/json" \
  -d '{"to": "919876543210", "message": "Hello from bot!"}'
```

### Test Webhook Verification

```bash
curl "http://localhost:3000/webhook?hub.mode=subscribe&hub.verify_token=your_verify_token&hub.challenge=test123"
```

Should return: `test123`

## 🔧 Configuration

### Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `WHATSAPP_TOKEN` | Meta access token | Yes |
| `WHATSAPP_PHONE_NUMBER_ID` | Phone number ID | Yes |
| `VERIFY_TOKEN` | Webhook verify token | Yes |
| `WHATSAPP_BUSINESS_ACCOUNT_ID` | Business account ID | No |
| `APP_ID` | Meta app ID | No |
| `APP_SECRET` | Meta app secret | No |
| `GOOGLE_SHEET_ID` | Google Sheets ID | No* |
| `GOOGLE_SERVICE_ACCOUNT_EMAIL` | Service account email | No* |
| `GOOGLE_PRIVATE_KEY` | Service account private key | No* |
| `GOOGLE_DRIVE_FOLDER_ID` | Parent folder ID | No* |
| `PORT` | Server port | No (default: 3000) |
| `TESTING_MODE` | Skip authorization | No (default: true) |

*Required for production mode (`TESTING_MODE=false`)

### Testing vs Production Mode

**Testing Mode** (`TESTING_MODE=true`):
- ✅ Authorizes all users
- ✅ No Google Sheets needed
- ✅ Good for development
- ❌ Not secure for production

**Production Mode** (`TESTING_MODE=false`):
- ✅ Checks Google Sheets for authorization
- ✅ Only registered users can access
- ✅ Secure for production
- ❌ Requires Google Sheets setup

## 🚢 Deployment

### Deploy to Heroku

```bash
# Install Heroku CLI
# Login to Heroku
heroku login

# Create app
heroku create your-whatsapp-bot

# Set environment variables
heroku config:set WHATSAPP_TOKEN=your_token
heroku config:set WHATSAPP_PHONE_NUMBER_ID=your_id
# ... set all other variables

# Deploy
git init
git add .
git commit -m "Initial commit"
git push heroku main

# Check logs
heroku logs --tail
```

### Deploy to Railway

1. Go to https://railway.app/
2. Click "New Project" → "Deploy from GitHub"
3. Select your repository
4. Add environment variables in Settings
5. Deploy

### Deploy to Render

1. Go to https://render.com/
2. Click "New" → "Web Service"
3. Connect your repository
4. Set build command: `pip install -r requirements.txt`
5. Set start command: `python bot.py`
6. Add environment variables
7. Deploy

### Deploy to VPS (Ubuntu)

```bash
# SSH into your VPS
ssh user@your-server-ip

# Install Python and pip
sudo apt update
sudo apt install python3 python3-pip

# Clone repository
git clone your-repo-url
cd python-wat-bot

# Install dependencies
pip3 install -r requirements.txt

# Create .env file
nano .env
# (paste your credentials)

# Run with nohup (keeps running after logout)
nohup python3 bot.py > bot.log 2>&1 &

# Or use systemd for production
sudo nano /etc/systemd/system/whatsapp-bot.service
```

Systemd service file:
```ini
[Unit]
Description=WhatsApp Bot
After=network.target

[Service]
User=your-user
WorkingDirectory=/path/to/python-wat-bot
Environment="PATH=/usr/bin"
ExecStart=/usr/bin/python3 bot.py
Restart=always

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable whatsapp-bot
sudo systemctl start whatsapp-bot
sudo systemctl status whatsapp-bot
```

## 📝 Customization

### Modify Menus

Edit the `MenuSystem` class in `bot.py`:

```python
def get_main_menu(self) -> Dict[str, Any]:
    return {
        'text': (
            '🏠 *Your Custom Main Menu*\n\n'
            'Select:\n\n'
            '1️⃣ Your Option 1\n'
            '2️⃣ Your Option 2\n'
        ),
        'type': self.MENUS['MAIN']
    }
```

### Add New Menu Level

```python
# Add to MENUS dict
MENUS = {
    'MAIN': 'main',
    'MENU_1': 'menu1',
    'MENU_2': 'menu2',
    'MENU_3': 'menu3',
    'MENU_4': 'menu4'  # New menu
}

# Add getter method
def get_menu_4(self) -> Dict[str, Any]:
    return {
        'text': '🎨 *Your New Menu*\n\nChoose an option...',
        'type': self.MENUS['MENU_4']
    }

# Add to handle_user_input
if current_menu == self.MENUS['MAIN']:
    # ... existing code ...
    elif input_text == '4':
        self.user_sessions[user_id] = self.MENUS['MENU_4']
        return self.get_menu_4()
```

### Change Authorization Logic

```python
def check_authorization(phone_number: str) -> bool:
    # Custom authorization logic
    # Example: Check database
    # Example: Call external API
    # Example: Use hardcoded list
    
    authorized_numbers = ['919876543210', '918765432109']
    clean_number = ''.join(filter(str.isdigit, phone_number))
    return clean_number in authorized_numbers
```

## 🐛 Troubleshooting

### Bot Not Responding

**Check webhook configuration:**
```bash
# Verify webhook endpoint
curl http://your-server/webhook
```

**Check logs:**
```bash
# If running locally
# Check terminal output

# If on Heroku
heroku logs --tail

# If on systemd
sudo journalctl -u whatsapp-bot -f
```

**Verify Meta credentials:**
- Check if access token is expired
- Verify phone number ID is correct
- Ensure webhook is subscribed to messages

### Authorization Issues

**Check Google Sheets:**
- Verify sheet is shared with service account
- Check phone numbers format in sheet
- Ensure `GOOGLE_SHEET_ID` is correct

**Check credentials:**
```python
# Test in Python console
from google.oauth2 import service_account

credentials_info = {
    'type': 'service_account',
    'client_email': 'your-email@project.iam.gserviceaccount.com',
    'private_key': 'your-key',
    'token_uri': 'https://oauth2.googleapis.com/token',
}

creds = service_account.Credentials.from_service_account_info(
    credentials_info,
    scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
)
print("✅ Credentials valid")
```

### Files Not Showing

**Check Google Drive:**
- Verify folder names match phone numbers exactly
- Ensure service account has access
- Check `GOOGLE_DRIVE_FOLDER_ID` is correct

**Test manually:**
```python
# In Python console
from googleapiclient.discovery import build

service = build('drive', 'v3', credentials=creds)
results = service.files().list(pageSize=10).execute()
print(results.get('files', []))
```

### Server Errors

**Check environment variables:**
```bash
# Print all env vars
python -c "import os; print(os.environ)"
```

**Check port availability:**
```bash
# Check if port is in use
netstat -ano | findstr :3000  # Windows
lsof -i :3000                  # Linux/Mac
```

**Verify dependencies:**
```bash
pip list
pip install -r requirements.txt --upgrade
```

## 📚 API Reference

### Endpoints

#### `GET /webhook`
Webhook verification endpoint.

**Query Parameters:**
- `hub.mode` - Should be "subscribe"
- `hub.verify_token` - Your verify token
- `hub.challenge` - Challenge string to return

**Response:** Challenge string (200) or Forbidden (403)

#### `POST /webhook`
Receive WhatsApp messages.

**Request Body:** WhatsApp webhook payload

**Response:** 200 OK

#### `POST /send-test`
Test message sending.

**Request Body:**
```json
{
  "to": "919876543210",
  "message": "Hello!"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Message sent successfully"
}
```

#### `GET /`
Health check.

**Response:**
```json
{
  "status": "running",
  "message": "WhatsApp Bot is active",
  "endpoints": {
    "webhook_verification": "GET /webhook",
    "webhook_receiver": "POST /webhook",
    "test_send": "POST /send-test"
  }
}
```

## 🔒 Security

- ✅ Never commit `.env` file - Add to `.gitignore`
- ✅ Use environment variables for all credentials
- ✅ Rotate access tokens regularly
- ✅ Limit service account permissions
- ✅ Use HTTPS in production
- ✅ Implement rate limiting (optional)
- ✅ Add webhook signature verification (optional)

## 📖 Resources

- [Meta WhatsApp Business API](https://developers.facebook.com/docs/whatsapp/cloud-api)
- [Google Sheets API](https://developers.google.com/sheets/api)
- [Google Drive API](https://developers.google.com/drive/api)
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python dotenv](https://pypi.org/project/python-dotenv/)

## 🤝 Contributing

Feel free to customize the bot for your needs. If you want to regenerate the bot with AI:
1. See `prompt.md` for the complete generation prompt
2. Paste the prompt into ChatGPT, Claude, or similar
3. Add your credentials
4. Deploy

## 📄 License

MIT License - Feel free to use and modify as needed.

## 🆘 Support

If you encounter issues:
1. Check the troubleshooting section
2. Review server logs
3. Verify all credentials
4. Refer to API documentation
5. Create an issue in the repository

## 🎉 Acknowledgments

This bot is a Python port of the original Node.js WhatsApp bot with enhanced features and single-file implementation for easier deployment and management.

---

**Made with ❤️ for easy WhatsApp bot deployment**
# python-whatsapp-bot
