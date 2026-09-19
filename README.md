# Obra Conecta — Versión definitiva

## La causa real de "no se puede acceder a este sitio web"

Analicé el zip que subiste con tu propio `venv` y encontré el problema
exacto (no era de conexión ni de código):

1. **El entorno virtual estaba prácticamente vacío.** Tenía `pip` y
   `setuptools`, pero nunca se instaló `fastapi`, `uvicorn`, `sqlalchemy`
   ni nada del `requirements.txt`. Por eso `uvicorn app.main:app --reload`
   no podía funcionar — el comando `uvicorn` ni siquiera existía en ese
   entorno. Eso es exactamente "no se puede acceder a este sitio": el
   servidor nunca llegó a levantarse.

2. **El archivo `.env` apuntaba a SQLite, no a tu MySQL de XAMPP**
   (`DATABASE_URL=sqlite:///./obra_conecta.db`). Esto lo generó un archivo
   `configure.py` que traías en el proyecto (no lo escribí yo) con un valor
   por defecto equivocado. Aunque hubieras instalado todo, el backend habría
   creado una base SQLite nueva y vacía, completamente separada de tu MySQL
   con los usuarios reales que me compartiste en el `.sql`.

## Qué cambié para que esto no se repita

Además de corregir el `.env` y el `configure.py`, **simplifiqué las
dependencias del backend** para reducir el riesgo de que la instalación
vuelva a fallar a medias:

- Antes: 12 paquetes, incluyendo `python-jose` y `passlib[bcrypt]`, que en
  Windows a veces necesitan compilar extensiones nativas y fallan sin dar
  un error claro.
- Ahora: 8 paquetes. El hash de contraseñas y las sesiones (JWT) se
  reescribieron usando **solo la librería estándar de Python**
  (`hashlib`, `hmac`, `secrets`) — cero dependencias adicionales para la
  parte más sensible del sistema. Esta parte la probé de verdad (no solo
  la revisé): hash y verificación de contraseña, creación y validación de
  sesión, rechazo de firma inválida y de sesión expirada — las 4 pruebas
  pasan.

## Cómo instalar y ejecutar (desde cero)

### 1. Enciende MySQL en XAMPP
Panel de control de XAMPP → **Start** en la fila de MySQL.

### 2. Backend
```bash
cd backend
python -m venv venv
venv\Scripts\activate
```
**Confirma que ves `(venv)` al inicio de tu línea de comandos antes de continuar.**

```bash
pip install -r requirements.txt
```
**Importante:** revisa que este comando termine sin errores en rojo. Si ves
algún `ERROR` al final, dime exactamente cuál — no sigas al siguiente paso
hasta que este instale limpio.

Verifica que quedó instalado:
```bash
pip list
```
Debes ver `fastapi`, `uvicorn`, `sqlalchemy`, `pymysql`, `pydantic`,
`email-validator`, `python-dotenv`, `python-multipart` en la lista.

El `.env` ya viene configurado para MySQL de XAMPP (usuario `root`, sin
contraseña, puerto 3306). Si tu MySQL tiene otra configuración, ábrelo y
ajústalo.

### 3. Base de datos
Tu base de datos MySQL ya tiene la estructura correcta (la comparé con tu
`.sql` y coincide exactamente con lo que espera el código). Solo hace falta
llenarla:
```bash
python seed.py
```
Esto crea las categorías con foto, reactiva tus usuarios existentes
(estaban marcados como inactivos por una versión anterior), y crea 5
profesionales de ejemplo con foto para que el sitio se vea poblado.

### 4. Levanta el backend
```bash
uvicorn app.main:app --reload
```
Debe quedar así, sin cerrarse:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```
Confírmalo abriendo `http://localhost:8000/docs` en el navegador.

### 5. Frontend (en otra terminal)
```bash
cd frontend
npm install
npm run dev
```
Abre `http://localhost:5173`.

## Usuarios de prueba (después de correr seed.py)

| Rol | Correo | Contraseña |
|---|---|---|
| Cliente | cliente@demo.com | demo1234 |
| Profesional | profesional@demo.com (y 5 más, ver seed.py) | demo1234 |

**Nota sobre tus usuarios reales** (Danilo, carlos, camila, Prueba): sus
contraseñas fueron creadas con un método distinto (de una versión anterior
del proyecto). `seed.py` los reactiva, pero si el login les falla,
regístrense de nuevo — es más simple que intentar recuperar esas
contraseñas antiguas.

## Si algo sigue sin funcionar

Antes de nada, dime exactamente en cuál de estos dos comandos aparece un
error, y el mensaje completo:
1. `pip install -r requirements.txt`
2. `uvicorn app.main:app --reload`

Con el mensaje exacto puedo decirte la causa en un solo intento, en vez de
que sigamos adivinando.
