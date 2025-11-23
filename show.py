"""
============================================================
    Script: show.py
    Autor: Francisco Javier Sánchez Galián
    Descripción:
        Muestra una pregunta aleatoria desde la base de datos,
        espera a que el usuario pulse ENTER y revela la respuesta
        correcta en color.

    Fecha de creación: 23 Noviembre 2025
    Última actualización: 23 Noviembre 2025
    Versión: 2025.11.23
    Licencia: Uso personal libre

    Notas:
    - Ideal para estudiar preguntas individualmente.
    - Compatible con multirrespuesta.
============================================================
"""


import sqlite3
import random

DB_FILE = "test.db"

# Colores ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
YELLOW = "\033[93m"

def mostrar_pregunta():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    # Elegir una pregunta aleatoria
    cur.execute("SELECT id, question, option1, option2, option3, option4, correct FROM questions ORDER BY RANDOM() LIMIT 1")
    row = cur.fetchone()
    conn.close()

    if not row:
        print("No hay preguntas en la base de datos.")
        return

    q_id, enunciado, o1, o2, o3, o4, correct = row

    # Convertir "2,3" → [2,3]
    correct_indices = [int(x) for x in correct.split(",")]

    print(f"\n{BOLD}PREGUNTA #{q_id}:{RESET}")
    print(enunciado)
    print("")

    opciones = [o1, o2, o3, o4]

    # --- Mostrar preguntas sin color ---
    for i, texto in enumerate(opciones, start=1):
        if texto is None:
            continue
        print(f"{i}. {texto}")

    # Esperar a que el usuario pulse ENTER
    input("\nPulsa ENTER para mostrar la solución...\n")

    # --- Mostrar con color las correctas ---
    for i, texto in enumerate(opciones, start=1):
        if texto is None:
            continue
        if i in correct_indices:
            print(f"{YELLOW}{BOLD}{i}. {texto}{RESET}")
        else:
            print(f"{i}. {texto}")

if __name__ == "__main__":
    mostrar_pregunta()
