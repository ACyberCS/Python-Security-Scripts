import requests
import os
from datetime import datetime

# --- CONFIGURACIÓN DE RUTAS Y ARCHIVOS ---
root_dir = os.path.dirname(os.path.abspath(__file__))
URL_file = os.path.join(root_dir, "sitios_empresa.txt")

if not os.path.exists(URL_file):
    with open(URL_file, "w") as f:
        f.write("")

now = datetime.now()
date_str = now.strftime("%Y-%m-%d")
REPORT_file = os.path.join(root_dir, f"Reporte_Auditoria_Web_{date_str}.txt")

# --- AUDITORIA WEB ---
with open(REPORT_file, "w", encoding="utf-8") as report:
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    report.write(f"--- REPORTE DE AUDITORIA WEB | GENERADO EL {timestamp} ---\n\n")

    with open(URL_file, "r") as file:
        for line in file:
            url = line.strip()
            # --- GENERADOR DE REPORTE ---
            try:
                response = requests.get(url, timeout=3)
            except requests.ConnectionError:
                report.write(f"URL Auditada: {url}\nCódigo HTTP: N/A\nEstado: INACCESIBLE (Error de conexión)\nInformación del servidor: N/A\n\n")
            except requests.Timeout:
                report.write(f"URL Auditada: {url}\nCódigo HTTP: N/A\nEstado: TIMEOUT (La solicitud tardó más de 3s)\nInformación del servidor: N/A\n\n")
            # manejara cualquier otro error genérico de requests y lo reportara
            except requests.RequestException as e:
                report.write(f"URL Auditada: {url}\nEstado: ERROR DESCONOCIDO\nDetalle: {e}\n\n")
            else:
                # SE EJECUTARA SOLO SI EL 'TRY' FUNCIONÓ
                code_HTTP = response.status_code
                if code_HTTP == 200:
                    status = "EN LiNEA"
                elif code_HTTP == 404:
                    status = "NO ENCONTRADO"
                elif code_HTTP >= 500:
                    status = "ERROR DE SERVIDOR"
                elif code_HTTP >= 400:
                    status = "ERROR DE CLIENTE"
                else:
                    status = f"INACCESIBLE, CÓDIGO INESPERADO ({code_HTTP})"
                
                server = response.headers.get('Server')
                if server:
                    server_info = f"EXPUESTO ({server})"
                else:
                    server_info = "BUENA PRACTICA! (Oculto)"

                report.write(f"URL Auditada: {url}\nCódigo HTTP: {code_HTTP}\nEstado:  {status}\nInformación del servidor: {server_info}\n\n")

# --- MENSAJE EN TERMINAL ---
nm_report = os.path.basename(REPORT_file)
print(f"Auditoria completada! Revisa el archivo [{nm_report}]")