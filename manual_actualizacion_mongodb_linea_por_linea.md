# Manual nuevo: parte implementada (linea por linea)

Este manual explica solo lo nuevo que ya se implemento en el proyecto.
No repite Flask basico; se centra en integracion con MongoDB, login y registro.

## 1) Archivo: mongo_config.py

Codigo implementado:

```python
from pymongo import MongoClient

MONGO_URI = "mongodb+srv://ipatzantzic_db_user:tAtcJU9ofAYsSUmh@cluster0.c32wlgu.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["flask_app"]
users_col = db["users"]
```

Explicacion linea por linea:

1. from pymongo import MongoClient
   Por que se hizo: para tener el cliente oficial de MongoDB en Python.
   Para que sirve: abrir una conexion desde Flask hacia Atlas.

2. MONGO_URI = "..."
   Por que se hizo: centralizar la cadena de conexion en una variable.
   Para que sirve: indicar usuario, cluster y host de Atlas.

3. client = MongoClient(MONGO_URI)
   Por que se hizo: crear una sesion de conexion reutilizable.
   Para que sirve: ejecutar operaciones de lectura/escritura.

4. db = client["flask_app"]
   Por que se hizo: apuntar a la base de datos del proyecto.
   Para que sirve: separar datos de esta app de otras bases.

5. users_col = db["users"]
   Por que se hizo: definir la coleccion principal de usuarios.
   Para que sirve: insertar, buscar y validar cuentas.

## 2) Archivo: app.py (parte nueva implementada)

### 2.1 Import de coleccion MongoDB

Codigo:

```python
from mongo_config import users_col
```

Linea y razon:

1. from mongo_config import users_col
   Por que se hizo: reutilizar la conexion/configuracion en un solo lugar.
   Para que sirve: usar la coleccion users en login y register sin repetir codigo.

### 2.2 Login con validacion en MongoDB

Codigo implementado:

```python
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        user = users_col.find_one({"email": email, "password": password})

        if user:
            return render_template('home.html', var1="¡Bienvenido, " + user['name'])
        else:
            return render_template('login.html', var1="Credenciales incorrectas")
    return render_template('login.html')
```

Explicacion linea por linea:

1. @bp.route('/login', methods=['GET', 'POST'])
   Por que se hizo: manejar formulario en una sola ruta.
   Para que sirve: GET muestra vista, POST valida credenciales.

2. def login():
   Por que se hizo: crear controlador del endpoint /login.
   Para que sirve: contener toda la logica de inicio de sesion.

3. if request.method == 'POST':
   Por que se hizo: separar el envio del formulario de la carga inicial.
   Para que sirve: ejecutar validacion solo cuando usuario presiona Login.

4. email = request.form['email']
   Por que se hizo: capturar identificador del usuario.
   Para que sirve: buscar coincidencia en MongoDB.

5. password = request.form['password']
   Por que se hizo: capturar credencial ingresada.
   Para que sirve: comparar contra el documento guardado.

6. user = users_col.find_one({"email": email, "password": password})
   Por que se hizo: validar login con datos reales en base.
   Para que sirve: traer un usuario que cumpla ambas condiciones.

7. if user:
   Por que se hizo: verificar si Mongo encontro documento.
   Para que sirve: decidir flujo exitoso o error.

8. return render_template('home.html', var1="¡Bienvenido, " + user['name'])
   Por que se hizo: confirmar acceso correcto.
   Para que sirve: mostrar pantalla de inicio personalizada.

9. else:
   Por que se hizo: cubrir caso de credenciales invalidas.
   Para que sirve: regresar al login con mensaje de error.

10. return render_template('login.html', var1="Credenciales incorrectas")
    Por que se hizo: dar retroalimentacion al usuario.
    Para que sirve: indicar fallo sin romper la app.

11. return render_template('login.html')
    Por que se hizo: respuesta del metodo GET.
    Para que sirve: mostrar formulario vacio la primera vez.

### 2.3 Register con validacion y guardado en MongoDB

Codigo implementado:

```python
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form.get('name')
        lastname = request.form.get('lastname')
        email = request.form.get('email')
        password = request.form.get('password')

        if not name or not email or not password:
            return render_template('register.html', var1="Faltan datos obligatorios")

        if users_col.find_one({"email": email}):
            return render_template('register.html', var1="Email ya registrado")

        users_col.insert_one({
            "name": name,
            "lastname": lastname,
            "email": email,
            "password": password
        })

        return render_template('register.html', var1="Registrado!")
    return render_template('register.html')
```

Explicacion linea por linea:

1. @bp.route('/register', methods=['GET', 'POST'])
   Por que se hizo: usar una ruta para mostrar y procesar registro.
   Para que sirve: simplificar flujo del formulario.

2. def register():
   Por que se hizo: crear controlador de alta de usuarios.
   Para que sirve: concentrar reglas de negocio de registro.

3. if request.method == 'POST':
   Por que se hizo: ejecutar logica solo al enviar formulario.
   Para que sirve: evitar procesar datos cuando solo se abre la vista.

4. name = request.form.get('name')
   Por que se hizo: leer nombre enviado por el input name.
   Para que sirve: guardar nombre del usuario.

5. lastname = request.form.get('lastname')
   Por que se hizo: leer apellido como dato adicional.
   Para que sirve: tener perfil mas completo en la coleccion.

6. email = request.form.get('email')
   Por que se hizo: usar email como campo de unicidad logica.
   Para que sirve: identificar usuario en registro y login.

7. password = request.form.get('password')
   Por que se hizo: capturar credencial del nuevo usuario.
   Para que sirve: autenticar en login (version didactica).

8. if not name or not email or not password:
   Por que se hizo: validar datos obligatorios antes de tocar la BD.
   Para que sirve: evitar inserciones incompletas.

9. return render_template('register.html', var1="Faltan datos obligatorios")
   Por que se hizo: informar al usuario que complete campos.
   Para que sirve: mejorar UX y evitar errores silenciosos.

10. if users_col.find_one({"email": email}):
    Por que se hizo: prevenir registros duplicados por correo.
    Para que sirve: mantener consistencia de cuentas.

11. return render_template('register.html', var1="Email ya registrado")
    Por que se hizo: comunicar conflicto de email existente.
    Para que sirve: guiar al usuario a usar otro correo.

12. users_col.insert_one({...})
    Por que se hizo: persistir usuario en MongoDB.
    Para que sirve: que los datos no se pierdan al reiniciar Flask.

13. "name": name
    Por que se hizo: guardar nombre principal.
    Para que sirve: mostrar saludo y datos de perfil.

14. "lastname": lastname
    Por que se hizo: guardar apellido capturado.
    Para que sirve: completar informacion del usuario.

15. "email": email
    Por que se hizo: guardar correo para login/consulta.
    Para que sirve: buscar usuario rapidamente.

16. "password": password
    Por que se hizo: mantener compatibilidad con el flujo actual de clase.
    Para que sirve: validar acceso en login.

17. return render_template('register.html', var1="Registrado!")
    Por que se hizo: confirmar exito del alta.
    Para que sirve: feedback inmediato para el estudiante/usuario.

18. return render_template('register.html')
    Por que se hizo: respuesta del metodo GET.
    Para que sirve: mostrar formulario inicial.

## 3) Resumen de la actualizacion

- Se paso de datos en memoria a persistencia real en MongoDB.
- Login ahora valida contra coleccion users.
- Register ahora valida obligatorios, evita email duplicado e inserta documento.
- El campo lastname tambien se guarda cuando viene en el formulario.

## 4) Nota didactica importante

La contrasena se guarda en texto plano solo por simplificacion de clase.
En produccion se debe usar hash (por ejemplo, bcrypt) antes de guardar.
