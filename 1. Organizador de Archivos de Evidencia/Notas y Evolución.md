# 📝Notas y Evolución - organizador.py
Este documento registra una bitácora de desarrollo y seguimiento del script. Funciona como un historial completo que narra la evolución de sus versiones, con el propósito de documentar de manera ordenada el proceso de concepción, asegurando que el resultado final cumpla con todos los requerimientos propuestos.

### Escenario propuesto: 
Eres un analista forense junior y acabas de recibir un volcado de datos de un disco duro. Los archivos están todos mezclados en una sola carpeta llamada `evidencia_desorganizada`. Tu tarea es crear un script de Python que los organice en subcarpetas según su tipo de archivo (extensión).

### Objetivos a cumplir:
1. Tu script debe crear una carpeta principal llamada `evidencia_organizada`.
2. Dentro de `evidencia_organizada`, debe crear subcarpetas basadas en las extensiones de los archivos que encuentre (por ejemplo: logs, textos, imágenes).
3. El script debe mover cada archivo de la carpeta `evidencia_desorganizada` a la subcarpeta correspondiente dentro de `evidencia_organizada`.

### Requisitos pedidos del Script (`organizador.py`):
1. Debe usar el módulo `os` para leer los archivos de la carpeta `evidencia_desorganizada`.
2. Para cada archivo, debe extraer su extensión (p. ej., de `"access.log"`, la extensión es "log").
3. Debe verificar si ya existe una carpeta para esa extensión dentro de `evidencia_organizada`. Si no existe, debe crearla.
4. Debe mover el archivo desde `evidencia_desorganizada` a la carpeta de destino correcta.

### V.1 - Primera version funcional

**📌 Objetivos cumplidos:**
-  Crear un directorio llamado `evidencia_organizada` en caso de no existir
-  Crear sub directorios de evidencia en `evidencia_organizada` por tipo de extension
-  Mover los ficheros de `evidencia_desorganizada` a los sub directorios de `evidencia_organizada` correctos

```
import os
import shutil

destino = 'evidencia_organizada'
ruta = 'evidencia_desorganizada'

if not os.path.exists(destino):
    os.mkdir(destino)

for file in os.listdir(ruta):
    nm_evidencia, extension = os.path.splitext(file)
    if extension:
        subcarpeta = extension[1:]
        destino_subcarpeta = os.path.join(destino, subcarpeta)
        if not os.path.exists(destino_subcarpeta):
            os.mkdir(destino_subcarpeta)
    if file.endswith(extension):
        mov_inicial = os.path.join(ruta, file)
        mov_final = os.path.join(destino_subcarpeta,file)
        shutil.move(mov_inicial, mov_final)
```

**🔧 Observaciones a corregir:**
-   Es mejor usar `os.makedirs()` a `os.mkdir`  → puesto que se puede crear directorios anidados de forma recursiva
-  Agregar un aviso de procesamiento del script → mejoraremos la interacción y visualización del script trabajando
-  Preferible usar `filename` sobre `file` → refiere al nombre de un fichero como una cadena de texto
-  Eliminar línea `if file.endswith(extension):` → dentro del `for` ya se ha extraído la extensión, por lo que no es estrictamente necesaria, el script funciona sin ella
### V.2 - Versión corregida de las anteriores observaciones

```
import os
import shutil

destino = 'evidencia_organizada'
ruta = 'evidencia_desorganizada'

if not os.path.exists(destino):
    os.makedirs(destino)

print("Iniciando la organización de archivos...")

for filename in os.listdir(ruta):
    pos_inicial = os.path.join(ruta, filename)
    
    if os.path.isfile(pos_inicial):
        nm_archivo, extension = os.path.splitext(filename)
    if extension:
        nm_subcarpeta = extension[1:]
        destino_subcarpeta = os.path.join(destino, nm_subcarpeta)
        if not os.path.exists(destino_subcarpeta):
            os.makedirs(destino_subcarpeta)
        pos_final = os.path.join(destino_subcarpeta, filename)
        shutil.move(pos_inicial, pos_final)

print("Organización completada con éxito!")
```

**🔧 Observaciones a corregir:**
-  Presenta error al cambiar la  ubicación de directorios  externamente → se necesita asegurar que las rutas siempre apunten a la ubicación correcta, sin importar desde dónde se ejecute el script
-  (Opcional no requerido) Cambio de palabras:  de `archivo ` a `fichero` y de `carpeta` a `directorio`
### V.3 - Final de Script

**📌 Objetivos cumplidos:**
-  Construir una ruta absoluta para ejecutar el script sin importar donde se encuentre  → y redefinimos  las variables `ruta` y `destino` 
-  Adicional, se añadió un bloque `try-except` para manejar posibles errores, como la no existencia del directorio `evidencia_desorganizada`

```
import os
import shutil

directorio_base = os.path.dirname(os.path.abspath(__file__))

destino = os.path.join(directorio_base, 'evidencia_organizada')
ruta = os.path.join(directorio_base, 'evidencia_desorganizada')

if not os.path.exists(destino):
    os.makedirs(destino)

print("Iniciando la organización de ficheros...")

try:
    for filename in os.listdir(ruta):
        pos_inicial = os.path.join(ruta, filename)
        if os.path.isfile(pos_inicial):
            # Extrae la extensión
            nm_fichero, extension = os.path.splitext(filename)
        if extension:
            nm_subdirectorio = extension[1:]
            destino_subdirectorio = os.path.join(destino, nm_subdirectorio)
            if not os.path.exists(destino_subdirectorio):
                os.makedirs(destino_subdirectorio)
            pos_final = os.path.join(destino_subdirectorio, filename)
            shutil.move(pos_inicial, pos_final)
    print("Organización completada con éxito!")
except FileNotFoundError:
    print(f"Error! No se encontró el directorio '{ruta}'. Asegúrate de que existe.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")
```