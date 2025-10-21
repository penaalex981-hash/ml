import sqlite3
import os

# Ruta absoluta al archivo de la base de datos
db_path = os.path.join(os.path.dirname(__file__), "database", "todo.db")

# Conexión
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Crear la tabla si no existe
cursor.execute("""
CREATE TABLE IF NOT EXISTS tasks (
    uuid TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    description TEXT NOT NULL,
    status TEXT NOT NULL
)
""")

conn.commit()
conn.close()

print("✅ Tabla 'tasks' creada correctamente en la base de datos.")
