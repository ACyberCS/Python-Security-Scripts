# 📝Notas y Evolución - scanner.py
Este documento registra una bitácora de desarrollo y seguimiento del script. Funciona como un historial completo que narra la evolución de sus versiones, con el propósito de documentar de manera ordenada el proceso de concepción, asegurando que el resultado final cumpla con todos los requerimientos propuestos.

### Escenario propuesto: 
Eres un Analista de Seguridad en un Centro de Operaciones de Seguridad (SOC). Se te ha entregado un archivo de texto, `ips_servidores.txt`, que contiene una lista de las direcciones IP de los servidores críticos de la empresa. Tu supervisor te ha pedido que crees un script para verificar rápidamente el estado de conectividad de todos estos servidores.
### Objetivos a cumplir:
1. Tu script debe leer el archivo `ips_servidores.txt`, que contiene una dirección IP por línea.
2. Para cada dirección IP leída del archivo, debe ejecutar el comando `ping`.
3. Basándose en el `returncode` del comando `ping`, el script debe imprimir en la consola un reporte claro, indicando si cada servidor está **EN LÍNEA** o **FUERA DE LÍNEA**.
-----
 - 🏆 Objetivo Adicional (Opcional): Si te sientes con confianza, modifica tu script para que, además de imprimir el reporte en pantalla, lo escriba en un nuevo archivo llamado `reporte_conectividad.txt`
---
### Requisitos pedidos del Script (`scanner.py`):
1. Debe usar `with open(...)` para abrir y leer el archivo `ips_servidores.txt`.
2. Debe usar un bucle `for` para iterar sobre cada línea (cada IP) del archivo.
3. Dentro del bucle, debe utilizar `subprocess.run()` para hacer `ping` a la IP actual.
4. Debe usar una estructura `if/else` para comprobar el `resultado.returncode` y mostrar el estado correspondiente.

### V.1 - Primera version funcional

**📌 Objetivos cumplidos:**
-  Lee el fichero `ips_servidores.txt` línea por línea
-  Ejecuta por cada IP leída el comando `ping`
-  Imprime información básica del estado ("EN LÍNEA" o "FUERA DE LÍNEA") en  la consola

```
import subprocess
import os

print(f'Procesando lectura de fichero...')

directorio_base = os.path.dirname(os.path.abspath(__file__))
fichero = os.path.join(directorio_base, 'ips_servidores.txt')

with open(fichero) as servidores_criticos:
    for linea in servidores_criticos:
        ip_limpia = linea.strip()
        comando = ["ping", "-n", "1", ip_limpia]
        resultado = subprocess.run(comando, capture_output=True, text=True, check=False)
        if resultado.returncode == 0:
            print(f"EN LÍNEA")
        else:
            print(f"FUERA DE LÍNEA")
```

**🔧 Observaciones a corregir:**
-  No cuenta con informe de reporte
-  La información proporcionada en la consola no da mucha información

### V.2 - Con informe de reporte básico y obtención de datos como, la latencia y  el error si existe

**📌 Objetivos cumplidos:**
-  Impresión de datos en terminal y en fichero de `reporte_conectividad.txt` 
-  El reporte de conectividad brinda información básica de conectividad: fecha de verificación, IP a verificar y el estado de conexión

```
import subprocess
import os
from datetime import datetime

print(f'Iniciando escaneo de red...')

directorio_base = os.path.dirname(os.path.abspath(__file__))
fichero_ips = os.path.join(directorio_base, 'ips_servidores.txt')
fichero_reporte = os.path.join(directorio_base, 'reporte_conectividad.txt')

with open(fichero_reporte, 'w') as reporte:
    timestamp_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte.write(f"--- Reporte de Conectividad generado el {timestamp_inicio} --\n\n")
    
    with open(fichero_ips, 'r') as servidores_criticos:
        for linea in servidores_criticos:
            ip_limpia = linea.strip()
            if not ip_limpia:
                continue
            
            print(f"[Verficando {ip_limpia}...]")
            comando = ["ping", "-n", "1", ip_limpia]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=False)
            timestamp_check = datetime.now().strftime("%H:%M:%S")
            
            if resultado.returncode == 0:
                print(f"ESTADO: EN LINEA")
                print(f"Respuesta del ping:")
                print(resultado.stdout)
                reporte.write(f"[{timestamp_check}] {ip_limpia:15} | ESTADO: EN LINEA\n")
            else:
                print(f"ESTADO: FUERA DE LINEA")
                print(resultado.stderr)
                print(f"Respuesta del ping:")
                reporte.write(f"[{timestamp_check}] {ip_limpia:15} | ESTADO: FUERA DE LINEA\n")

print(f"\n Ecaneo completado! Los resultados han sido guardados en {fichero_reporte}")
```

**🔧 Observaciones a corregir:**
-  Al reporte le falta agregar información de latencia y causa de error del estado "FUERA DE LÍNEA"

### V.3 - Con reporte avanzado, capturando información de latencia y causa de errores

**📌 Objetivos cumplidos:**
-  Impresión en consola de estado de conectividad, latencia y error, en caso de existir → captura de datos específicos por expresiones Regulares (Regex)
-  Creación de reporte de conectividad que incluye: fecha de verificación, IP a verificar, estado de conectividad, latencia o causa de error

**📓 Complemento de aprendizaje:**
-  Expresiones Regulares (Regex) para la búsqueda y manipulación de patrones de texto se trabajo con el módulo `re` → Capturamos datos de latencia y causa de errores
	-  Patrón de interés →  `tiempo=XXms`
	-  Cuando el `ping` falla, en **Windows** los errores a menudo se encuentran `.stdout` como "Host de destino inaccesible" o "Tiempo de espera agotado para esta solicitud"

```
import subprocess
import os
from datetime import datetime
import re

print(f'Iniciando escaneo de red...')

directorio_base = os.path.dirname(os.path.abspath(__file__))
fichero_ips = os.path.join(directorio_base, 'ips_servidores.txt')
fichero_reporte = os.path.join(directorio_base, 'reporte_conectividad.txt')

with open(fichero_reporte, 'w') as reporte:
    timestamp_inicio = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    reporte.write(f"--- REPORTE DE CONECTIVIDAD GENERADO EL: {timestamp_inicio} ---\n\n")

    with open(fichero_ips, 'r') as servidores_criticos:
        for linea in servidores_criticos:
            ip_limpia = linea.strip()
            if not ip_limpia:
                continue

            print(f"[Verficando {ip_limpia}...]")

            comando = ["ping", "-n", "1", ip_limpia]
            resultado = subprocess.run(comando, capture_output=True, text=True, check=False)
            
            timestamp_check = datetime.now().strftime("%H:%M:%S")

            if resultado.returncode == 0:
                match = re.search(r"tiempo=(\d+)ms", resultado.stdout)

                if match:
                    latencia = match.group(1)
                    info_adicional = f"LATENCIA: {latencia} ms"
                    print(f"EN LINEA (Latencia: {latencia} ms)")
                else:
                    info_adicional = "Repuesta inesperada"
                    print ("EN LINEA (Respuesta inesperada)")

                reporte.write(f"[{timestamp_check}] {ip_limpia:15} | ESTADO: EN LINEA | {info_adicional}\n")

            else:
                error_msg = "Error desconocido"
                lineas_salida = resultado.stdout.strip().split('\n')
                if len(lineas_salida) > 1:
                    error_msg = lineas_salida[1].strip()
                
                print(f"FUERA DE LINEA ({error_msg})")
                reporte.write(f"[{timestamp_check}] {ip_limpia:15} | ESTADO: FUERA DE LINEA | CAUSA: {error_msg}\n")

print(f"\nEscaneo completado! Los resultados se han guardado en {fichero_reporte}")
```