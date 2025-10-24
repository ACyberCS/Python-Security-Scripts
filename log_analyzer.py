import os
import re
from collections import Counter

directorio_base = os.path.dirname(os.path.abspath(__file__))
arch_log = os.path.join(directorio_base, "auth.log")

# --- ESTRUCTURAS DE DATOS ANTES DEL ANÁLISIS (AQUÍ SE ALMACENARAN LOS DATOS CAPTURADOS) ---
total_fallos = 0
ip_fallidos = set()
usr_fallidos = set()
ip_intentos = Counter()

# --- LECTURA DEL ARCHIVO "AUTH.LOG" LÍNEA POR LINEA E IDENTIFICACIÓN DE LÍNEAS ÚNICAS "FAILED PASSWORD" ---
with open (arch_log, "r") as auth_log:
    for linea_log in auth_log:
        # CAPTURA NOMBRE DE USUARIO Y DIRECCIÓN IP CON LOGIN FALLIDO
        match = re.search(r"Failed password for (?:invalid user|user) (\w+) from ([\d.]+) port (\d+)", linea_log)
        '''PATRÓN BUSCADO: Failed password for (puede coincidir con invalid user O user) (coincide con 
        uno o más caracteres alfanuméricos y guiones bajos) from (coincide con un o más dígitos o 
        puntos) port (coincide con uno o más dígitos)'''
        if match:
            usr = match.group(1)
            ip = match.group(2)

            # CONTEO TOTAL DE INTENTOS DE LOGIN FALLIDOS, ENLISTADO DE DIRECCIONES IP Y NOMBRE DE USUARIOS QUE LO COMETIERON
            total_fallos +=1
            
            ip_fallidos.add(ip)
            usr_fallidos.add(usr)
            # CONTEO DE INTENTOS POR CADA IP
            ip_intentos[ip] +=1

# --- IMPRESIÓN DE RESUMEN SOBRE EL ANÁLISIS ---
print("--- ANÁLISIS DE SEGURIDAD COMPLETADO ---\n")
print(f"[*] Número total de intentos de login fallidos: {total_fallos}")
print(f"\n[*] Direcciones IP únicas con intentos fallidos:")
for ip in sorted(list(ip_fallidos)): # IMPRESIÓN EN FORMATO DE LISTA
    print(f"   - {ip}")
print(f"\n[*] Nombres de usuario únicos intentados:")
for usr in sorted(list(usr_fallidos)):
    print(f"   - {usr}")

# --- ALERTA DE POSIBLE ATAQUE DE FUERZA BRUTA ---
print("\n--- ALERTA DE SEGURIDAD ---")
alerta = False
for ip, intentos in ip_intentos.items():
    if intentos > 2:
        print(f"[!] ALERTA: Posible ataque de fuerza bruta desde la IP: {ip} con ({intentos} intentos fallidos).\n")
        alerta = True
if not alerta:
    print("[-] No se detectaron actividades de fuerza bruta sospechosas.\n")