from flask import Flask
from flask import Flask, Blueprint, render_template, request



app = Flask(__name__)
blueprints = Blueprint('Renderer', __name__, template_folder='templates')

@app.route("/")
def home():
    return "Hola Flask"

@blueprints.route('/inicio')
def inicio():
    return render_template('inicio.html')


@blueprints.route('/fin')
def fin():
    return render_template('fin.html')

@blueprints.route('/tabla')
def tabla():
    return render_template('tabla.html')

@blueprints.route('/login')
def login():
    return render_template('login.html')


@app.route('/get', methods=['GET'])
def perticion_get():
    print("Hola Mundo")
    return "<h2>Hello World get<h2>"

@app.route('/get/<id>', methods=['GET'])
def _peticion_get2(id):
    print(id)
    return f"<p>El ID es <strong>{id} </strong> </p>"


#se pone en el html el "segundos" para que se pueda usar en el html
@blueprints.route('/tabla/<numero>')
def tabla_numero(numero):
    context = {"segundos": numero}
    return render_template('tabla_numero.html', var1=context)  



#====================================================================================================
#====================================================================================================

class User:
    def __init__(self, name, lastname, email, password):
        self.name = name
        self.lastname = lastname
        self.email = email
        self.password = password

global users
users = []


@blueprints.route('/login' , methods=['POST'])
def login_post():
    email = request.form['typeEmailX-2']
    password = request.form['typePasswordX-2']

    for user in users:
        if user.email == email and user.password == password:
            return render_template('home.html', var1="Bienvenido " + user.name + " " + user.lastname)
        else:
            return render_template('login.html', var1="Usuario o contraseña incorrectos")
        

    return render_template('login.html')

@blueprints.route('/register' , methods=['GET'])
def register():
    return render_template('register.html')

@blueprints.route('/register', methods=['POST'])
def register_post():
    name = request.form['form3Example1']
    lastname = request.form['form3Example2']
    email = request.form['form3Example3']
    password = request.form['form3Example4']

    user = User(name, lastname, email, password)
    users.append(user)

    print(name)
    return render_template('register.html', var1="Usuario registrado correctamente")

#====================================================================================================
#====================================================================================================


app.register_blueprint(blueprints)


if __name__ == "__main__":
    app.run(port=5000, debug=True)
