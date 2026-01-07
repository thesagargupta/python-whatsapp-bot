"""
WhatsApp Bot with Menu System and Google Sheets/Drive Integration
==================================================================
A comprehensive WhatsApp bot built with Python Flask that provides:
- Interactive menu system (3 main menus, each with 3 submenus)
- User authorization via Google Sheets
- File sharing from Google Drive
- Meta WhatsApp Business API integration
- Message read receipts

Author: Generated from WhatsApp Bot Template
License: MIT
"""

import os
import json
import logging
from typing import Dict, List, Optional, Any
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import requests
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


# ============================================
# Configuration
# ============================================
class Config:
    """Configuration class for storing all credentials and settings"""
    
    # Meta WhatsApp API Configuration
    WHATSAPP_TOKEN = os.getenv('WHATSAPP_TOKEN')
    WHATSAPP_PHONE_NUMBER_ID = os.getenv('WHATSAPP_PHONE_NUMBER_ID')
    VERIFY_TOKEN = os.getenv('VERIFY_TOKEN')
    WHATSAPP_BUSINESS_ACCOUNT_ID = os.getenv('WHATSAPP_BUSINESS_ACCOUNT_ID')
    APP_ID = os.getenv('APP_ID')
    APP_SECRET = os.getenv('APP_SECRET')
    
    # Google Sheets Configuration
    GOOGLE_SHEET_ID = os.getenv('GOOGLE_SHEET_ID')
    GOOGLE_SERVICE_ACCOUNT_EMAIL = os.getenv('GOOGLE_SERVICE_ACCOUNT_EMAIL')
    GOOGLE_PRIVATE_KEY = os.getenv('GOOGLE_PRIVATE_KEY', '').replace('\\n', '\n')
    
    # Google Drive Configuration
    GOOGLE_DRIVE_FOLDER_ID = os.getenv('GOOGLE_DRIVE_FOLDER_ID')
    
    # Server Configuration
    PORT = int(os.getenv('PORT', 3000))
    
    # Testing Mode
    TESTING_MODE = os.getenv('TESTING_MODE', 'true').lower() == 'true'
    
    @classmethod
    def validate(cls):
        """Validate required environment variables"""
        required_vars = ['WHATSAPP_TOKEN', 'WHATSAPP_PHONE_NUMBER_ID', 'VERIFY_TOKEN']
        missing_vars = [var for var in required_vars if not getattr(cls, var)]
        if missing_vars:
            logger.warning(f'⚠️  Warning: Missing environment variables: {", ".join(missing_vars)}')
        return len(missing_vars) == 0


# ============================================
# WhatsApp Service
# ============================================
class WhatsAppService:
    """Service for interacting with WhatsApp Business API"""
    
    def __init__(self):
        self.token = Config.WHATSAPP_TOKEN
        self.phone_number_id = Config.WHATSAPP_PHONE_NUMBER_ID
        self.api_url = f"https://graph.facebook.com/v18.0/{self.phone_number_id}/messages"
    
    def send_message(self, to: str, message: str) -> Optional[Dict]:
        """
        Send a text message to a WhatsApp user
        
        Args:
            to: Recipient phone number
            message: Message text to send
            
        Returns:
            API response data or None if error
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messaging_product': 'whatsapp',
                'to': to,
                'type': 'text',
                'text': {
                    'body': message
                }
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            
            logger.info(f'✅ Message sent successfully to {to}')
            return response.json()
            
        except requests.exceptions.RequestException as e:
            logger.error(f'❌ Error sending message: {e}')
            if hasattr(e, 'response') and e.response is not None:
                logger.error(f'Response: {e.response.text}')
            return None
    
    def mark_as_read(self, message_id: str) -> bool:
        """
        Mark a message as read
        
        Args:
            message_id: ID of the message to mark as read
            
        Returns:
            True if successful, False otherwise
        """
        try:
            headers = {
                'Authorization': f'Bearer {self.token}',
                'Content-Type': 'application/json'
            }
            
            payload = {
                'messaging_product': 'whatsapp',
                'status': 'read',
                'message_id': message_id
            }
            
            response = requests.post(self.api_url, headers=headers, json=payload)
            response.raise_for_status()
            return True
            
        except requests.exceptions.RequestException as e:
            logger.error(f'❌ Error marking message as read: {e}')
            return False


# ============================================
# Google Sheets Service
# ============================================
class GoogleSheetsService:
    """Service for Google Sheets integration and user authorization"""
    
    def __init__(self):
        self.sheet_id = Config.GOOGLE_SHEET_ID
        self.credentials = None
        self.service = None
        self.initialized = False
    
    def initialize(self):
        """Initialize Google Sheets API connection"""
        try:
            if not Config.GOOGLE_SERVICE_ACCOUNT_EMAIL or not Config.GOOGLE_PRIVATE_KEY:
                logger.warning('❌ Google Sheets credentials not configured')
                return False
            
            credentials_info = {
                'type': 'service_account',
                'client_email': Config.GOOGLE_SERVICE_ACCOUNT_EMAIL,
                'private_key': Config.GOOGLE_PRIVATE_KEY,
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
            
            self.credentials = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=['https://www.googleapis.com/auth/spreadsheets.readonly']
            )
            
            self.service = build('sheets', 'v4', credentials=self.credentials)
            self.initialized = True
            logger.info('✅ Google Sheets API initialized successfully')
            return True
            
        except Exception as e:
            logger.error(f'❌ Error initializing Google Sheets: {e}')
            return False
    
    def is_user_authorized(self, phone_number: str) -> bool:
        """
        Check if a phone number is authorized by looking it up in Google Sheets
        
        Args:
            phone_number: Phone number to check
            
        Returns:
            True if authorized, False otherwise
        """
        try:
            if not self.initialized or not self.service:
                logger.warning('❌ Google Sheets not initialized, denying authorization')
                return False
            
            # Read from Sheet1, column A (adjust range as needed)
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.sheet_id,
                range='Sheet1!A:A'
            ).execute()
            
            values = result.get('values', [])
            
            # Extract and clean phone numbers
            authorized_numbers = []
            for row in values:
                if row and row[0]:
                    num = str(row[0]).strip()
                    # Only keep entries with at least one digit
                    if any(c.isdigit() for c in num):
                        authorized_numbers.append(num)
            
            logger.info(f'📋 Authorized numbers from sheet: {authorized_numbers}')
            
            # Clean phone number for comparison (remove non-digits)
            clean_number = ''.join(filter(str.isdigit, phone_number))
            logger.info(f'🔍 Checking phone number: {clean_number}')
            
            # Check if the number matches any authorized number
            for auth_num in authorized_numbers:
                clean_auth = ''.join(filter(str.isdigit, auth_num))
                
                # Skip invalid entries
                if not clean_auth or len(clean_auth) < 10:
                    logger.debug(f'  Skipping invalid entry: {auth_num}')
                    continue
                
                logger.debug(f'  Comparing with: {clean_auth}')
                
                # Match if numbers are equal or one ends with the other
                if (clean_auth == clean_number or 
                    clean_auth.endswith(clean_number) or 
                    clean_number.endswith(clean_auth)):
                    logger.info('🎯 Match found!')
                    return True
            
            logger.info('❌ No match found')
            return False
            
        except HttpError as e:
            logger.error(f'❌ Error checking user authorization: {e}')
            return False
        except Exception as e:
            logger.error(f'❌ Unexpected error in authorization check: {e}')
            return False


# ============================================
# Google Drive Service
# ============================================
class GoogleDriveService:
    """Service for Google Drive integration and file sharing"""
    
    def __init__(self):
        self.parent_folder_id = Config.GOOGLE_DRIVE_FOLDER_ID
        self.credentials = None
        self.service = None
        self.initialized = False
    
    def initialize(self):
        """Initialize Google Drive API connection"""
        try:
            if not Config.GOOGLE_SERVICE_ACCOUNT_EMAIL or not Config.GOOGLE_PRIVATE_KEY:
                logger.warning('❌ Google Drive credentials not configured')
                return False
            
            credentials_info = {
                'type': 'service_account',
                'client_email': Config.GOOGLE_SERVICE_ACCOUNT_EMAIL,
                'private_key': Config.GOOGLE_PRIVATE_KEY,
                'token_uri': 'https://oauth2.googleapis.com/token',
            }
            
            self.credentials = service_account.Credentials.from_service_account_info(
                credentials_info,
                scopes=['https://www.googleapis.com/auth/drive.readonly']
            )
            
            self.service = build('drive', 'v3', credentials=self.credentials)
            self.initialized = True
            logger.info('✅ Google Drive API initialized successfully')
            return True
            
        except Exception as e:
            logger.error(f'❌ Error initializing Google Drive: {e}')
            return False
    
    def get_user_folder_files(self, phone_number: str) -> List[Dict]:
        """
        Get all files from a user's folder in Google Drive
        
        Args:
            phone_number: Phone number (used as folder name)
            
        Returns:
            List of file dictionaries with id, name, link, and mimeType
        """
        try:
            if not self.initialized or not self.service:
                logger.warning('❌ Google Drive not initialized')
                return []
            
            logger.info(f'🔍 Searching for folder: {phone_number}')
            
            # Search for folder with the phone number name
            folder_query = f"name='{phone_number}' and mimeType='application/vnd.google-apps.folder' and trashed=false"
            
            # If parent folder ID is provided, search within it
            if self.parent_folder_id:
                folder_query += f" and '{self.parent_folder_id}' in parents"
            
            # Find the user's folder
            folder_results = self.service.files().list(
                q=folder_query,
                fields='files(id, name)',
                spaces='drive'
            ).execute()
            
            folders = folder_results.get('files', [])
            
            if not folders:
                logger.info(f'❌ No folder found for phone number: {phone_number}')
                return []
            
            user_folder_id = folders[0]['id']
            logger.info(f'✅ Found folder: {folders[0]["name"]} (ID: {user_folder_id})')
            
            # Get all files in the user's folder
            files_results = self.service.files().list(
                q=f"'{user_folder_id}' in parents and trashed=false",
                fields='files(id, name, mimeType, webViewLink, webContentLink)',
                spaces='drive'
            ).execute()
            
            files = files_results.get('files', [])
            logger.info(f'📁 Found {len(files)} file(s) in folder')
            
            return [
                {
                    'id': file['id'],
                    'name': file['name'],
                    'link': file.get('webViewLink') or file.get('webContentLink'),
                    'mimeType': file['mimeType']
                }
                for file in files
            ]
            
        except HttpError as e:
            logger.error(f'❌ Error fetching user folder files: {e}')
            return []
        except Exception as e:
            logger.error(f'❌ Unexpected error fetching files: {e}')
            return []


# ============================================
# Menu System
# ============================================
class MenuSystem:
    """Menu and submenu management system"""
    
    MENUS = {
        'MAIN': 'main',
        'MENU_1': 'menu1',
        'MENU_2': 'menu2',
        'MENU_3': 'menu3'
    }
    
    def __init__(self):
        self.user_sessions: Dict[str, str] = {}
    
    def get_main_menu(self) -> Dict[str, Any]:
        """Get the main menu"""
        return {
            'text': (
                '🏠 *Welcome to Study Cafe Bot!*\n\n'
                'Please select an option:\n\n'
                '1️⃣ Academic Resources\n'
                '2️⃣ Study Sessions\n'
                '3️⃣ Support & Help\n\n'
                'Reply with a number (1-3) to continue.'
            ),
            'type': self.MENUS['MAIN']
        }
    
    def get_menu_1(self) -> Dict[str, Any]:
        """Get menu 1 - Academic Resources"""
        return {
            'text': (
                '📚 *Academic Resources*\n\n'
                'Choose a submenu:\n\n'
                '1.1 Course Materials\n'
                '1.2 Practice Tests\n'
                '1.3 Study Guides\n\n'
                'Reply with the option number or type *back* to return to main menu.'
            ),
            'type': self.MENUS['MENU_1']
        }
    
    def get_menu_2(self) -> Dict[str, Any]:
        """Get menu 2 - Study Sessions"""
        return {
            'text': (
                '🎯 *Study Sessions*\n\n'
                'Choose a submenu:\n\n'
                '2.1 Schedule Session\n'
                '2.2 Join Live Session\n'
                '2.3 View Recordings\n\n'
                'Reply with the option number or type *back* to return to main menu.'
            ),
            'type': self.MENUS['MENU_2']
        }
    
    def get_menu_3(self) -> Dict[str, Any]:
        """Get menu 3 - Support & Help"""
        return {
            'text': (
                '💬 *Support & Help*\n\n'
                'Choose a submenu:\n\n'
                '3.1 Contact Admin\n'
                '3.2 FAQ\n'
                '3.3 Technical Support\n\n'
                'Reply with the option number or type *back* to return to main menu.'
            ),
            'type': self.MENUS['MENU_3']
        }
    
    def handle_user_input(self, user_id: str, message: str) -> Dict[str, Any]:
        """
        Handle user input and navigate through menus
        
        Args:
            user_id: User identifier (phone number)
            message: User's message text
            
        Returns:
            Dictionary with response text, type, and optional submenu info
        """
        input_text = message.lower().strip()
        current_menu = self.user_sessions.get(user_id, self.MENUS['MAIN'])
        
        # Handle back command
        if input_text in ['back', 'menu', 'main']:
            self.user_sessions[user_id] = self.MENUS['MAIN']
            return self.get_main_menu()
        
        # Handle main menu
        if current_menu == self.MENUS['MAIN']:
            if input_text == '1':
                self.user_sessions[user_id] = self.MENUS['MENU_1']
                return self.get_menu_1()
            elif input_text == '2':
                self.user_sessions[user_id] = self.MENUS['MENU_2']
                return self.get_menu_2()
            elif input_text == '3':
                self.user_sessions[user_id] = self.MENUS['MENU_3']
                return self.get_menu_3()
            else:
                return self.get_main_menu()
        
        # Handle Menu 1 submenus
        if current_menu == self.MENUS['MENU_1']:
            if input_text in ['1.1', '11']:
                return {
                    'text': '📖 *Course Materials*\n\nFetching your files...',
                    'type': self.MENUS['MENU_1'],
                    'isSubmenu': True,
                    'option': '1.1'
                }
            elif input_text in ['1.2', '12']:
                return {
                    'text': '✏️ *Practice Tests*\n\nFetching your files...',
                    'type': self.MENUS['MENU_1'],
                    'isSubmenu': True,
                    'option': '1.2'
                }
            elif input_text in ['1.3', '13']:
                return {
                    'text': '📝 *Study Guides*\n\nFetching your files...',
                    'type': self.MENUS['MENU_1'],
                    'isSubmenu': True,
                    'option': '1.3'
                }
            else:
                return self.get_menu_1()
        
        # Handle Menu 2 submenus
        if current_menu == self.MENUS['MENU_2']:
            if input_text in ['2.1', '21']:
                return {
                    'text': '📅 *Schedule Session*\n\nFetching your files...',
                    'type': self.MENUS['MENU_2'],
                    'isSubmenu': True,
                    'option': '2.1'
                }
            elif input_text in ['2.2', '22']:
                return {
                    'text': '🔴 *Join Live Session*\n\nFetching your files...',
                    'type': self.MENUS['MENU_2'],
                    'isSubmenu': True,
                    'option': '2.2'
                }
            elif input_text in ['2.3', '23']:
                return {
                    'text': '📹 *View Recordings*\n\nFetching your files...',
                    'type': self.MENUS['MENU_2'],
                    'isSubmenu': True,
                    'option': '2.3'
                }
            else:
                return self.get_menu_2()
        
        # Handle Menu 3 submenus
        if current_menu == self.MENUS['MENU_3']:
            if input_text in ['3.1', '31']:
                return {
                    'text': '👤 *Contact Admin*\n\nFetching your files...',
                    'type': self.MENUS['MENU_3'],
                    'isSubmenu': True,
                    'option': '3.1'
                }
            elif input_text in ['3.2', '32']:
                return {
                    'text': '❓ *FAQ*\n\nFetching your files...',
                    'type': self.MENUS['MENU_3'],
                    'isSubmenu': True,
                    'option': '3.2'
                }
            elif input_text in ['3.3', '33']:
                return {
                    'text': '🔧 *Technical Support*\n\nFetching your files...',
                    'type': self.MENUS['MENU_3'],
                    'isSubmenu': True,
                    'option': '3.3'
                }
            else:
                return self.get_menu_3()
        
        return self.get_main_menu()
    
    def reset_user_session(self, user_id: str):
        """Reset a user's session"""
        if user_id in self.user_sessions:
            del self.user_sessions[user_id]


# ============================================
# Flask Application
# ============================================
app = Flask(__name__)

# Initialize services
whatsapp_service = WhatsAppService()
google_sheets_service = GoogleSheetsService()
google_drive_service = GoogleDriveService()
menu_system = MenuSystem()

# Initialize Google services
google_sheets_service.initialize()
google_drive_service.initialize()

logger.info('🤖 WhatsApp Bot Starting...')
logger.info('📋 Make sure to update .env file with your credentials')


def check_authorization(phone_number: str) -> bool:
    """
    Check if a user is authorized to use the bot
    
    Args:
        phone_number: User's phone number
        
    Returns:
        True if authorized, False otherwise
    """
    logger.info(f'🔍 Authorization check for: {phone_number}')
    logger.info(f'📊 Testing mode enabled: {Config.TESTING_MODE}')
    logger.info(f'📋 Google Sheet ID configured: {bool(Config.GOOGLE_SHEET_ID)}')
    logger.info(f'🔑 Google credentials configured: {bool(Config.GOOGLE_SERVICE_ACCOUNT_EMAIL)}')
    
    if Config.TESTING_MODE:
        logger.info('⚠️  Testing mode: Authorizing all users')
        return True
    
    # Production mode - check Google Sheets
    try:
        is_authorized = google_sheets_service.is_user_authorized(phone_number)
        logger.info(f'🔐 Google Sheets authorization result: {is_authorized}')
        return is_authorized
    except Exception as e:
        logger.error(f'Authorization check error: {e}')
        return False


@app.route('/webhook', methods=['GET'])
def webhook_verify():
    """Webhook verification endpoint for Meta"""
    mode = request.args.get('hub.mode')
    token = request.args.get('hub.verify_token')
    challenge = request.args.get('hub.challenge')
    
    logger.info('Webhook verification request received')
    
    if mode == 'subscribe' and token == Config.VERIFY_TOKEN:
        logger.info('✅ Webhook verified successfully!')
        return challenge, 200
    else:
        logger.warning('❌ Webhook verification failed')
        return 'Forbidden', 403


@app.route('/webhook', methods=['POST'])
def webhook_receive():
    """Webhook endpoint to receive messages from WhatsApp"""
    try:
        data = request.get_json()
        logger.info(f'Incoming webhook: {json.dumps(data, indent=2)}')
        
        # Extract message data
        entry = data.get('entry', [{}])[0]
        changes = entry.get('changes', [{}])[0]
        value = changes.get('value', {})
        messages = value.get('messages', [])
        
        if not messages:
            return 'OK', 200
        
        message = messages[0]
        from_number = message.get('from')
        message_id = message.get('id')
        message_text = message.get('text', {}).get('body', '')
        
        logger.info(f'📩 Message received from {from_number}: {message_text}')
        
        # Mark message as read
        whatsapp_service.mark_as_read(message_id)
        
        # Check if user is authorized
        is_authorized = check_authorization(from_number)
        
        if not is_authorized:
            logger.info(f'❌ Unauthorized user: {from_number}')
            try:
                whatsapp_service.send_message(
                    from_number,
                    '🚫 *Unauthorized Access*\n\n'
                    'Sorry, your number is not registered in our system. '
                    'Please contact the administrator to get access.'
                )
            except Exception:
                logger.warning('⚠️  Could not send unauthorized message (Meta API restriction)')
            return 'OK', 200
        
        logger.info(f'✅ Authorized user: {from_number}')
        
        # Process menu navigation
        menu_response = menu_system.handle_user_input(from_number, message_text)
        
        # If submenu is selected, fetch and send Google Drive files
        if menu_response.get('isSubmenu'):
            logger.info(f'📂 Fetching files for user: {from_number}, option: {menu_response.get("option")}')
            
            files = google_drive_service.get_user_folder_files(from_number)
            
            if files:
                file_message = '📚 *Here are your files:*\n\n'
                for idx, file in enumerate(files, 1):
                    file_message += f'{idx}. {file["name"]}\n{file["link"]}\n\n'
                file_message += 'Type *back* to return to the menu.'
                
                whatsapp_service.send_message(from_number, file_message)
            else:
                whatsapp_service.send_message(
                    from_number,
                    '❌ No files found in your folder.\n\n'
                    'Please contact admin or type *back* to return to menu.'
                )
        else:
            # Regular menu navigation
            whatsapp_service.send_message(from_number, menu_response['text'])
        
        return 'OK', 200
        
    except Exception as e:
        logger.error(f'Error processing webhook: {e}', exc_info=True)
        return 'Internal Server Error', 500


@app.route('/send-test', methods=['POST'])
def send_test_message():
    """Test endpoint to send messages manually"""
    try:
        data = request.get_json()
        to = data.get('to')
        message = data.get('message')
        
        if not to or not message:
            return jsonify({'error': 'Missing "to" or "message" in request body'}), 400
        
        result = whatsapp_service.send_message(to, message)
        
        if result:
            return jsonify({'success': True, 'message': 'Message sent successfully'}), 200
        else:
            return jsonify({'success': False, 'message': 'Failed to send message'}), 500
            
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'running',
        'message': 'WhatsApp Bot is active',
        'endpoints': {
            'webhook_verification': 'GET /webhook',
            'webhook_receiver': 'POST /webhook',
            'test_send': 'POST /send-test'
        }
    }), 200


if __name__ == '__main__':
    # Validate configuration
    Config.validate()
    
    PORT = Config.PORT
    logger.info(f'\n✅ Server running on port {PORT}')
    logger.info(f'📍 Webhook URL: http://localhost:{PORT}/webhook')
    logger.info('\n📝 Setup Instructions:')
    logger.info('1. Update .env file with your Meta WhatsApp API credentials')
    logger.info('2. Use ngrok or similar tool to expose your local server')
    logger.info('3. Configure webhook URL in Meta App Dashboard')
    logger.info('4. Update Google Sheets and Drive credentials in .env')
    logger.info('5. Add authorized phone numbers to your Google Sheet')
    logger.info('\n🚀 Bot is ready to receive messages!\n')
    
    app.run(host='0.0.0.0', port=PORT, debug=False)
