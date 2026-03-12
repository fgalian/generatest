# 📄 Formato del fichero XML para importar preguntas

Este documento explica el formato exacto que debe tener el fichero XML
utilizado por `import.py` para importar preguntas a la base de datos SQLite.

---

## 📌 Nombre del fichero

Por defecto, el script `import.py` espera encontrar un fichero llamado:

```text
test.xml
```

Si quieres usar otro nombre, debes modificar esta línea en `import.py`:

```python
XML_FILE = "test.xml"
```

---

## 🧱 Estructura general del XML

El script recorre las preguntas con esta instrucción:

```python
root.findall("./c/c")
```

Eso significa que el XML debe tener esta estructura básica:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<test>
  <c>
    <c>
      <p>Texto de la pregunta</p>
      <c>2000</c>
      <r>
        <o>Opción 1</o>
        <o>Opción 2</o>
        <o>Opción 3</o>
        <o>Opción 4</o>
      </r>
    </c>
  </c>
</test>
```

---

## 🧩 Significado de cada etiqueta

### `<test>`
Es el nodo raíz del documento XML.

### `<c>`
Se utiliza en dos niveles:

- el primer `<c>` agrupa todas las preguntas
- cada segundo `<c>` representa una pregunta individual

### `<p>`
Contiene el enunciado de la pregunta.

### `<c>`
Dentro de cada pregunta, esta etiqueta contiene el código de respuestas correctas.

### `<r>`
Agrupa las respuestas posibles.

### `<o>`
Cada etiqueta `<o>` representa una opción de respuesta.

---

## ✅ Cómo funciona el código de respuestas

El campo `<c>` de cada pregunta indica qué respuestas son correctas.

Tu script interpreta como correcta toda posición cuyo valor sea `"2"`.

Ejemplo del código actual:

```python
correctas = [str(i+1) for i, x in enumerate(codigo) if x == "2"]
```

### Ejemplos

| Código | Respuesta correcta |
|--------|--------------------|
| `2000` | opción 1 |
| `0200` | opción 2 |
| `0020` | opción 3 |
| `0002` | opción 4 |
| `2020` | opciones 1 y 3 |
| `2222` | opciones 1, 2, 3 y 4 |

---

## 📝 Ejemplo de una pregunta con una sola respuesta correcta

```xml
<c>
  <p>¿Cuál es la capital de España?</p>
  <c>2000</c>
  <r>
    <o>Madrid</o>
    <o>Barcelona</o>
    <o>Sevilla</o>
    <o>Valencia</o>
  </r>
</c>
```

En este caso, la opción correcta es la primera.

---

## 📝 Ejemplo de una pregunta con varias respuestas correctas

```xml
<c>
  <p>¿Cuáles de los siguientes números son pares?</p>
  <c>0202</c>
  <r>
    <o>1</o>
    <o>2</o>
    <o>3</o>
    <o>4</o>
  </r>
</c>
```

En este caso, son correctas las opciones 2 y 4.

---

## 📦 Ejemplo completo de fichero XML

```xml
<?xml version="1.0" encoding="UTF-8"?>
<test>
  <c>

    <c>
      <p>¿Cuál es la capital de España?</p>
      <c>2000</c>
      <r>
        <o>Madrid</o>
        <o>Barcelona</o>
        <o>Sevilla</o>
        <o>Valencia</o>
      </r>
    </c>

    <c>
      <p>¿Qué lenguaje utiliza este proyecto?</p>
      <c>2000</c>
      <r>
        <o>Python</o>
        <o>Java</o>
        <o>C++</o>
        <o>PHP</o>
      </r>
    </c>

    <c>
      <p>¿Cuáles de estos números son pares?</p>
      <c>0202</c>
      <r>
        <o>1</o>
        <o>2</o>
        <o>3</o>
        <o>4</o>
      </r>
    </c>

  </c>
</test>
```

---

## ⚠️ Reglas importantes

### 1. El XML debe estar bien formado
Todas las etiquetas deben abrirse y cerrarse correctamente.

Correcto:

```xml
<p>Pregunta</p>
```

Incorrecto:

```xml
<p>Pregunta
```

---

### 2. Cada pregunta debe tener sus etiquetas obligatorias

Cada bloque de pregunta debe incluir:

- `<p>`
- `<c>`
- `<r>`
- al menos una etiqueta `<o>`

---

### 3. El número de posiciones del código debe coincidir con las opciones

Si tienes 3 opciones:

```xml
<r>
  <o>A</o>
  <o>B</o>
  <o>C</o>
</r>
```

el código debería tener 3 posiciones, por ejemplo:

```xml
<c>020</c>
```

Si tienes 4 opciones, el código debería tener 4 posiciones.

---

### 4. El proyecto actual guarda hasta 4 opciones por pregunta

La tabla SQLite creada por `import.py` contiene estos campos:

- `option1`
- `option2`
- `option3`
- `option4`

Por tanto, actualmente el sistema está preparado para almacenar **hasta 4 respuestas por pregunta**.

Si el XML contiene más de 4 opciones, las adicionales no se guardarán.

---

### 5. Las preguntas con menos de 4 opciones son válidas

Puedes usar preguntas con 2, 3 o 4 respuestas.

Ejemplo con 3 opciones:

```xml
<c>
  <p>¿Qué color resulta de mezclar azul y amarillo?</p>
  <c>020</c>
  <r>
    <o>Rojo</o>
    <o>Verde</o>
    <o>Morado</o>
  </r>
</c>
```

---

## 🚀 Cómo importar el XML

Una vez creado el fichero `test.xml`, ejecuta:

```bash
python3 import.py
```

Si todo va bien, aparecerá un mensaje como este:

```text
Importación completada. Total preguntas insertadas: 25
```

---

## 🛠 Recomendaciones prácticas

- usa siempre codificación UTF-8
- revisa tildes, signos y caracteres especiales
- evita etiquetas vacías
- procura que el número de opciones coincida con la longitud del código
- mantén una redacción clara y homogénea en todas las preguntas

---

## 🔍 Errores habituales

### Error: `NoneType has no attribute 'strip'`
Suele ocurrir cuando falta contenido en alguna etiqueta, por ejemplo:

```xml
<p></p>
```

o si la etiqueta directamente no existe.

---

### Error: pregunta mal estructurada
Ocurre si una pregunta no contiene `<p>`, `<c>` o `<r>`.

---

### Error: respuestas incorrectas mal codificadas
Si el código no coincide con las opciones, la importación puede ser errónea aunque el XML sea válido.

Ejemplo incorrecto:

- 3 opciones
- código `2000`

Aquí sobra una posición.

---

## 📚 Resumen rápido

Cada pregunta debe seguir este esquema:

```xml
<c>
  <p>Enunciado de la pregunta</p>
  <c>Código de respuestas correctas</c>
  <r>
    <o>Opción 1</o>
    <o>Opción 2</o>
    <o>Opción 3</o>
    <o>Opción 4</o>
  </r>
</c>
```

Y el documento completo debe envolverse así:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<test>
  <c>
    ...preguntas...
  </c>
</test>
```

---

## 📎 Compatibilidad con el proyecto

Este formato está pensado para el comportamiento actual de:

- `import.py`
- `show.py`
- `editar.py`
- `examen.py`

Si en el futuro cambias la estructura de la base de datos o amplías el número
de respuestas posibles, este formato también deberá actualizarse.