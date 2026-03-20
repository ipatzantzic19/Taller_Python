from flask import Flask, Blueprint, render_template, request
from mongo_config import user_col
app = Flask(__name__)
bp = Blueprint('main', __name__, template_folder='templates')

# ── Rutas simples ───────────────────────────────────────────
@bp.route('/')
def home():
    return render_template('home.html', var1="¡Bienvenido!")

@bp.route('/inicio')
def inicio():
    return render_template('inicio.html')

# ── Login ────────────────────────────────────────────────────
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        
        user = user_col.find_one({"email": email, "password": password})

        if user:
            return render_template('home.html', var1 = "Bienvenido " + user["name"])
        else:          
            return render_template('login.html', var1="Credenciales incorrectas")
    return render_template('login.html')

# ── Register ─────────────────────────────────────────────────
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form.get('name')
        lastname = request.form.get('lastname')
        email    = request.form.get('email')
        password = request.form.get('password')
        
        if not name or not email or not password:
            return render_template('register.html', var1="Faltan datos obligatorios")
        
        if user_col.find_one({"email": email}):
            return render_template('register.html', var1="Email ya registrado")
        
        user_col.insert_one({
            "name": name,
            "lastname": lastname,
            "email": email,
            "password": password
        })
    
        return render_template('register.html', var1="Registrado!")
    return render_template('register.html')

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)