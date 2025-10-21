import typer
import uuid
import sys, os

# Asegura que se puedan importar módulos de la carpeta actual
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from rich.console import Console
from rich.table import Table
from typing import Literal
from rich import print
from connection.connect_database import connect_database
from helpers.status_colors import status_colored

app = typer.Typer()
console = Console()
STATUS = Literal["COMPLETED", "PENDING", "IN_PROGRESS"]

# Obtener ruta absoluta del archivo de base de datos
db_path = os.path.join(os.path.dirname(__file__), "database", "todo.db")

@app.command(short_help="Create one task")
def create(name: str, description: str, status: STATUS):
    """Crea una nueva tarea."""
    conn = connect_database(db_path)
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO tasks(uuid, name, description, status) VALUES(?, ?, ?, ?)",
            (str(uuid.uuid4()), name, description, status)
        )
        conn.commit()
        conn.close()
        print("[bold green]Tarea creada exitosamente[/bold green]")

@app.command(short_help="List all tasks")
def list():
    """Lista todas las tareas."""
    conn = connect_database(db_path)
    if conn:
        cursor = conn.cursor()
        results = cursor.execute("SELECT uuid, name, description, status FROM tasks")

        table = Table("UUID", "Name", "Description", "Status", show_lines=True)
        for uuid_, name, description, status in results.fetchall():
            status_with_color = status_colored(status)
            table.add_row(uuid_, name, description, status_with_color)

        conn.close()
        table.caption = "List all tasks"
        console.print(table)

@app.command(short_help="Update one task")
def update(uuid_: str, name: str, description: str, status: STATUS):
    """Actualiza una tarea por su UUID."""
    conn = connect_database(db_path)
    if conn:
        cursor = conn.cursor()
        cursor.execute(
            "UPDATE tasks SET name=?, description=?, status=? WHERE uuid=?",
            (name, description, status, uuid_)
        )
        conn.commit()
        conn.close()
        print(f"[bold yellow]Tarea {uuid_} actualizada[/bold yellow]")

@app.command(short_help="Delete one task")
def delete(uuid_: str):
    """Elimina una tarea por su UUID."""
    conn = connect_database(db_path)
    if conn:
        cursor = conn.cursor()
        cursor.execute("DELETE FROM tasks WHERE uuid=?", (uuid_,))
        conn.commit()
        conn.close()
        print(f"[bold red]Tarea {uuid_} eliminada[/bold red]")

if __name__ == "__main__":
    app()
