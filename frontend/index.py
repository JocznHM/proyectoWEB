from flask import Flask, render_template, request, session, redirect, url_for,jsonify
from flask_cors import CORS


app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SESSION_COOKIE_NAME'] = "SESSION_DATA"
app.config["SECRET_KEY"] = "miclave"

def validateSession():
    if session.get('logged_in'):
        return True
    else:
        return False

@app.route('/')
def index():
    if validateSession():
        return redirect(url_for('dashboard'))
    else:
        return render_template('index.html')

@app.route('/login')
def login():
    if validateSession():
        return redirect(url_for('myCourses'))
    return render_template('signin.html')


@app.route('/signin', methods=['POST', 'GET'])
def signin():
    data = request.get_json()
    if data:
        print(data)
        session['logged_in'] = data['logged_in']
        session['email'] = data['email']
        session['token'] = data['token']
        msg = {
            "success": "datos agregados a la session",
        }
        print("session creada")
        return jsonify(msg)
    return jsonify({"msg": "data is empty"})

@app.route('/signup')
def signup():
    if validateSession():
        return redirect(url_for('/myCourses'))
    return render_template('signup.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/myCourses')
def dashboard():
    if not validateSession():
        return redirect(url_for('login'))
    current_user = session['email']
    print(current_user)
    return render_template('myCourses.html', current_user=current_user)

@app.route('/allCourses')
def all_courses():
    if not validateSession():
        return redirect(url_for('login'))
    current_user = session['email']
    return render_template('all_courses.html', current_user=current_user)

@app.route('/offers')
def offers():
    if not validateSession():
        return redirect(url_for('login'))
    current_user = session['email']
    return render_template('offers.html', current_user=current_user)

@app.route('/settings')
def settings():
    if not validateSession():
        return redirect(url_for('login'))
    current_user = session['email']
    return render_template('settings.html', current_user=current_user)

@app.route('/contact')
def contact():
    if not validateSession():
        return redirect(url_for('login'))
    current_user = session['email']
    return render_template('contact.html', current_user=current_user)

@app.route("/get_token", methods=["GET"])
def get_token():
    return session['token']

if __name__ == '__main__':
    app.run(debug=True, port=5000)