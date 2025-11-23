"""
============================================================
    Script: examen.py
    Autor: Francisco Javier Sánchez Galián
    Descripción:
        Ejecuta un examen completo con:
        - Temporizador total
        - Barajado de respuestas
        - Limpieza de pantalla entre preguntas
        - Penalización configurable por fallos
        - Preguntas en blanco sin penalizar
        - Nota final sobre 10
        - Resumen de fallos

    Fecha de creación: 23 Noviembre 2025
    Última actualización: 23 Noviembre 2025
    Versión: 2025.11.23
    Licencia: Uso personal libre

    Notas:
    - Si el tiempo límite expira, el examen se entrega automáticamente.
    - Soporta preguntas multirrespuesta.
============================================================
"""


import sqlite3
import random
import time
import os
import platform

DB_FILE = "test.db"

# Colores ANSI
RESET = "\033[0m"
BOLD = "\033[1m"
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
CYAN = "\033[96m"

def limpiar_pantalla():
    if platform.system() == "Windows":
        os.system("cls")
    else:
        os.system("clear")

def obtener_preguntas(n):
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    cur.execute(f"""
        SELECT id, question, option1, option2, option3, option4, correct
        FROM questions
        ORDER BY RANDOM()
        LIMIT {n}
    """)

    preguntas = cur.fetchall()
    conn.close()
    return preguntas

def examen():
    limpiar_pantalla()
    print(f"{BOLD}{CYAN}=== MODO EXAMEN ==={RESET}")

    # Número de preguntas
    try:
        n = int(input("¿Cuántas preguntas quieres responder?: ").strip())
    except:
        print("Número inválido.")
        return

    # Tiempo límite total
    try:
        tiempo_limite = int(input("¿Tiempo total del examen (en segundos)?: ").strip())
    except:
        print("Tiempo inválido.")
        return

    # Penalización por fallo
    try:
        penalizacion_valor = float(input("¿Cuánto resta cada fallo? (en puntos sobre 10, ej: 0.25): ").strip())
    except:
        penalizacion_valor = 0.0

    preguntas = obtener_preguntas(n)
    if not preguntas:
        print("No hay preguntas en la base de datos.")
        return

    aciertos = 0
    fallos = []
    en_blanco = 0

    tiempo_inicio = time.time()

    for p in preguntas:

        # Si se acabó el tiempo → finalizar examen
        if time.time() - tiempo_inicio >= tiempo_limite:
            print(f"\n{RED}{BOLD}¡SE HA ACABADO EL TIEMPO!{RESET}")
            break

        # Limpiar pantalla
        limpiar_pantalla()

        q_id, texto, o1, o2, o3, o4, correct_str = p
        correctas = [int(x) for x in correct_str.split(",")]
        opciones = [o1, o2, o3, o4]

        # --- Barajar respuestas ---
        indices_originales = [1, 2, 3, 4]
        baraja = list(zip(indices_originales, opciones))
        random.shuffle(baraja)

        opciones_barajadas = [o for _, o in baraja]
        mapa_respuestas = {i+1: orig for i, (orig, _) in enumerate(baraja)}

        print(f"{BOLD}Pregunta #{q_id}:{RESET}")
        print(texto)
        print("")

        for i, opcion in enumerate(opciones_barajadas, start=1):
            print(f"{i}. {opcion}")

        print("\nIntroduce 1–4 para responder, o 0 para dejarla en blanco.")

        # Esperar respuesta (sin temporizador por pregunta)
        while True:
            resp = input("\nTu respuesta: ").strip()
            if resp in ("0", "1", "2", "3", "4"):
                break
            print("Respuesta inválida. Usa 0, 1, 2, 3 o 4.")

        if resp == "0":
            en_blanco += 1
            continue

        resp = int(resp)
        resp_original = mapa_respuestas[resp]

        if resp_original in correctas:
            aciertos += 1
        else:
            fallos.append((p, opciones_barajadas, mapa_respuestas, resp, correctas))

    tiempo_total = round(time.time() - tiempo_inicio, 1)

    # ---- RESULTADO ----

    # Calcular nota final
    nota = aciertos - (len(fallos) * penalizacion_valor)
    if nota < 0:
        nota = 0
    nota = round((nota / n) * 10, 2)  # Nota sobre 10

    limpiar_pantalla()
    print("\n" + "="*60)
    print(f"{BOLD}RESULTADO FINAL:{RESET}")
    print(f"Aciertos: {GREEN}{aciertos}{RESET}")
    print(f"Fallos:   {RED}{len(fallos)}{RESET}")
    print(f"En blanco: {YELLOW}{en_blanco}{RESET}")
    print(f"Tiempo total: {CYAN}{tiempo_total} segundos{RESET}")
    print("="*60)

    print(f"\n{BOLD}NOTA FINAL SOBRE 10:{RESET} {CYAN}{nota}{RESET}")

    if fallos:
        print(f"\n{BOLD}{RED}Preguntas falladas:{RESET}\n")
        for p, barajadas, mapa, resp_usuario, correctas in fallos:
            q_id, texto, o1, o2, o3, o4, correct_str = p

            print(f"{YELLOW}{BOLD}Pregunta #{q_id}:{RESET}")
            print(texto)
            print("")

            for i, opcion in enumerate(barajadas, start=1):
                original = mapa[i]
                if i == resp_usuario:
                    print(f"{RED}Tu respuesta: {i}. {opcion}{RESET}")
                elif original in correctas:
                    print(f"{GREEN}Correcta: {i}. {opcion}{RESET}")
                else:
                    print(f"{i}. {opcion}")
            print("")

if __name__ == "__main__":
    examen()
