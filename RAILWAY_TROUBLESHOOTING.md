# 🔧 Solución de Problemas Railway

## Error: "Can't connect to MySQL server"

Si ves este error, significa que Django está intentando usar MySQL en lugar de PostgreSQL.

### ✅ Solución

1. **Verifica que DATABASE_URL esté configurado en Railway:**
   - Ve a tu servicio web (Django) en Railway
   - Pestaña **"Variables"**
   - Debe aparecer `DATABASE_URL` con un valor como:
     ```
     postgresql://postgres:password@gondola.proxy.rlwy.net:5432/railway
     ```

2. **Si NO aparece DATABASE_URL:**
   - Asegúrate de que PostgreSQL y el servicio web estén en el **mismo proyecto**
   - Railway conecta automáticamente las bases de datos en el mismo proyecto
   - Si están en proyectos diferentes, necesitas agregar la variable manualmente

3. **Agregar DATABASE_URL manualmente (si es necesario):**
   - Ve a tu servicio PostgreSQL
   - Pestaña **"Variables"**
   - Copia el valor de `DATABASE_URL` o `PGDATABASE_URL`
   - Ve a tu servicio web
   - Pestaña **"Variables"**
   - Clic en **"+ New Variable"**
   - Key: `DATABASE_URL`
   - Value: (pega la URL que copiaste)
   - Clic en **"Add"**

4. **Verificar en los logs:**
   - Después de desplegar, revisa los logs
   - Debes ver: `✅ Usando base de datos desde DATABASE_URL: postgresql://...`
   - Si ves `✅ Usando MySQL local` o `✅ Usando SQLite`, entonces `DATABASE_URL` no está configurado

## Verificar Variables de Entorno en Railway

### Método 1: Desde el Dashboard
1. Ve a tu servicio web
2. Pestaña **"Variables"**
3. Debe aparecer `DATABASE_URL` automáticamente

### Método 2: Desde los Logs
Agrega esto temporalmente en `settings.py` para debug:

```python
# Solo para debug - eliminar después
if 'DATABASE_URL' in os.environ:
    print(f"DATABASE_URL encontrado: {os.environ['DATABASE_URL'][:50]}...")
else:
    print("❌ DATABASE_URL NO encontrado en variables de entorno")
    print(f"Variables disponibles: {list(os.environ.keys())}")
```

## Variables Requeridas

Asegúrate de tener estas variables en tu servicio web:

- ✅ `DATABASE_URL` (automático de Railway)
- ✅ `SECRET_KEY` (debes agregarla manualmente)
- ✅ `DEBUG=False` (para producción)
- ✅ `ALLOWED_HOSTS=*.railway.app` (o tu dominio)
- ✅ `CORS_ALLOWED_ORIGINS` (tu frontend)

## Reiniciar el Servicio

Después de agregar/modificar variables:
1. Ve a tu servicio web
2. Clic en **"..."** (menú)
3. Selecciona **"Restart"**
4. Espera a que se reinicie

## Verificar Conexión a la Base de Datos

Una vez desplegado, los logs deben mostrar:
```
✅ Usando base de datos desde DATABASE_URL: postgresql://...
Operations to perform:
  Apply all migrations: ...
Running migrations:
  ...
```

Si ves errores de conexión, verifica:
1. Que PostgreSQL esté activo (debe decir "Active" en Railway)
2. Que `DATABASE_URL` esté correctamente configurado
3. Que el servicio web y PostgreSQL estén en el mismo proyecto

## Comandos Útiles

### Ver logs en tiempo real
En Railway, ve a tu servicio → pestaña **"Deployments"** → **"View Logs"**

### Conectar a la base de datos localmente
```bash
railway connect
```

### Ejecutar migraciones manualmente
```bash
railway run python manage.py migrate
```

