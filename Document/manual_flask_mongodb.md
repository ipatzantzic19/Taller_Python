# 📖 Manual del Profesor — Flask + MongoDB
> **Duración total:** 1 hora 30 minutos  
> **Nivel:** Principiantes que ya conocen Flask básico

---

## 🗓️ Agenda (tiempos sugeridos)

| # | Bloque | Tiempo |
|---|--------|--------|
| 1 | Repaso de Flask + código limpio | 15 min |
| 2 | Teoría de MongoDB | 20 min |
| 3 | Demo en vivo: registro e inicio de sesión | 35 min |
| 4 | Kahoot | 10 min |
| — | Buffer / preguntas | 10 min |

---

## 🧹 Bloque 1 — Repaso Flask + código limpio (15 min)

### ¿Qué decir?
> "Antes de entrar a MongoDB, vamos a limpiar el código que ya tenemos para entender bien qué hace cada parte."

### Cambios al código original

**Problema 1: Dos blueprints con la misma ruta `/login`**
El código original define `/login` dos veces en el mismo Blueprint (una GET y una POST). Flask no lo permite así. Se debe usar el mismo nombre de función con `methods=['GET', 'POST']`.

**Problema 2: El `if __name__ == "__main__"` debe estar al final** ✔️ (ya lo está)

**Problema 3: `global users` e `users = []` en memoria** — esto es exactamente por qué vamos a usar MongoDB.

### Código limpio (app.py final)

```python
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
```

### Punto clave a destacar
> "El problema con el código anterior es que los usuarios se guardan en una **lista en memoria**. Cuando apagamos el servidor, ¡se pierden todos! MongoDB resuelve eso."

---

## 🍃 Bloque 2 — Teoría de MongoDB (20 min)

### ¿Qué es MongoDB?

MongoDB es una base de datos **NoSQL** (Not Only SQL). En lugar de guardar datos en tablas con filas y columnas, guarda **documentos en formato JSON**.

### Analogía simple para explicarlo

| SQL (lo que conocen) | MongoDB |
|---------------------|---------|
| Base de datos | Base de datos |
| Tabla | Colección (Collection) |
| Fila | Documento (Document) |
| Columna | Campo (Field) |

### Ejemplo de un documento MongoDB

```json
{
  "_id": "ObjectId('abc123')",
  "name": "Ana García",
  "email": "ana@mail.com",
  "password": "contraseña_hasheada"
}
```

> 💡 **Tip para explicar:** "Piensen en MongoDB como guardar cada usuario en un **post-it JSON** dentro de una caja llamada 'users'. No hay una tabla con columnas fijas."

### ¿Por qué MongoDB para este proyecto?

1. **Fácil de instalar** (Atlas tiene tier gratis en la nube)
2. **JSON nativo** — combina perfecto con Python y Flask
3. **Sin esquema fijo** — podemos agregar campos cuando queramos
4. **Muy popular** en startups y proyectos web modernos

### MongoDB Atlas (la opción más fácil)

Atlas es la versión en la **nube gratuita** de MongoDB. No necesitan instalar nada localmente.

> Mostrar en pantalla: https://cloud.mongodb.com → crear cuenta → crear cluster gratis → obtener connection string

**Connection string se ve así:**
```
mongodb+srv://usuario:password@cluster.mongodb.net/miapp
```

---

## 💻 Bloque 3 — Demo en vivo (35 min)

> **Decirle a los estudiantes:** "Yo voy a explicar la parte de Python y Flask, ustedes van a ver cómo se conecta con Mongo paso a paso."

### Paso 1 — Instalar pymongo (2 min)

```bash
pip install pymongo[srv]
```

> `[srv]` permite conectarse a MongoDB Atlas (en la nube).

---

### Paso 2 — Archivo de configuración (3 min)

Crear `mongo_config.py`:

```python
from pymongo import MongoClient

# Reemplazar con tu connection string de Atlas
MONGO_URI = "mongodb+srv://usuario:password@cluster.mongodb.net/"

client = MongoClient(MONGO_URI)
db = client["flask_app"]           # nombre de la base de datos
users_col = db["users"]            # nombre de la colección
```

> 💡 Explicar: "Esto es como abrir una conexión al servidor de base de datos. Solo se hace una vez."

---

### Paso 3 — Registrar usuario (10 min)

En `app.py`, importar y usar la colección:

```python
from mongo_config import users_col

@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name     = request.form['name']
        email    = request.form['email']
        password = request.form['password']

        # Verificar que el email no exista ya
        if users_col.find_one({"email": email}):
            return render_template('register.html', var1="El email ya existe")

        # Guardar en MongoDB
        users_col.insert_one({
            "name":     name,
            "email":    email,
            "password": password   # En producción se hashea, hoy simplificamos
        })

        return render_template('register.html', var1="¡Usuario registrado!")

    return render_template('register.html')
```

#### Métodos MongoDB a explicar:

| Método | Qué hace |
|--------|----------|
| `insert_one({...})` | Inserta un documento |
| `find_one({"campo": valor})` | Busca el primer resultado |
| `find({...})` | Busca todos los resultados |

> Abrir MongoDB Atlas en pantalla y mostrar que el usuario apareció en la colección.

---

### Paso 4 — Iniciar sesión (10 min)

```python
@bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email    = request.form['email']
        password = request.form['password']

        # Buscar usuario en MongoDB
        user = users_col.find_one({"email": email, "password": password})

        if user:
            return render_template('home.html',
                                   var1="Bienvenido, " + user["name"])
        else:
            return render_template('login.html',
                                   var1="Email o contraseña incorrectos")

    return render_template('login.html')
```

> 💡 Explicar línea por línea:
> - `find_one({"email": email, "password": password})` busca un usuario que tenga **ambos** campos iguales
> - Si `user` es `None`, el login falló
> - Si `user` existe, podemos acceder a `user["name"]`, `user["email"]`, etc.

---

### Paso 5 — Prueba completa (10 min)

1. Ir a `/register` → registrar un usuario
2. Verificar en Atlas que el documento fue creado
3. Ir a `/login` → ingresar con esas credenciales
4. Ver el mensaje de bienvenida
5. Intentar login incorrecto → ver el mensaje de error

---

### 🗂️ Estructura final del proyecto

```
mi_proyecto/
├── app.py               ← rutas y lógica Flask
├── mongo_config.py      ← conexión a MongoDB
└── templates/
    ├── templates.html   ← base (navbar)
    ├── home.html        ← página de bienvenida
    ├── login.html       ← formulario login
    └── register.html    ← formulario registro
```

---

## 🎮 Bloque 4 — Kahoot (10 min)

### Preguntas sugeridas para el Kahoot

**Pregunta 1:** ¿Cómo se llama la librería de Python para conectarse a MongoDB?
- ✅ pymongo
- ❌ mongoflask
- ❌ pydb
- ❌ mongodriver

**Pregunta 2:** ¿Cómo se llama cada "fila" en MongoDB?
- ✅ Documento
- ❌ Tabla
- ❌ Fila
- ❌ Registro

**Pregunta 3:** ¿Qué método usamos para guardar un usuario nuevo?
- ✅ `insert_one()`
- ❌ `save()`
- ❌ `add()`
- ❌ `push()`

**Pregunta 4:** ¿Qué devuelve `find_one()` si no encuentra nada?
- ✅ `None`
- ❌ `False`
- ❌ Error 404
- ❌ Una lista vacía

**Pregunta 5:** En MongoDB, ¿cómo se llama el equivalente a una "tabla"?
- ✅ Collection
- ❌ Table
- ❌ Group
- ❌ Folder

**Pregunta 6:** ¿Cuál de estos NO es válido en MongoDB?
- ✅ Requiere que todos los documentos tengan los mismos campos
- ❌ Guarda datos en formato JSON
- ❌ Tiene versión gratuita en la nube (Atlas)
- ❌ Se puede usar con Python

---

## ⚠️ Errores comunes y cómo resolverlos

| Error | Causa | Solución |
|-------|-------|----------|
| `ServerSelectionTimeoutError` | No se conecta a Mongo | Verificar connection string y whitelist de IP en Atlas |
| `ModuleNotFoundError: pymongo` | No instalado | `pip install pymongo[srv]` |
| `KeyError: 'email'` | El campo del form no coincide | Verificar que `name="email"` en el HTML |
| Login siempre falla | Password no coincide | Asegurarse de no hashear en registro y no hashear en login (o hashear en ambos) |

---

## 🚀 Ideas para la próxima clase

- **Hashear contraseñas** con `bcrypt` (seguridad real)
- **Flask sessions** — mantener al usuario logueado
- **Variables de entorno** con `.env` para no exponer el connection string
- **Actualizar y eliminar** documentos en MongoDB

---

> 📝 **Nota del profesor:** El código de esta clase está simplificado intencionalmente (sin hash de contraseñas, sin sessions) para que los estudiantes puedan enfocarse en entender la conexión Flask ↔ MongoDB. En la siguiente clase se agregan estas mejoras de seguridad.
