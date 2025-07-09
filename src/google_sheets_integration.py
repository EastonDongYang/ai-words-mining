import json
import os
from typing import List, Dict, Optional
from datetime import datetime
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google.oauth2.service_account import Credentials as ServiceAccountCredentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config

class GoogleSheetsIntegration:
    """Google Sheets API integration for updating AI words data"""
    
    SCOPES = ['https://www.googleapis.com/auth/spreadsheets']
    
    def __init__(self):
        self.config = Config()
        self.service = None
        self.spreadsheet_id = self.config.GOOGLE_SHEETS_ID
        self.range_name = self.config.GOOGLE_SHEETS_RANGE
        self.setup_service()
    
    def setup_service(self):
        """Setup Google Sheets API service"""
        creds = None
        
        # Try to load service account credentials first
        try:
            if os.path.exists(self.config.GOOGLE_SHEETS_CREDENTIALS_PATH):
                creds = ServiceAccountCredentials.from_service_account_file(
                    self.config.GOOGLE_SHEETS_CREDENTIALS_PATH,
                    scopes=self.SCOPES
                )
                print("Using service account credentials")
            else:
                print(f"Service account credentials file not found: {self.config.GOOGLE_SHEETS_CREDENTIALS_PATH}")
                
        except Exception as e:
            print(f"Error loading service account credentials: {e}")
        
        # Fallback to OAuth flow if service account fails
        if not creds:
            creds = self.setup_oauth_credentials()
        
        if creds:
            try:
                self.service = build('sheets', 'v4', credentials=creds)
                print("Google Sheets API service initialized successfully")
            except Exception as e:
                print(f"Error building Google Sheets service: {e}")
                self.service = None
        else:
            print("Failed to setup Google Sheets credentials")
    
    def setup_oauth_credentials(self):
        """Setup OAuth2 credentials for Google Sheets"""
        creds = None
        
        # Load existing token
        token_file = 'token.json'
        if os.path.exists(token_file):
            try:
                creds = Credentials.from_authorized_user_file(token_file, self.SCOPES)
            except Exception as e:
                print(f"Error loading existing token: {e}")
        
        # If there are no valid credentials, let the user log in
        if not creds or not creds.valid:
            if creds and creds.expired and creds.refresh_token:
                try:
                    creds.refresh(Request())
                except Exception as e:
                    print(f"Error refreshing token: {e}")
                    creds = None
            
            if not creds:
                # This would require user interaction, so we'll skip it in automated mode
                print("OAuth credentials setup required but not available in automated mode")
                return None
        
        # Save the credentials for the next run
        if creds:
            try:
                with open(token_file, 'w') as token:
                    token.write(creds.to_json())
            except Exception as e:
                print(f"Error saving token: {e}")
        
        return creds
    
    def create_headers(self) -> List[str]:
        """Create headers for the Google Sheet"""
        return [
            'Word',
            'Category',
            'Definition',
            'Importance',
            'Trend Potential',
            'Business Value',
            'Is Emerging',
            'Extraction Count',
            'Ranking Score',
            'First Seen',
            'Last Seen',
            'Related Terms',
            'Target Sectors',
            'Contexts'
        ]
    
    def prepare_sheet_data(self, words_data: List[Dict]) -> List[List[str]]:
        """Prepare words data for Google Sheets format"""
        if not words_data:
            return []
        
        # Add headers
        sheet_data = [self.create_headers()]
        
        # Add word data
        for word_data in words_data:
            row = [
                word_data.get('word', ''),
                word_data.get('category', ''),
                word_data.get('definition', ''),
                word_data.get('importance', ''),
                str(word_data.get('trend_potential', 5)),
                word_data.get('business_value', ''),
                str(word_data.get('is_emerging', False)),
                str(word_data.get('extraction_count', 1)),
                str(round(word_data.get('ranking_score', 0), 2)),
                word_data.get('first_seen', ''),
                word_data.get('last_seen', ''),
                ', '.join(word_data.get('related_terms', [])),
                ', '.join(word_data.get('target_sectors', [])),
                ' | '.join(word_data.get('contexts', []))
            ]
            sheet_data.append(row)
        
        return sheet_data
    
    def get_sheet_info(self) -> Optional[Dict]:
        """Get information about the spreadsheet"""
        if not self.service:
            return None
        
        try:
            sheet = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            return {
                'title': sheet.get('properties', {}).get('title', 'Unknown'),
                'sheets': [s['properties']['title'] for s in sheet.get('sheets', [])],
                'url': f"https://docs.google.com/spreadsheets/d/{self.spreadsheet_id}"
            }
        except HttpError as e:
            print(f"Error getting sheet info: {e}")
            return None
    
    def clear_sheet(self, range_name: str = None) -> bool:
        """Clear existing data from the sheet"""
        if not self.service:
            return False
        
        if not range_name:
            range_name = self.range_name
        
        try:
            self.service.spreadsheets().values().clear(
                spreadsheetId=self.spreadsheet_id,
                range=range_name
            ).execute()
            
            print(f"Cleared data from range: {range_name}")
            return True
            
        except HttpError as e:
            print(f"Error clearing sheet: {e}")
            return False
    
    def update_sheet(self, sheet_data: List[List[str]], range_name: str = None, clear_first: bool = True) -> bool:
        """Update the Google Sheet with new data"""
        if not self.service:
            print("Google Sheets service not available")
            return False
        
        if not sheet_data:
            print("No data to update")
            return False
        
        if not range_name:
            range_name = self.range_name
        
        try:
            # Clear existing data if requested
            if clear_first:
                self.clear_sheet(range_name)
            
            # Update with new data
            body = {
                'values': sheet_data
            }
            
            result = self.service.spreadsheets().values().update(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                body=body
            ).execute()
            
            updated_cells = result.get('updatedCells', 0)
            print(f"Updated {updated_cells} cells in Google Sheets")
            
            return True
            
        except HttpError as e:
            print(f"Error updating sheet: {e}")
            return False
    
    def append_to_sheet(self, sheet_data: List[List[str]], range_name: str = None) -> bool:
        """Append data to the Google Sheet"""
        if not self.service:
            print("Google Sheets service not available")
            return False
        
        if not sheet_data:
            print("No data to append")
            return False
        
        if not range_name:
            range_name = self.range_name
        
        try:
            body = {
                'values': sheet_data
            }
            
            result = self.service.spreadsheets().values().append(
                spreadsheetId=self.spreadsheet_id,
                range=range_name,
                valueInputOption='RAW',
                insertDataOption='INSERT_ROWS',
                body=body
            ).execute()
            
            updated_cells = result.get('updates', {}).get('updatedCells', 0)
            print(f"Appended {updated_cells} cells to Google Sheets")
            
            return True
            
        except HttpError as e:
            print(f"Error appending to sheet: {e}")
            return False
    
    def format_sheet(self) -> bool:
        """Apply formatting to the Google Sheet"""
        if not self.service:
            return False
        
        try:
            # Get sheet ID
            sheet_metadata = self.service.spreadsheets().get(
                spreadsheetId=self.spreadsheet_id
            ).execute()
            
            sheet_id = sheet_metadata['sheets'][0]['properties']['sheetId']
            
            # Format headers
            requests = [
                {
                    'repeatCell': {
                        'range': {
                            'sheetId': sheet_id,
                            'startRowIndex': 0,
                            'endRowIndex': 1
                        },
                        'cell': {
                            'userEnteredFormat': {
                                'textFormat': {
                                    'bold': True
                                },
                                'backgroundColor': {
                                    'red': 0.9,
                                    'green': 0.9,
                                    'blue': 0.9
                                }
                            }
                        },
                        'fields': 'userEnteredFormat(textFormat,backgroundColor)'
                    }
                },
                {
                    'autoResizeDimensions': {
                        'dimensions': {
                            'sheetId': sheet_id,
                            'dimension': 'COLUMNS'
                        }
                    }
                },
                {
                    'updateSheetProperties': {
                        'properties': {
                            'sheetId': sheet_id,
                            'gridProperties': {
                                'frozenRowCount': 1
                            }
                        },
                        'fields': 'gridProperties.frozenRowCount'
                    }
                }
            ]
            
            body = {
                'requests': requests
            }
            
            self.service.spreadsheets().batchUpdate(
                spreadsheetId=self.spreadsheet_id,
                body=body
            ).execute()
            
            print("Sheet formatting applied successfully")
            return True
            
        except HttpError as e:
            print(f"Error formatting sheet: {e}")
            return False
    
    def create_summary_sheet(self, summary_data: Dict) -> bool:
        """Create a summary sheet with statistics"""
        if not self.service or not summary_data:
            return False
        
        try:
            # Prepare summary data
            summary_sheet_data = [
                ['AI Words Mining System - Summary Report'],
                ['Generated:', datetime.now().strftime('%Y-%m-%d %H:%M:%S')],
                [''],
                ['Statistics:'],
                ['Total Words:', str(summary_data.get('total_words', 0))],
                ['Emerging Terms:', str(summary_data.get('emerging_terms_count', 0))],
                ['Average Trend Score:', str(summary_data.get('average_trend_score', 0))],
                [''],
                ['Categories:']
            ]
            
            # Add category breakdown
            categories = summary_data.get('categories', {})
            for category, count in categories.items():
                summary_sheet_data.append([category, str(count)])
            
            # Add importance distribution
            summary_sheet_data.extend([
                [''],
                ['Importance Distribution:']
            ])
            
            importance_dist = summary_data.get('importance_distribution', {})
            for importance, count in importance_dist.items():
                summary_sheet_data.append([importance.title(), str(count)])
            
            # Update summary sheet
            summary_range = 'Summary!A1:B20'
            return self.update_sheet(summary_sheet_data, summary_range, clear_first=True)
            
        except Exception as e:
            print(f"Error creating summary sheet: {e}")
            return False
    
    def update_words_and_summary(self, words_data: List[Dict], summary_data: Dict) -> bool:
        """Update both words data and summary in Google Sheets"""
        if not self.service:
            print("Google Sheets service not available")
            return False
        
        success = True
        
        # Prepare and update words data
        sheet_data = self.prepare_sheet_data(words_data)
        if not self.update_sheet(sheet_data):
            success = False
        
        # Format the main sheet
        if not self.format_sheet():
            print("Warning: Sheet formatting failed")
        
        # Create summary sheet
        if not self.create_summary_sheet(summary_data):
            print("Warning: Summary sheet creation failed")
            success = False
        
        if success:
            sheet_info = self.get_sheet_info()
            if sheet_info:
                print(f"Successfully updated Google Sheets: {sheet_info['title']}")
                print(f"Sheet URL: {sheet_info['url']}")
            else:
                print("Successfully updated Google Sheets")
        
        return success
    
    def test_connection(self) -> bool:
        """Test the Google Sheets connection"""
        if not self.service:
            print("Google Sheets service not available")
            return False
        
        try:
            sheet_info = self.get_sheet_info()
            if sheet_info:
                print(f"✓ Connected to Google Sheets: {sheet_info['title']}")
                print(f"  Available sheets: {', '.join(sheet_info['sheets'])}")
                print(f"  URL: {sheet_info['url']}")
                return True
            else:
                print("✗ Failed to get sheet information")
                return False
                
        except Exception as e:
            print(f"✗ Connection test failed: {e}")
            return False
    
    def backup_current_data(self) -> Optional[List[List[str]]]:
        """Backup current data from the sheet"""
        if not self.service:
            return None
        
        try:
            result = self.service.spreadsheets().values().get(
                spreadsheetId=self.spreadsheet_id,
                range=self.range_name
            ).execute()
            
            values = result.get('values', [])
            if values:
                print(f"Backed up {len(values)} rows of data")
                return values
            else:
                print("No data found to backup")
                return []
                
        except HttpError as e:
            print(f"Error backing up data: {e}")
            return None

if __name__ == "__main__":
    # Test the Google Sheets integration
    sheets_integration = GoogleSheetsIntegration()
    
    # Test connection
    if sheets_integration.test_connection():
        print("Google Sheets integration test passed!")
        
        # Sample test data
        sample_words = [
            {
                'word': 'Test Word',
                'category': 'Test Category',
                'definition': 'Test definition',
                'importance': 'medium',
                'trend_potential': 7,
                'business_value': 'high',
                'is_emerging': True,
                'extraction_count': 1,
                'ranking_score': 45.5,
                'first_seen': datetime.now().isoformat(),
                'last_seen': datetime.now().isoformat(),
                'related_terms': ['term1', 'term2'],
                'target_sectors': ['AI', 'Tech'],
                'contexts': ['context1', 'context2']
            }
        ]
        
        sample_summary = {
            'total_words': 1,
            'emerging_terms_count': 1,
            'average_trend_score': 7.0,
            'categories': {'Test Category': 1},
            'importance_distribution': {'medium': 1}
        }
        
        # Test update
        if sheets_integration.update_words_and_summary(sample_words, sample_summary):
            print("Test data updated successfully!")
        else:
            print("Test data update failed!")
    else:
        print("Google Sheets integration test failed!") 