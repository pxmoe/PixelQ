from shutil import copyfile
from flask import Flask, send_from_directory, request, jsonify, session, redirect, url_for, send_file
from authlib.integrations.flask_client import OAuth
from werkzeug.utils import secure_filename
from dotenv import load_dotenv
import os, json, io, tempfile
import numpy as np
from PIL import Image
import cv2
import pytesseract





# Tesseract path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

load_dotenv()

app = Flask(__name__)
app.secret_key = 'supersecret'

UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

oauth = OAuth(app)
google = oauth.register(
    name='google',
    client_id=os.getenv("GOOGLE_CLIENT_ID"),
    client_secret=os.getenv("GOOGLE_CLIENT_SECRET"),
    access_token_url='https://accounts.google.com/o/oauth2/token',
    authorize_url='https://accounts.google.com/o/oauth2/auth',
    api_base_url='https://www.googleapis.com/oauth2/v1/',
    userinfo_endpoint='https://openidconnect.googleapis.com/v1/userinfo',
    client_kwargs={'scope': 'email profile'},
)

USER_FILE = 'users.json'

def load_users():
    return json.load(open(USER_FILE)) if os.path.exists(USER_FILE) else {}

def save_users(users):
    json.dump(users, open(USER_FILE, 'w'), indent=2)

def create_user(name, email, password):
    users = load_users()
    if email in users:
        return False, "User already exists"
    users[email] = {
        "username": name,
        "password": password
    }
    save_users(users)
    return True, "Account created"

def authenticate(email, password):
    users = load_users()
    return email in users and users[email]['password'] == password

def get_user(email):
    return load_users().get(email)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in {'png', 'jpg', 'jpeg', 'mp4'}


@app.route('/')
def index():
    return send_from_directory('public', 'dashboard.html')

@app.route('/dashboard')
def dashboard():
    return send_from_directory('public', 'dashboard.html')

@app.route('/signup')
def signup():
    return send_from_directory('public', 'signup.html')

@app.route('/login')
def login_page():
    return send_from_directory('public', 'login.html')

@app.route('/<path:path>')
def static_proxy(path):
    return send_from_directory('public', path)

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    if authenticate(data['email'], data['password']):
        session['user'] = data['email']
        return jsonify(success=True)
    return jsonify(success=False, error="Invalid credentials")

@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    success, msg = create_user(data['name'], data['email'], data['password'])
    if success:
        session['user'] = data['email']
        return jsonify(success=True)
    return jsonify(success=False, error=msg)

@app.route('/logout')
def logout():
    session.pop('user', None)
    return redirect('/dashboard')

@app.route('/user_info')
def user_info():
    if 'user' not in session:
        return jsonify({"logged_in": False})
    user = get_user(session['user'])
    return jsonify({
        "logged_in": True,
        "email": session['user'],
        "username": user.get("username", "")
    })

@app.route('/auth/google')
def auth_google():
    redirect_uri = url_for('auth_google_callback', _external=True)
    return google.authorize_redirect(redirect_uri)

@app.route('/auth/google/callback')
def auth_google_callback():
    token = google.authorize_access_token()
    resp = google.get('userinfo')
    user_info = resp.json()

    email = user_info['email']
    name = user_info.get('name', 'Google User')

    users = load_users()
    if email not in users:
        users[email] = {
            "username": name,
            "password": None
        }
        save_users(users)

    session['user'] = email
    return redirect('/dashboard')

@app.route("/remove_watermark_lama", methods=["POST"])
def remove_watermark_lama():
    if "file" not in request.files or "mask" not in request.files:
        return jsonify({"error": "File and mask are required"}), 400

    image_file = request.files["file"]
    mask_file = request.files["mask"]

    # Use a safe filename for image
    filename = secure_filename(image_file.filename)
    image_path = os.path.join(UPLOAD_FOLDER, filename)
    image_file.save(image_path)

    try:
        # ✅ Load input image using PIL (handles JPGs safely)
        image = Image.open(image_path).convert("RGB")
        image_np = np.array(image)

        # ✅ Load mask (grayscale), ensure dimensions match
        mask = Image.open(mask_file).convert("L")
        mask_np = np.array(mask)

        if mask_np.shape != image_np.shape[:2]:
            return jsonify({"error": "Mask size must match image size"}), 400
        
        # Save files to debug
        Image.fromarray(image_np).save("debug_image.png")
        Image.fromarray(mask_np).save("debug_mask.png")
        print("✅ Saved debug_image.png and debug_mask.png")


        # ✅ Send to LaMa for inpainting
        from lama_client import send_to_lama
        result = send_to_lama(image_np, mask_np)

        # ✅ Save result as PNG regardless of original format
        result_path = os.path.join(PROCESSED_FOLDER, f"lama_{os.path.splitext(filename)[0]}.png")
        cv2.imwrite(result_path, cv2.cvtColor(result, cv2.COLOR_RGB2BGR))

        return send_file(result_path, mimetype="image/png")

    except Exception as e:
       import traceback
       print("❌ Error during inpainting:", str(e))
       traceback.print_exc()
       return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
