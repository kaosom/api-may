# 🚂 Guía de Despliegue en Railway

Esta guía te ayudará a desplegar tu aplicación Django y base de datos PostgreSQL en Railway.

## 📋 Requisitos Previos

1. Cuenta en GitHub (gratis)
2. Cuenta en Railway (gratis) - https://railway.app
3. Tu proyecto debe estar en un repositorio de GitHub

## 🚀 Paso a Paso

### 1. Preparar el Repositorio

Asegúrate de que tu proyecto esté en GitHub:

```bash
# Si aún no tienes git inicializado
git init
git add .
git commit -m "Preparado para Railway"
git branch -M main
git remote add origin https://github.com/TU_USUARIO/TU_REPO.git
git push -u origin main
```

### 2. Crear Cuenta en Railway

1. Ve a https://railway.app
2. Haz clic en "Login" o "Start a New Project"
3. Conecta con tu cuenta de GitHub
4. Autoriza Railway para acceder a tus repositorios

### 3. Crear un Nuevo Proyecto

1. En el dashboard de Railway, haz clic en **"New Project"**
2. Selecciona **"Deploy from GitHub repo"**
3. Elige tu repositorio `control_escolar_desit_api`
4. Railway detectará automáticamente que es un proyecto Python/Django

### 4. Agregar Base de Datos PostgreSQL

1. En tu proyecto de Railway, haz clic en **"+ New"**
2. Selecciona **"Database"** → **"Add PostgreSQL"**
3. Railway creará automáticamente una base de datos PostgreSQL
4. La variable `DATABASE_URL` se configurará automáticamente

### 5. Configurar Variables de Entorno

En tu servicio web (no en la base de datos), ve a la pestaña **"Variables"** y agrega:

```
SECRET_KEY=tu-secret-key-super-segura-aqui
DEBUG=False
ALLOWED_HOSTS=*.railway.app,tu-dominio.com
CORS_ALLOWED_ORIGINS=https://lavender-cat-827556.hostingersite.com,http://localhost:4200
PYTHON_VERSION=3.11
```

**Nota:** Railway ya configura automáticamente `DATABASE_URL`, no necesitas agregarla manualmente.

### 6. Configurar el Servicio Web

1. En el servicio web, ve a **"Settings"**
2. En **"Build Command"** (opcional, Railway lo detecta automáticamente):
   ```
   pip install -r requirements.txt && python manage.py collectstatic --noinput
   ```
3. En **"Start Command"**:
   ```
   python manage.py migrate --noinput && gunicorn control_escolar_desit_api.wsgi:application --bind 0.0.0.0:$PORT
   ```

### 7. Desplegar

1. Railway detectará automáticamente los cambios en tu repositorio
2. Cada push a `main` desplegará automáticamente
3. Puedes ver el progreso en la pestaña **"Deployments"**

### 8. Obtener tu URL

1. Una vez desplegado, ve a **"Settings"** del servicio web
2. En **"Domains"**, Railway te dará una URL como: `tu-proyecto.up.railway.app`
3. Esta URL será tu endpoint de la API

## 🔧 Configuración Adicional

### Variables de Entorno Importantes

- `DATABASE_URL`: Se configura automáticamente por Railway
- `PORT`: Se configura automáticamente (no lo cambies)
- `SECRET_KEY`: Genera uno seguro con: `python -c "import secrets; print(secrets.token_urlsafe(50))"`
- `ALLOWED_HOSTS`: Incluye tu dominio de Railway y cualquier dominio personalizado

### Migraciones

Las migraciones se ejecutan automáticamente en el `Procfile` antes de iniciar el servidor.

### Logs

Puedes ver los logs en tiempo real en la pestaña **"Deployments"** → **"View Logs"**

## 🆓 Límites del Plan Gratuito

- **$5 de crédito gratis al mes**
- **500 horas de ejecución** (suficiente para 24/7 si solo tienes 1 servicio)
- **Base de datos PostgreSQL** incluida
- **Despliegues ilimitados**

## 🐛 Solución de Problemas

### Error: "No module named X"
- Verifica que todas las dependencias estén en `requirements.txt`

### Error: "Database connection failed"
- Verifica que la base de datos esté en el mismo proyecto
- Railway configura `DATABASE_URL` automáticamente

### Error: "Static files not found"
- Asegúrate de que `collectstatic` se ejecute en el build
- Verifica que `STATIC_ROOT` esté configurado en `settings.py`

### El servicio se apaga después de inactividad
- En el plan gratuito, Railway puede pausar servicios inactivos
- La primera petición después de pausar puede tardar ~30 segundos

## 📝 Comandos Útiles

### Ver logs en tiempo real
```bash
railway logs
```

### Conectar a la base de datos localmente
```bash
railway connect
```

### Ejecutar comandos Django
```bash
railway run python manage.py createsuperuser
railway run python manage.py shell
```

## 🔗 Enlaces Útiles

- [Documentación de Railway](https://docs.railway.app)
- [Railway Discord](https://discord.gg/railway)
- [Ejemplos de Django en Railway](https://docs.railway.app/guides/django)

## ✅ Checklist Final

- [ ] Proyecto en GitHub
- [ ] Cuenta de Railway creada
- [ ] Proyecto creado en Railway
- [ ] Base de datos PostgreSQL agregada
- [ ] Variables de entorno configuradas
- [ ] Primer despliegue exitoso
- [ ] URL de producción funcionando
- [ ] Migraciones aplicadas
- [ ] API respondiendo correctamente

---

**¡Listo!** Tu aplicación debería estar funcionando en Railway. 🎉

