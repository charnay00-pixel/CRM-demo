from werkzeug.security import check_password_hash

# 2. KONTA UŻYTKOWNIKÓW (Prototyp: stałe konta w kodzie, hasła zahaszowane.
# Docelowo do przeniesienia na prawdziwą tabelę użytkowników / zewnętrzny provider auth.)
USERS = {
    "aleks": {
        "username": "aleks",
        "password_hash": "scrypt:32768:8:1$U0GJiCqS6h7qZsw9$8d8a4056bf7e6a0261fc2ba30375d4865e4413ab87301d84679acd3b200b32aeb2971e6644effacb440639cd170f8e5fd6160481d78481fa1a1394b192940078",
        "role": "recruiter",
        "recruiter_name": "Aleks",
        "display_name": "Aleks",
    },
    "marta": {
        "username": "marta",
        "password_hash": "scrypt:32768:8:1$7biPDc4MyI51T5iG$c599a4ff813528c7d003d5cb6637eeb0752beb3e028f585a0cb9435ef105e35d91cfa412aafd21bb8dd7e883957285d8112718d0b29c1e531a4c7583441990a3",
        "role": "recruiter",
        "recruiter_name": "Marta",
        "display_name": "Marta",
    },
    "tomasz": {
        "username": "tomasz",
        "password_hash": "scrypt:32768:8:1$uZqfRAdzU4uLfsTy$c4337d74d24f78a815f79fdcb0622de39dfd936e3b4482954634867d6544564a003ecf84ffabe8d42055bfa618def868bccd922d48ab275fd07b0be0b193025b",
        "role": "recruiter",
        "recruiter_name": "Tomasz",
        "display_name": "Tomasz",
    },
    "admin": {
        "username": "admin",
        "password_hash": "scrypt:32768:8:1$RlInkr8Er0jo9VeX$992181aab6fc77d95141d1de293c1dd73337d83405fc6363098723c475ab02530620d48e37512b1b9c99bb564c76e11c9fcb502d1e16306371cde2130b4d18cb",
        "role": "admin",
        "recruiter_name": None,
        "display_name": "Admin",
    },
}


def verify_login(username, password):
    user = USERS.get(username.lower())
    if user and check_password_hash(user["password_hash"], password):
        return user
    return None


def get_user(username):
    return USERS.get(username)
