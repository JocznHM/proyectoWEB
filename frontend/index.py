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

@app.route('/curso')
def course():
    if not validateSession():
        return redirect(url_for('login'))
    current_user = session['email']
    return render_template('course.html', current_user=current_user)

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

@app.route('/carrito')
def cart():
    if not validateSession():
        return redirect(url_for('login'))
    current_user = session['email']
    return render_template('carrito.html', current_user=current_user)

@app.route("/get_token", methods=["GET"])
def get_token():
    return session['token']

@app.route('/agregar_carrito', methods=['POST'])
def add_to_cart():
    # Obtener el curso a agregar desde el cuerpo de la solicitud
    data = request.get_json()
    course_id = data['course_id']
    
    if not course_id:
        return jsonify({"error": "No course_id provided"}), 400

    # Inicializar la lista 'cart' en la sesión si no existe
    if 'cart' not in session:
        session['cart'] = []

    # Agregar el curso a la lista 'cart'
    session['cart'].append(course_id)
    
    # Guardar la sesión
    session.modified = True

    return jsonify({"msg": "Curso agregado al carrito", "cart": session['cart']}), 200


@app.route('/eliminar_carrito', methods=['POST'])
def remove_from_cart():
    # Obtener el curso a eliminar desde el cuerpo de la solicitud
    data = request.get_json()
    course_id = data['course_id']
    
    if not course_id:
        return jsonify({"error": "No course_id provided"}), 400

    # Inicializar la lista 'cart' en la sesión si no existe
    if 'cart' not in session:
        session['cart'] = []

    # Eliminar el curso de la lista 'cart'
    session['cart'].remove(course_id)
    
    # Guardar la sesión
    session.modified = True

    return jsonify({"msg": "Curso eliminado del carrito", "cart": session['cart']}), 200

@app.route('/get_carrito', methods=['GET'])
def get_cart():
    # Obtener la lista 'cart' de la sesión
    cart = session.get('cart', [])
    return jsonify({"cart": cart}), 200

@app.route('/limpiar_carrito', methods=['GET'])
def clear_cart():
    # Eliminar la lista 'cart' de la sesión
    session.pop('cart', None)
    return jsonify({"msg": "Carrito limpiado"}), 200

if __name__ == '__main__':
    app.run(debug=True, port=5000)