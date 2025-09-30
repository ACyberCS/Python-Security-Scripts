# organizador.py
## Descripción
Este script de Python se diseño para automatizar la organización de ficheros dentro de un directorio especifico. 
Su función principal es tomar todos los ficheros ubicados en un directorio llamado `evidencia_desorganizada` y moverlos a un directorio de destino llamado `evidencia_organizada`.
Dentro de `evidencia_organizada`, el script crea automáticamente sub directorios basados en la extensión de cada fichero (por ejemplo, pdf, jpg, docx) y coloca el fichero correspondiendo dentro de su sub directorio.

- **Objetivo:** Clasificar ficheros por tipo de manera eficiente
- **Módulos Clave:** Utiliza `os` para la manipulación de rutas de ficheros y directorios, y `shutil` para la operación de mover (`move`)
## Uso o Funcionamiento
Para que el script funcione correctamente, se debe seguir este proceso:
1. **Estructura Inicial:** El script asume que existe un directorio llamado `evidencia_desorganizada` en el mismo directorio donde se ejecuta el `organizador.py` . Este directorio debe contener los ficheros que se desean organizar.
2. **Ejecución:** Al ejecutar el script, este realiza las siguientes acciones:
	-  Verifica si el directorio de destino, `evidencia_organizada` , existe. Si no, lo crea.
	-  Itera sobre cada elemento dentro de `evidencia_desorganizada`
	- Para cada fichero encontrado, extrae su extensión (por ejemplo, de `documento.pdf`, extrae `.pdf` ).
	-  Crea un sub directorio con el nombre de la extensión (sin el punto inicial) dentro de `evidencia_organizada`. Si ya existe, no hace nada.
	-  Mueve el fichero original desde `evidencia_desorganizada` al sub directorio recién creado.
3. **Manejo de Errores:** Incluye manejo de excepciones para avisar si el directorio `evidencia_desorganizada` no se encuentra

## Ejemplo de Salida

**🖥️ Escenario 1: Ejecución Exitosa**

Condiciones iniciales del directorio:
```
. 
├── script.py 
└── evidencia_desorganizada 
    ├── informe.pdf 
    ├── foto_1.jpg 
    ├── datos.xlsx 
    └── nota.txt
```

Salida de la Consola (Output):
```
Iniciando la organización de ficheros...
Organización completa con éxito!
```

Resultado final del directorio:
```
. 
├── script.py 
├── evidencia_desorganizada # Queda vacía 
└── evidencia_organizada 
    ├── pdf 
        └── informe.pdf 
    ├── jpg 
        └── foto_1.jpg 
    ├── xlsx 
        └── datos.xlsx 
    └── txt 
        └── nota.txt
```

**🖥️ Escenario 2: Error por directorio No encontrada**

Condiciones iniciales del directorio:
(El directorio `evidencia_desorganizada` no existe)

Salida de la Consola (Output):
```
Iniciando la organización de ficheros...
Error! No se encontró el directorio 'ruta/absoluta/donde/se/espera/evidencia_desorganizada'. Asegúrate de que existe.
```