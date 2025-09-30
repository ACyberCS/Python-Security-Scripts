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