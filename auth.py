from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()

users = {
    "admin": "s3cur3p@ss",  # Cambia con le tue credenziali
    "gatto": "mia0w!"
}

@auth.verify_password
def verify_password(username, password):
    if username in users and users[username] == password:
        return username
    return None
