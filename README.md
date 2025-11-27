# Control Escolar DESIT API

Backend Django REST Framework para el sistema de control escolar.

## 🚀 Inicio Rápido

### 1. Configurar MySQL
```bash
# Si conoces la contraseña de root
./setup_mysql_simple.sh

# Si NO conoces la contraseña
./reset_mysql_password.sh
```

### 2. Iniciar Backend
```bash
./iniciar_backend.sh
```

O manualmente:
```bash
source venv/bin/activate
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

## 📚 Documentación

- **Guía de inicio rápido:** [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
- **Configuración MySQL:** [CONFIGURAR_MYSQL.md](CONFIGURAR_MYSQL.md)

## 🔗 Endpoints

- `POST /login/` - Iniciar sesión
- `GET /logout/` - Cerrar sesión
- `POST /alumnos/` - Crear alumno
- `GET /lista-alumnos/` - Listar alumnos
- `POST /maestros/` - Crear maestro
- `GET /lista-maestros/` - Listar maestros
- `POST /admin/` - Crear administrador
- `GET /lista-admins/` - Listar administradores

## 🛠️ Tecnologías

- Django 5.0.2
- Django REST Framework 3.16.1
- MySQL 8.0
- PyMySQL

## 📝 Requisitos

- Python 3.8+
- MySQL 8.0+
- Entorno virtual (venv)
