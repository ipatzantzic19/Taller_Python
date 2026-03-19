# Manual explicativo de app.py (linea por linea)

Este documento explica que hace cada linea de [app.py](app.py) y por que existe.

## Codigo base analizado

```python
from flask import Flask, Blueprint, render_template, request

app = Flask(__name__)
bp = Blueprint('main', __name__, template_folder='templates')

# -- Rutas simples -------------------------------------------
@bp.route('/')
def home():
    return render_template('home.html', var1="¡Bienvenido!")

@bp.route('/inicio')
def inicio():
    return render_template('inicio.html')

# -- Login ----------------------------------------------------
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']
        # (aqui ira la logica con MongoDB)
        return render_template('login.html', var1="Sin BD por ahora")
    return render_template('login.html')

# -- Register -------------------------------------------------
@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']
        # (aqui ira la logica con MongoDB)
        return render_template('register.html', var1="Registrado!")
    return render_template('register.html')

app.register_blueprint(bp)

if __name__ == "__main__":
    app.run(port=5000, debug=True)
```

## Explicacion linea por linea

1. from flask import Flask, Blueprint, render_template, request
Por que: importa las herramientas minimas que usa la app.
Que hace: Flask crea la aplicacion, Blueprint organiza rutas, render_template carga HTML, request lee datos enviados por formularios.

2. (linea vacia)
Por que: separa visualmente imports de la configuracion.
Que hace: no ejecuta logica, solo mejora lectura.

3. app = Flask(__name__)
Por que: Flask necesita una instancia principal para saber donde inicia la app.
Que hace: crea el objeto app que ejecutara rutas y servidor.

4. bp = Blueprint('main', __name__, template_folder='templates')
Por que: ayuda a agrupar rutas en un modulo reutilizable.
Que hace: crea un blueprint llamado main y le indica donde estan las plantillas HTML.

5. (linea vacia)
Por que: separa configuracion de rutas.
Que hace: solo formato.

6. # -- Rutas simples -------------------------------------------
Por que: etiqueta visual para identificar bloque de rutas basicas.
Que hace: comentario, no ejecuta codigo.

7. @bp.route('/')
Por que: define la URL raiz del sitio.
Que hace: asocia la ruta / con la funcion home.

8. def home():
Por que: cada ruta necesita una funcion que responda.
Que hace: declara la funcion ejecutada al entrar a /.

9. return render_template('home.html', var1="¡Bienvenido!")
Por que: se quiere devolver una pagina HTML y un mensaje para mostrar.
Que hace: renderiza home.html y envia la variable var1 al template.

10. (linea vacia)
Por que: separa funciones distintas.
Que hace: formato.

11. @bp.route('/inicio')
Por que: agrega una ruta adicional para la pagina inicio.
Que hace: conecta la URL /inicio con la funcion inicio.

12. def inicio():
Por que: endpoint necesita funcion asociada.
Que hace: define la funcion que responde en /inicio.

13. return render_template('inicio.html')
Por que: se desea mostrar la vista de inicio.
Que hace: devuelve el template inicio.html sin variables extra.

14. (linea vacia)
Por que: separa secciones de la app.
Que hace: formato.

15. # -- Login ----------------------------------------------------
Por que: marca inicio del bloque de autenticacion de login.
Que hace: comentario.

16. @bp.route('/login', methods=['GET', 'POST'])
Por que: login necesita mostrar formulario (GET) y procesarlo (POST).
Que hace: habilita ambos metodos HTTP en la misma ruta.

17. def login():
Por que: ruta necesita funcion manejadora.
Que hace: define controlador de login.

18. if request.method == 'POST':
Por que: se debe distinguir entre abrir formulario y enviar datos.
Que hace: entra a procesar solo cuando se envio el formulario.

19. email    = request.form['email']
Por que: para autenticar, se necesita el correo enviado por el usuario.
Que hace: extrae el campo email del formulario.

20. password = request.form['password']
Por que: tambien se requiere la contrasena para validar acceso.
Que hace: extrae el campo password del formulario.

21. # (aqui ira la logica con MongoDB)
Por que: recuerda el punto donde ira la consulta real a la base de datos.
Que hace: comentario de pendiente tecnico.

22. return render_template('login.html', var1="Sin BD por ahora")
Por que: mientras no hay base de datos, se muestra estado temporal.
Que hace: vuelve a login.html con mensaje de demostracion.

23. return render_template('login.html')
Por que: cuando es GET, se debe mostrar el formulario vacio.
Que hace: renderiza login.html sin mensaje especial.

24. (linea vacia)
Por que: separa login y registro para legibilidad.
Que hace: formato.

25. # -- Register -------------------------------------------------
Por que: marca el bloque de registro de usuarios.
Que hace: comentario.

26. @bp.route('/register', methods=['GET', 'POST'])
Por que: registro igual requiere mostrar formulario y procesar envio.
Que hace: configura la ruta /register para GET y POST.

27. def register():
Por que: controlador para la ruta de registro.
Que hace: define funcion de alta de usuarios.

28. if request.method == 'POST':
Por que: solo en envio real se capturan y guardan datos.
Que hace: condiciona la logica de registro al metodo POST.

29. name     = request.form['name']
Por que: registro necesita nombre del usuario.
Que hace: toma el campo name del formulario.

30. email    = request.form['email']
Por que: correo suele ser identificador unico de usuario.
Que hace: obtiene el email desde el formulario.

31. password = request.form['password']
Por que: credencial necesaria para acceso futuro.
Que hace: obtiene la contrasena enviada.

32. # (aqui ira la logica con MongoDB)
Por que: indica donde se insertara el usuario en base de datos.
Que hace: comentario de futura implementacion.

33. return render_template('register.html', var1="Registrado!")
Por que: confirma visualmente que el registro se proceso.
Que hace: retorna la vista con mensaje de exito.

34. return render_template('register.html')
Por que: en GET solo muestra formulario limpio.
Que hace: devuelve register.html sin mensaje.

35. (linea vacia)
Por que: separa rutas de configuracion final.
Que hace: formato.

36. app.register_blueprint(bp)
Por que: sin registrar el blueprint, Flask no conoce esas rutas.
Que hace: conecta todas las rutas de bp a la aplicacion principal.

37. (linea vacia)
Por que: separa definicion de app de arranque del servidor.
Que hace: formato.

38. if __name__ == "__main__":
Por que: evita que el servidor arranque al importar este archivo desde otro modulo.
Que hace: ejecuta el bloque solo cuando se corre directamente app.py.

39. app.run(port=5000, debug=True)
Por que: inicia servidor local para desarrollo y facilita depuracion.
Que hace: levanta Flask en puerto 5000 y activa recarga/errores detallados con debug.

## Resumen rapido para explicar en clase

- Importas herramientas Flask.
- Creas app y blueprint para organizar rutas.
- Defines rutas para paginas simples.
- Defines login y register con GET y POST.
- Tomas datos del formulario con request.form.
- Devuelves templates con mensajes de estado.
- Registras blueprint.
- Inicias servidor solo si ejecutas el archivo directamente.
