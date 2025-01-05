from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from flask import session, request, url_for

# Path to client_secret.json file downloaded from Google Cloud Console
GOOGLE_CLIENT_SECRETS_FILE = "client_secret.json"
SCOPES = ["openid", "https://www.googleapis.com/auth/userinfo.profile", "https://www.googleapis.com/auth/userinfo.email"]


def create_login_flow():
    """Create the login flow with Google's OAuth."""
    flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES)
    flow.redirect_uri = url_for("callback", _external=True)
    return flow


def get_authorization_url():
    """Generate the authorization URL for user login."""
    flow = create_login_flow()
    authorization_url, state = flow.authorization_url(prompt="consent")
    session["state"] = state
    return authorization_url


def handle_oauth_callback():
    """Handle the callback after user authorization."""
    state = session["state"]
    flow = InstalledAppFlow.from_client_secrets_file(GOOGLE_CLIENT_SECRETS_FILE, scopes=SCOPES, state=state)
    flow.redirect_uri = url_for("callback", _external=True)
    flow.fetch_token(authorization_response=request.url)

    credentials = flow.credentials
    session["credentials"] = credentials_to_dict(credentials)

    service = build("oauth2", "v2", credentials=credentials)
    user_info = service.userinfo().get().execute()

    return user_info


def logout_user():
    """Clear session data to log out the user."""
    session.pop("credentials", None)
    session.pop("user", None)


def credentials_to_dict(credentials):
    """ converts the user's credentials into a dictionary object """
    return {
        "token": credentials.token,
        "refresh_token": credentials.refresh_token,
        "token_uri": credentials.token_uri,
        "client_id": credentials.client_id,
        "client_secret": credentials.client_secret,
        "scopes": credentials.scopes,
    }