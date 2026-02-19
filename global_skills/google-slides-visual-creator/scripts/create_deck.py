import os
import sys
import json
import pickle
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

SCOPES = ['https://www.googleapis.com/auth/presentations', 'https://www.googleapis.com/auth/drive.file']
BASE_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CREDENTIALS_PATH = os.path.join(BASE_PATH, "resources", "credentials.json")
TOKEN_PATH = os.path.join(BASE_PATH, "resources", "token.pickle")

THEMES = {
    "Corporate Future": {
        "bg": {"color": {"rgbColor": {"red": 0.05, "green": 0.07, "blue": 0.1}}},
        "title_text": {"rgbColor": {"red": 0.0, "green": 0.8, "blue": 1.0}},
        "body_text": {"rgbColor": {"red": 0.9, "green": 0.9, "blue": 0.9}},
        "accent": {"rgbColor": {"red": 1.0, "green": 0.0, "blue": 0.5}}
    }
}

def authenticate():
    creds = None
    if os.path.exists(TOKEN_PATH):
        with open(TOKEN_PATH, 'rb') as token:
            creds = pickle.load(token)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_PATH, SCOPES)
            creds = flow.run_local_server(port=0)
        with open(TOKEN_PATH, 'wb') as token:
            pickle.dump(creds, token)
    return creds

def create_visual_deck(title, slides_data, mood="Corporate Future"):
    creds = authenticate()
    service = build('slides', 'v1', credentials=creds)
    theme = THEMES.get(mood, THEMES["Corporate Future"])
    
    presentation = service.presentations().create(body={'title': title}).execute()
    presentation_id = presentation.get('presentationId')
    
    requests = []
    for i, slide in enumerate(slides_data):
        page_id = f"page_{i}"
        title_id = f"title_{i}"
        body_id = f"body_{i}"
        accent_id = f"accent_{i}"
        
        requests.append({'createSlide': {'objectId': page_id, 'insertionIndex': str(i), 'slideLayoutReference': {'predefinedLayout': 'BLANK'}}})
        requests.append({'updatePageProperties': {'objectId': page_id, 'pageProperties': {'pageBackgroundFill': {'solidFill': theme['bg']}}, 'fields': 'pageBackgroundFill'}})
        
        # Decorative line
        requests.append({'createShape': {'objectId': accent_id, 'shapeType': 'RECTANGLE', 'elementProperties': {'pageObjectId': page_id, 'size': {'height': {'magnitude': 3, 'unit': 'PT'}, 'width': {'magnitude': 150, 'unit': 'PT'}}, 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 100, 'unit': 'PT'}}}})
        requests.append({'updateShapeProperties': {'objectId': accent_id, 'shapeProperties': {'shapeBackgroundFill': {'solidFill': {'color': theme['accent']}}}, 'fields': 'shapeBackgroundFill'}})

        # Title Text
        requests.append({'createShape': {'objectId': title_id, 'shapeType': 'TEXT_BOX', 'elementProperties': {'pageObjectId': page_id, 'size': {'height': {'magnitude': 60, 'unit': 'PT'}, 'width': {'magnitude': 600, 'unit': 'PT'}}, 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 40, 'unit': 'PT'}}}})
        requests.append({'insertText': {'objectId': title_id, 'text': slide['title']}})
        requests.append({'updateTextStyle': {'objectId': title_id, 'style': {'fontSize': {'magnitude': 32, 'unit': 'PT'}, 'bold': True, 'foregroundColor': {'opaqueColor': theme['title_text']}}, 'fields': 'fontSize,bold,foregroundColor'}})

        # Body Text
        requests.append({'createShape': {'objectId': body_id, 'shapeType': 'TEXT_BOX', 'elementProperties': {'pageObjectId': page_id, 'size': {'height': {'magnitude': 250, 'unit': 'PT'}, 'width': {'magnitude': 600, 'unit': 'PT'}}, 'transform': {'scaleX': 1, 'scaleY': 1, 'translateX': 50, 'translateY': 130, 'unit': 'PT'}}}})
        requests.append({'insertText': {'objectId': body_id, 'text': slide['content']}})
        requests.append({'updateTextStyle': {'objectId': body_id, 'style': {'fontSize': {'magnitude': 16, 'unit': 'PT'}, 'foregroundColor': {'opaqueColor': theme['body_text']}}, 'fields': 'fontSize,foregroundColor'}})

    service.presentations().batchUpdate(presentationId=presentation_id, body={'requests': requests}).execute()
    return f"https://docs.google.com/presentation/d/{presentation_id}/edit"

if __name__ == "__main__":
    if len(sys.argv) > 1:
        try:
            data = json.loads(sys.argv[1])
            print(f"REAL_LINK: {create_visual_deck(data['title'], data['slides'], data.get('mood'))}")
        except Exception as e: print(f"Error: {str(e)}")
