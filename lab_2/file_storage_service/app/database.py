import json
import os

DB_FILE = "database.json"

# Инициализация базы данных, если файл отсутствует
if not os.path.exists(DB_FILE):
    with open(DB_FILE, "w") as f:
        json.dump({"files": []}, f)

def load_db():
    """Загружает данные из JSON-файла."""
    with open(DB_FILE, "r") as f:
        return json.load(f)

def save_db(data):
    """Сохраняет данные в JSON-файл."""
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def add_file(file_info):
    """Добавляет новый файл в базу данных."""
    data = load_db()
    data["files"].append(file_info)
    save_db(data)
    return file_info

def get_files():
    """Возвращает список всех файлов."""
    return load_db().get("files", [])

def get_file_by_id(file_id):
    """Возвращает файл по ID."""
    files = get_files()
    for file in files:
        if file["id"] == file_id:
            return file
    return None

def delete_file(file_id):
    """Удаляет файл по ID."""
    data = load_db()
    files = data.get("files", [])
    new_files = [file for file in files if file["id"] != file_id]
    if len(files) == len(new_files):
        return {"error": "Файл не найден"}
    data["files"] = new_files
    save_db(data)
    return {"message": "Файл удален"}
