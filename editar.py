"""
============================================================
    Script: editar.py
    Autor: Francisco Javier Sánchez Galián
    Descripción:
        Permite editar cualquier pregunta de la base de datos
        por ID. Se pueden modificar:
        - Enunciado
        - Respuestas
        - Opciones correctas

    Fecha de creación: 23 Noviembre 2025
    Última actualización: 23 Noviembre 2025
    Versión: 2025.11.23
    Licencia: Uso personal libre

    Notas:
    - Pulsa ENTER en un campo para mantener su valor original.
    - Admite múltiples respuestas correctas separadas por comas.
============================================================
"""


import sqlite3

DB_FILE = "test.db"

def editar_pregunta():
    conn = sqlite3.connect(DB_FILE)
    cur = conn.cursor()

    try:
        q_id = int(input("ID de la pregunta a editar: ").strip())
    except:
        print("ID no válido.")
        return

    cur.execute("""
        SELECT id, question, option1, option2, option3, option4, correct
        FROM questions
        WHERE id = ?
    """, (q_id,))

    row = cur.fetchone()

    if not row:
        print("No existe ninguna pregunta con ese ID.")
        conn.close()
        return

    id_p, texto, o1, o2, o3, o4, correct = row

    print("\n=== Pregunta actual ===")
    print(f"ID: {id_p}")
    print(f"Enunciado: {texto}")
    print(f"1. {o1}")
    print(f"2. {o2}")
    print(f"3. {o3}")
    print(f"4. {o4}")
    print(f"Correctas: {correct}")

    print("\nPulsa ENTER para dejar un campo igual que está.\n")

    # --- Editar enunciado ---
    nuevo_texto = input("Nuevo enunciado: ").strip()
    if nuevo_texto == "":
        nuevo_texto = texto

    # --- Editar respuestas ---
    nueva_o1 = input("Nueva respuesta 1: ").strip()
    nueva_o2 = input("Nueva respuesta 2: ").strip()
    nueva_o3 = input("Nueva respuesta 3: ").strip()
    nueva_o4 = input("Nueva respuesta 4: ").strip()

    nueva_o1 = nueva_o1 if nueva_o1 != "" else o1
    nueva_o2 = nueva_o2 if nueva_o2 != "" else o2
    nueva_o3 = nueva_o3 if nueva_o3 != "" else o3
    nueva_o4 = nueva_o4 if nueva_o4 != "" else o4

    # --- Editar correctas ---
    nuevas_correctas = input("Nuevas respuestas correctas (ej: 2 o 1,3,4): ").strip()
    if nuevas_correctas == "":
        nuevas_correctas = correct
    else:
        # Validación
        try:
            partes = nuevas_correctas.split(",")
            partes = [int(x) for x in partes]
            if any(x < 1 or x > 4 for x in partes):
                raise ValueError
        except:
            print("Formato incorrecto. Debe ser 1–4 separados por comas.")
            conn.close()
            return

    # --- Guardar cambios ---
    cur.execute("""
        UPDATE questions
        SET question = ?, option1 = ?, option2 = ?, option3 = ?, option4 = ?, correct = ?
        WHERE id = ?
    """, (nuevo_texto, nueva_o1, nueva_o2, nueva_o3, nueva_o4, nuevas_correctas, q_id))

    conn.commit()
    conn.close()

    print("\n✔ Cambios guardados correctamente.\n")

if __name__ == "__main__":
    editar_pregunta()
