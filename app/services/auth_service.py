import json
import os
from app.core.security import hash_password, verify_password, create_access_token

USERS_FILE = "app/db/users.json"


class AuthService:

    def load_users(self):
        if not os.path.exists(USERS_FILE):
            return []
        with open(USERS_FILE, "r") as f:
            return json.load(f)

    def save_users(self, users):
        with open(USERS_FILE, "w") as f:
            json.dump(users, f, indent=2)

    def register(self, username, email, password):
        users = self.load_users()

        for user in users:
            if user["email"] == email:
                raise Exception("User already exists")

        new_user = {
            "username": username,
            "email": email,
            "password": hash_password(password)
        }

        users.append(new_user)
        self.save_users(users)

        return {"message": "User registered successfully"}

    def login(self, email, password):
        users = self.load_users()

        for user in users:
            if user["email"] == email:
                if verify_password(password, user["password"]):
                    token = create_access_token({"sub": email})
                    return {"access_token": token}

        raise Exception("Invalid credentials")