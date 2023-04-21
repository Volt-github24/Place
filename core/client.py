import requests

# Configuration de l'identifiant client et du secret client OAuth2
client_id = "690748159814-sh25urm0cjgshl1k684a2gol01g5sm4r.apps.googleusercontent.com"
client_secret = "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"

# Configuration de l'URI de redirection de votre application
redirect_uri = "https://place-676f9.web.app/oauth2_callback"

# Configuration des scopes d'API que votre application souhaite accéder
scopes = ["https://www.googleapis.com/auth/calendar.readonly", "https://www.googleapis.com/auth/gmail.readonly"]

# Construction de l'URL d'autorisation
auth_url = "https://accounts.google.com/o/oauth2/auth?" \
           "client_id={0}&redirect_uri={1}&response_type=code&scope={2}".format(client_id, redirect_uri, " ".join(scopes))

# Redirection de l'utilisateur vers l'URL d'autorisation
# L'utilisateur doit se connecter et autoriser l'accès de votre application aux API Google
print("Veuillez vous connecter et autoriser l'accès à l'URL suivante :")
print(auth_url)

# Récupération du code d'autorisation dans l'URI de redirection de votre application
authorization_code = input("Entrez le code d'autorisation : ")

# Échange du code d'autorisation contre un jeton d'authentification
token_url = "https://oauth2.googleapis.com/token"
token_data = {
    "code": authorization_code,
    "client_id": client_id,
    "client_secret": client_secret,
    "redirect_uri": redirect_uri,
    "grant_type": "authorization_code"
}
response = requests.post(token_url, data=token_data)

# Extraction du jeton d'authentification de la réponse
if response.status_code == 200:
    token = response.json()["access_token"]
    print("Token d'authentification : {0}".format(token))
else:
    print("Erreur lors de la récupération du jeton d'authentification : {0}".format(response.text))