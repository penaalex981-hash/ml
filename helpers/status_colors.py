from rich.text import Text

def status_colored(status: str) -> Text:
    status = status.upper()
    colors = {
        "COMPLETED": "green",
        "PENDING": "yellow",
        "IN_PROGRESS": "red"
    }
    color = colors.get(status, "white")
    return Text(status, style=color)
