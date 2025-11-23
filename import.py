"""
============================================================
    Script: import.py
    Autor: Francisco Javier Sánchez Galián
    Descripción:
        Importa preguntas desde un fichero XML y las inserta
        en una base de datos SQLite. Detecta multirrespuesta
        y mantiene el código original del XML.

    Fecha de creación: 23 Noviembre 2025
    Última actualización: 23 Noviembre 2025
    Versión: 2025.11.23
    Licencia: Uso personal libre

    Notas:
    - Requiere un archivo XML estructurado según el formato
      utilizado en test.xml.
    - Genera automáticamente la base de datos test.db.
============================================================
"""


import sqlite3
import xml.etree.ElementTree as ET

XML_FILE = "test.xml"       # cambia si el nombre es otro
DB_FILE  = "test.db"

# -----------------------------------------
# CREAR LA BASE DE DATOS
# -----------------------------------------
conn = sqlite3.connect(DB_FILE)
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS questions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    question TEXT,
    option1 TEXT,
    option2 TEXT,
    option3 TEXT,
    option4 TEXT,
    correct TEXT,
    code TEXT
)
""")

# -----------------------------------------
# PARSEAR XML
# -----------------------------------------
tree = ET.parse(XML_FILE)
root = tree.getroot()

count = 0

# las preguntas están en /test/c/c (según el fichero de daypo)
for bloque in root.findall("./c/c"):
    try:
        enunciado = bloque.find("p").text.strip()
        codigo = bloque.find("c").text.strip()
        opciones = [o.text.strip() for o in bloque.find("r").findall("o")]

        # calcular respuestas correctas: indices donde codigo[i] == "2"
        correctas = [str(i+1) for i, x in enumerate(codigo) if x == "2"]
        correct_text = ",".join(correctas)

        # insertar en SQLite
        cur.execute("""
            INSERT INTO questions
            (question, option1, option2, option3, option4, correct, code)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            enunciado,
            opciones[0] if len(opciones) > 0 else None,
            opciones[1] if len(opciones) > 1 else None,
            opciones[2] if len(opciones) > 2 else None,
            opciones[3] if len(opciones) > 3 else None,
            correct_text,
            codigo
        ))

        count += 1

    except Exception as e:
        print("Error procesando una pregunta:", e)

conn.commit()
conn.close()

print(f"Importación completada. Total preguntas insertadas: {count}")
