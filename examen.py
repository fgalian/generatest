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
        - Soporte real para preguntas multirrespuesta

    Fecha de creación: 23 Noviembre 2025
    Última actualización: 12 Marzo 2026
    Versión: 2026.03.12
    Licencia: Uso personal libre

    Notas:
    - Si el tiempo límite expira, el examen se entrega automáticamente.
    - Soporta preguntas multirrespuesta.
    - Para preguntas con varias respuestas correctas, el usuario
      debe introducirlas separadas por comas, por ejemplo: 1,3
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

    cur.execute("""
        SELECT id, question, option1, option2, option3, option4, correct
        FROM questions
        ORDER BY RANDOM()
        LIMIT ?
    """, (n,))

    preguntas = cur.fetchall()
    conn.close()
    return preguntas


def parsear_respuesta_usuario(resp, max_opcion):
    resp = resp.strip()

    if resp == "0":
        return []

    partes = [x.strip() for x in resp.split(",") if x.strip()]
    if not partes:
        return None

    try:
        nums = sorted(set(int(x) for x in partes))
    except ValueError:
        return None

    if any(x < 1 or x > max_opcion for x in nums):
        return None

    return nums


def examen():
    limpiar_pantalla()
    print(f"{BOLD}{CYAN}=== MODO EXAMEN ==={RESET}")

    # Número de preguntas
    try:
        n = int(input("¿Cuántas preguntas quieres responder?: ").strip())
        if n <= 0:
            print("El número de preguntas debe ser mayor que 0.")
            return
    except:
        print("Número inválido.")
        return

    # Tiempo límite total
    try:
        tiempo_limite = int(input("¿Tiempo total del examen (en segundos)?: ").strip())
        if tiempo_limite <= 0:
            print("El tiempo debe ser mayor que 0.")
            return
    except:
        print("Tiempo inválido.")
        return

    # Penalización por fallo
    try:
        penalizacion_valor = float(input("¿Cuánto resta cada fallo? (en puntos sobre 10, ej: 0.25): ").strip())
        if penalizacion_valor < 0:
            penalizacion_valor = 0.0
    except:
        penalizacion_valor = 0.0

    preguntas = obtener_preguntas(n)
    if not preguntas:
        print("No hay preguntas en la base de datos.")
        return

    total_preguntas = len(preguntas)
    aciertos = 0
    fallos = []
    en_blanco = 0

    tiempo_inicio = time.time()

    for indice, p in enumerate(preguntas, start=1):

        # Si se acabó el tiempo → finalizar examen
        if time.time() - tiempo_inicio >= tiempo_limite:
            print(f"\n{RED}{BOLD}¡SE HA ACABADO EL TIEMPO!{RESET}")
            break

        limpiar_pantalla()

        q_id, texto, o1, o2, o3, o4, correct_str = p
        correctas = sorted(int(x) for x in correct_str.split(",") if x.strip())

        # Filtrar opciones nulas antes de barajar
        opciones_originales = [o1, o2, o3, o4]
        baraja = [(i + 1, opcion) for i, opcion in enumerate(opciones_originales) if opcion is not None]

        if not baraja:
            continue

        random.shuffle(baraja)

        opciones_barajadas = [o for _, o in baraja]
        mapa_respuestas = {i + 1: orig for i, (orig, _) in enumerate(baraja)}
        max_opcion = len(opciones_barajadas)

        tiempo_transcurrido = int(time.time() - tiempo_inicio)
        tiempo_restante = max(0, tiempo_limite - tiempo_transcurrido)

        print(f"{BOLD}{CYAN}Pregunta {indice} de {total_preguntas}{RESET}    "
              f"{BOLD}ID:{RESET} {q_id}    "
              f"{BOLD}Tiempo restante:{RESET} {YELLOW}{tiempo_restante}s{RESET}\n")

        print(f"{BOLD}{texto}{RESET}\n")

        for i, opcion in enumerate(opciones_barajadas, start=1):
            print(f"{i}. {opcion}")

        if len(correctas) > 1:
            print(f"\nIntroduce una o varias respuestas separadas por comas (ej: 1,3), o 0 para dejarla en blanco.")
        else:
            print(f"\nIntroduce una respuesta entre 1 y {max_opcion}, o 0 para dejarla en blanco.")

        while True:
            # comprobar también el tiempo mientras espera entre preguntas
            if time.time() - tiempo_inicio >= tiempo_limite:
                print(f"\n{RED}{BOLD}¡SE HA ACABADO EL TIEMPO!{RESET}")
                break

            resp = input("\nTu respuesta: ").strip()
            respuesta_usuario = parsear_respuesta_usuario(resp, max_opcion)

            if respuesta_usuario is not None:
                break

            if max_opcion == 1:
                print("Respuesta inválida. Usa 0 o 1.")
            else:
                print(f"Respuesta inválida. Usa 0 o números del 1 al {max_opcion} separados por comas, por ejemplo: 1,3")

        if time.time() - tiempo_inicio >= tiempo_limite:
            break

        if respuesta_usuario == []:
            en_blanco += 1
            continue

        respuestas_originales = sorted(mapa_respuestas[x] for x in respuesta_usuario)

        if respuestas_originales == correctas:
            aciertos += 1
        else:
            fallos.append({
                "pregunta": p,
                "barajadas": opciones_barajadas,
                "mapa": mapa_respuestas,
                "respuesta_usuario": respuesta_usuario,
                "correctas": correctas
            })

    tiempo_total = round(time.time() - tiempo_inicio, 1)

    respondidas = aciertos + len(fallos) + en_blanco
    if respondidas == 0:
        nota = 0.0
    else:
        nota_bruta = aciertos - (len(fallos) * penalizacion_valor)
        if nota_bruta < 0:
            nota_bruta = 0
        nota = round((nota_bruta / total_preguntas) * 10, 2)

    limpiar_pantalla()
    print("\n" + "=" * 60)
    print(f"{BOLD}RESULTADO FINAL:{RESET}")
    print(f"Aciertos:    {GREEN}{aciertos}{RESET}")
    print(f"Fallos:      {RED}{len(fallos)}{RESET}")
    print(f"En blanco:   {YELLOW}{en_blanco}{RESET}")
    print(f"Respondidas: {CYAN}{respondidas}/{total_preguntas}{RESET}")
    print(f"Tiempo total: {CYAN}{tiempo_total} segundos{RESET}")
    print("=" * 60)

    print(f"\n{BOLD}NOTA FINAL SOBRE 10:{RESET} {CYAN}{nota}{RESET}")

    if fallos:
        print(f"\n{BOLD}{RED}Preguntas falladas:{RESET}\n")

        for fallo in fallos:
            p = fallo["pregunta"]
            barajadas = fallo["barajadas"]
            mapa = fallo["mapa"]
            resp_usuario = fallo["respuesta_usuario"]
            correctas = fallo["correctas"]

            q_id, texto, o1, o2, o3, o4, correct_str = p

            print(f"{YELLOW}{BOLD}Pregunta #{q_id}:{RESET}")
            print(texto)
            print("")

            for i, opcion in enumerate(barajadas, start=1):
                original = mapa[i]

                if i in resp_usuario and original in correctas:
                    print(f"{YELLOW}Tu respuesta marcada y correcta: {i}. {opcion}{RESET}")
                elif i in resp_usuario and original not in correctas:
                    print(f"{RED}Tu respuesta incorrecta: {i}. {opcion}{RESET}")
                elif original in correctas:
                    print(f"{GREEN}Correcta: {i}. {opcion}{RESET}")
                else:
                    print(f"{i}. {opcion}")

            correctas_mostradas = [str(i) for i, original in mapa.items() if original in correctas]
            usuario_mostradas = [str(i) for i in resp_usuario]

            print("")
            print(f"{BOLD}Marcaste:{RESET} {', '.join(usuario_mostradas) if usuario_mostradas else 'ninguna'}")
            print(f"{BOLD}Correctas eran:{RESET} {', '.join(correctas_mostradas)}")
            print("")

if __name__ == "__main__":
    examen()