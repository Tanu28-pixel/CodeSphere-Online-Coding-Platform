from flask import Flask, request, jsonify
from flask_cors import CORS, cross_origin
import subprocess
import tempfile
import json
import os

app = Flask(__name__)

# FULL CORS FIX
CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)


# ------------------------ DATABASE FILE ------------------------

DB_FILE = "users.json"

def load_db():
    if not os.path.exists(DB_FILE):
        with open(DB_FILE, "w") as f:
            json.dump({"users": []}, f)
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)


# ------------------------ AUTH ENDPOINTS ------------------------

@app.route('/signup', methods=['POST'])
@cross_origin()
def signup():
    data = request.json
    username = data["username"]
    password = data["password"]

    db = load_db()

    for u in db["users"]:
        if u["username"] == username:
            return jsonify({"error": "User already exists"}), 400

    db["users"].append({
        "username": username,
        "password": password,
        "saved_code": []
    })

    save_db(db)
    return jsonify({"message": "Signup successful!"})


@app.route('/login', methods=['POST'])
@cross_origin()
def login():
    data = request.json
    username = data["username"]
    password = data["password"]

    db = load_db()

    for u in db["users"]:
        if u["username"] == username and u["password"] == password:
            return jsonify({"token": username})

    return jsonify({"error": "Invalid username or password"}), 400


# ------------------------ SAVE CODE ENDPOINT ------------------------

@app.route('/save_code', methods=['POST'])
@cross_origin()
def save_code():
    data = request.json
    username = data["username"]
    language = data["language"]
    code = data["code"]

    db = load_db()

    for u in db["users"]:
        if u["username"] == username:
            u["saved_code"].append({
                "language": language,
                "code": code
            })
            save_db(db)
            return jsonify({"message": "Code saved successfully!"})

    return jsonify({"error": "User not found"}), 400


# ------------------------ CODE EXECUTION ------------------------

def run_python(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.py') as tmp:
        tmp.write(code.encode())
        tmp.flush()
        try:
            result = subprocess.run(["python", tmp.name], capture_output=True, text=True, timeout=5)
            return result.stdout + result.stderr
        except Exception as e:
            return str(e)


def run_c(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.c') as src:
        src.write(code.encode())
        src.flush()

        exe = src.name + ".exe"
        compile_cmd = ["gcc", src.name, "-o", exe]
        run = subprocess.run(compile_cmd, capture_output=True, text=True)

        if run.returncode != 0:
            return run.stderr

        output = subprocess.run([exe], capture_output=True, text=True)
        return output.stdout + output.stderr


def run_cpp(code):
    with tempfile.NamedTemporaryFile(delete=False, suffix='.cpp') as src:
        src.write(code.encode())
        src.flush()

        exe = src.name + ".exe"
        compile_cmd = ["g++", src.name, "-o", exe]
        run = subprocess.run(compile_cmd, capture_output=True, text=True)

        if run.returncode != 0:
            return run.stderr

        output = subprocess.run([exe], capture_output=True, text=True)
        return output.stdout + output.stderr


# ------------------------ RUN ENDPOINT ------------------------

@app.route('/run', methods=['POST'])
@cross_origin()
def run_code():
    data = request.json
    code = data["code"]
    language = data["language"]

    if language == "python":
        output = run_python(code)
    elif language == "c":
        output = run_c(code)
    elif language == "cpp":
        output = run_cpp(code)
    else:
        return jsonify({"error": "Unsupported language"}), 400

    return jsonify({"output": output})


# ------------------------ START FLASK SERVER ------------------------

if __name__ == "__main__":
    print("Backend started at http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
