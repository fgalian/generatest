# 🧠 Sistema de Exámenes Tipo Test en Python

Este proyecto implementa un sistema completo para gestionar, practicar y
evaluar **preguntas tipo test** utilizando una base de datos SQLite y
varios scripts en Python.

---

## 👨‍💻 Información del Proyecto

- **Autor:** Francisco Javier Sánchez Galián  
- **Lenguaje principal:** Python 3  
- **Base de datos:** SQLite  
- **Última actualización:** Marzo 2026
- **Estado:** Activo / En mejora continua  
- **Licencia:** Uso libre personal  

---


## 📂 Estructura del proyecto

    .
    ├── import.py
    ├── show.py
    ├── examen.py
    ├── editar.py
    ├── test.db
    ├── Test.xml
    └── README.md

## 🛠 Requisitos

-   Python 3.8+
-   SQLite
-   Terminal con colores ANSI

## 🧩 Importar preguntas desde XML

    python3 import.py

## 📄 Formato del fichero XML

Si quieres crear o editar manualmente el fichero XML para importar preguntas,
consulta la documentación detallada aquí:

- [Ver formato del fichero XML](./FORMATOXML.md)

## 🎯 Estudiar preguntas sueltas

    python3 show.py

## 📝 Editar preguntas

    python3 editar.py

## 🧪 Modo examen avanzado

    python3 examen.py