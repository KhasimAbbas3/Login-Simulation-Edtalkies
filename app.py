from flask import Flask, request, jsonify, render_template
import pyrebase

app = Flask(__name__)

# ---------------- FIREBASE CONFIG ----------------
firebaseConfig = {
    "apiKey": "AIzaSyCkEUrCH7BW79cyfwd4r-kyl7VWgX5BFCQ",
    "authDomain": "login-auth-simulation.firebaseapp.com",
    "projectId": "login-auth-simulation",
    "storageBucket": "login-auth-simulation.appspot.com",
    "databaseURL": "https://login-auth-simulation-default-rtdb.asia-southeast1.firebasedatabase.app/",
    "messagingSenderId": "141271958530",
    "appId": "1:141271958530:web:4f5ffebd3dcca9ad86131b"
}

firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()

# ---------------- FRONTEND ----------------
@app.route("/")
def home():
    return render_template("index.html")

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

# ---------------- SIGNUP API ----------------
@app.route("/signup", methods=["POST"])
def signup():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        auth.create_user_with_email_and_password(email, password)
        return jsonify({"message": "Signup successful"}), 201

    except Exception as e:
        if "EMAIL_EXISTS" in str(e):
            return jsonify({"message": "Email already exists"}), 409
        return jsonify({"message": "Signup failed"}), 400

# ---------------- LOGIN API ----------------
@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    email = data.get("email")
    password = data.get("password")

    try:
        user = auth.sign_in_with_email_and_password(email, password)
        return jsonify({
            "message": "Login successful",
            "idToken": user["idToken"]
        }), 200

    except Exception as e:
        if "INVALID_PASSWORD" in str(e):
            return jsonify({"message": "Invalid password"}), 401
        if "EMAIL_NOT_FOUND" in str(e):
            return jsonify({"message": "Email not found"}), 404
        return jsonify({"message": "Login failed"}), 400


if __name__ == "__main__":
    app.run(debug=True)
