from flask import Flask, Blueprint, render_template, request

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
        # (aquí irá la lógica con MongoDB)
        return render_template('login.html', var1="Sin BD por ahora")
    return render_template('login.html')

# ── Register ─────────────────────────────────────────────────
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']
        # (aquí irá la lógica con MongoDB)
        return render_template('register.html', var1="Registrado!")
    return render_template('register.html')

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)