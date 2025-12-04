# Solo importar pymysql si realmente se va a usar MySQL (no cuando se usa DATABASE_URL)
import os
if 'DATABASE_URL' not in os.environ and os.path.exists(os.path.join(os.path.dirname(__file__), '..', 'my.cnf')):
    import pymysql
    pymysql.install_as_MySQLdb()
    #Esta línea registra pymysql con ese alias
    #  y evita errores de importación cuando se conecte a MySQL sin mysqlclient.