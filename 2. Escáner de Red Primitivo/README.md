# scanner.py
## Descripción
Este script de Python funciona como un **monitor de conectividad** simple, diseñado para verificar el estado de una lista de servidores críticos. Lee direcciones IP desde un fichero de texto (`ips_servidores.txt`) y ejecuta el comando **`ping`** para cada una.
Su propósito es determinar si cada servidor está "EN LÍNEA" o "FUERA DE LÍNEA" y registrar los resultados, incluyendo la latencia, en un fichero de reporte con marca de tiempo.

- **Función Clave:** Utiliza el módulo `subprocess` para interactuar con el sistema operativo y ejecutar comandos externos (`ping`)
- **Compatibilidad:** El uso del argumento `"-n", "1"` en el comando `ping` lo hace específicamente compatible con **sistemas operativos Windows**
-  **Módulos adicionales:** `os` - `datetime` - `re` 
## Uso o Funcionamiento
Para utilizar este script, se necesita una estructura de ficheros específica y se ejecuta en un ambiente Windows:

1. **Fichero de Entrada (`ips_servidores.txt`):** Debe existir en el mismo directorio que el script. Este fichero debe contener una lista de direcciones IP o nombres de host, una por línea.
```
		# Ejemplo de ips_servidores.txt 
		192.168.1.1 
		10.0.0.50 
		servidor-web.com 
		192.168.1.250
```
2. **Ejecución:** Al ejecutar el `scanner.py`, este realiza lo siguiente:
	-  Crea (o sobrescribe) un fichero de salida llamado `reporte_conectividad.txt` en el mismo directorio, encabezándolo con una marca de tiempo de inicio.
	-  Lee cada IP de `ips_servidores.txt`
	-  Ejecuta `ping -n 1 <IP>` para enviar un único paquete de prueba a la IP
	-  **Evalúa el Resultado:**
		- Si el comando `ping` retorna con código `0`, el servidor está "EN LÍNEA". El script busca la latencia (`tiempo=XXms`) usando expresiones regulares (`re`) y la registra.
		- Si retorna con un código diferente a `0`, el servidor está "FUERA DE LÍNEA". Intenta capturar el mensaje de error de la salida del  `ping` para registrar la causa (ej: "Tiempo de espera agotado")
	- Muestra el progreso y el resultado en la consola, y escribe la misma información detallada en el fichero de reporte
## Ejemplo de Salida

Asumiendo que `192.168.1.1` responde rápidamente, `10.0.0.50` no responde, y `servidor-web.com` responde con latencia moderada.

**Salida de la Consola (Output):**

```
Iniciando escaneo de red... 
[Verficando 192.168.1.1...] 
EN LINEA (Latencia: 2 ms) 
[Verficando 10.0.0.50...] 
FUERA DE LINEA (Tiempo de espera agotado.) 
[Verficando servidor-web.com...] 
EN LINEA (Latencia: 55 ms) 
[Verficando 192.168.1.250...] 
FUERA DE LINEA (Host de destino inaccesible.) 

Ecaneo completado! Los resultados se han guardado en /ruta/al/directorio/reporte_conectividad.txt
```

**Ejemplo de Fichero Generado (`reporte_conectividad.txt`)**

El contenido del fichero reflejará las marcas de tiempo y los estados de conectividad.

```
--- REPORTE DE CONECTIVIDAD GENERADO EL: 2025-09-28 19:15:30 --- 

[19:15:31] 192.168.1.1 | ESTADO: EN LINEA | LATENCIA: 2 ms 
[19:15:32] 10.0.0.50 | ESTADO: FUERA DE LINEA | CAUSA: Tiempo de espera agotado. 
[19:15:33] servidor-web.com| ESTADO: EN LINEA | LATENCIA: 55 ms 
[19:15:34] 192.168.1.250 | ESTADO: FUERA DE LINEA | CAUSA: Host de destino inaccesible.
```