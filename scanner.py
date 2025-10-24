import subprocess
import os
from datetime import datetime
import re 

print(f'Iniciando escaneo de red...')

# --- CONFIGURACIÓN DE RUTAS Y ARCHIVOS ---
root_dir = os.path.dirname(os.path.abspath(__file__))
IPS_file = os.path.join(root_dir, 'ips_servidores.txt')

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
REPORT_file = os.path.join(root_dir, f'Reporte_de_Conectividad_{date_str}.txt')

# --- VERIFICADOR DE ESTADO DE CONECTIVIDAD DE SERVIDORES Y GENERADOR DE REPORTE ---
with open(REPORT_file, 'w') as report:
    start_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report.write(f"--- REPORTE DE CONECTIVIDAD GENERADO EL: {start_timestamp} ---\n\n")
    
    with open(IPS_file, 'r') as critical_servers:
        for line in critical_servers:
            ip_clean = line.strip()
            if not ip_clean:
                continue
            
            print(f"[Verificando {ip_clean}...]")
            
            command = ["ping", "-n", "1", ip_clean]
            result = subprocess.run(command, capture_output=True, text=True, check=False)
            
            timestamp_check = datetime.now().strftime("%H:%M:%S")
            
            if result.returncode == 0:
                match = re.search(r"tiempo=(\d+)ms", result.stdout)
                if match:
                    latency = match.group(1)
                    additional_info = f"LATENCIA: {latency} ms"
                    print(f"EN LINEA (Latencia: {latency} ms)")
                else:
                    additional_info = "Repuesta inesperada"
                    print ("EN LINEA (Respuesta inesperada)")

                report.write(f"[{timestamp_check}] {ip_clean:15} | ESTADO: EN LINEA | {additional_info}\n")
            else:
                error_msg = "Error desconocido"
                lineas_salida = result.stdout.strip().split('\n')
                if len(lineas_salida) > 1:
                    error_msg = lineas_salida[1].strip()
                
                print(f"FUERA DE LINEA ({error_msg})")
                report.write(f"[{timestamp_check}] {ip_clean:15} | ESTADO: FUERA DE LINEA | CAUSA: {error_msg}\n")

nm_report = os.path.basename(REPORT_file)
print(f"\nEscaneo completado! Los resultados se han guardado en el archivo [{nm_report}]")