import imac_main.scripts.database as database
from firebase_admin import auth as fbauth
from firebase_admin import credentials, initialize_app
import pyrebase


config = {
    "apiKey":"AIzaSyC5Yyxkj-6CfyrBnJcznfVc20g87orCEy0",
    "authDomain": "i-mac-portal-lab-database.firebaseapp.com",
  "projectId": "i-mac-portal-lab-database",
  "storageBucket": "i-mac-portal-lab-database.appspot.com",
  "messagingSenderId": "818726947492",
  "appId": "1:818726947492:web:1f4b1568d8a1d4c258b431",
  "measurementId": "G-W1J9P85D3Y",
  "databaseURL": "https://i-mac-portal-lab-database-default-rtdb.asia-southeast1.firebasedatabase.app/",
  "serviceAccount": "imac_main/scripts/serviceAccountKey.json"
}



firebase = pyrebase.initialize_app(config)

cred = credentials.Certificate('imac_main/scripts/serviceAccountKey.json')
initialize_app(cred, {
    'databaseURL': 'https://i-mac-portal-lab-database-default-rtdb.asia-southeast1.firebasedatabase.app/'
})

auth = firebase.auth()

def fbsignup(name, email, acc_type, password):
    user = fbauth.create_user(
        email=email,
        email_verified=False,
        password=password,
        disabled=False)
    database.fbsignupwrite(user.uid, name, email, acc_type, password)
    return user.uid

def fblogin(email, password):
    print(auth)
    try:
        user = auth.sign_in_with_email_and_password(email, password)
        approved = database.fbloginread(user['localId'])
        name = approved["name"]
        acc_type = approved["type"]
        if approved["approved"]:
            return user, name, acc_type, True
        else:
            return user, name, acc_type, False
    except Exception as e:
        print(e)
        return None
    

def fblogout():
    auth.current_user = None
    return None