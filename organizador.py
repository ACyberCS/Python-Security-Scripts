import os
import shutil

# --- CONFIGURACIÓN DE RUTAS Y DIRECTORIOS ---
root_dir = os.path.dirname(os.path.abspath(__file__))
start_dir = os.path.join(root_dir, 'Evidencia Desorganizada')
end_dir = os.path.join(root_dir, 'Evidencia Organizada')

os.makedirs(start_dir, exist_ok=True)
os.makedirs(end_dir, exist_ok=True)

print("Iniciando la organización de archivos...\n")

# --- ORGANIZADOR DE FICHEROS ---
organized_files = 0
try:
    for file_name in os.listdir(start_dir):
        starting_point = os.path.join(start_dir, file_name)
        
        if os.path.isfile(starting_point):
            name_file, extension = os.path.splitext(file_name)
        
            if extension:
                subdir_name = extension[1:].lower()
            else:
                subdir_name = "ARCHIVOS SIN EXTENSION"
            
            subdir_destination = os.path.join(end_dir, subdir_name)
            if not os.path.exists(subdir_destination):
                os.makedirs(subdir_destination)
        
            end_point = os.path.join(subdir_destination, file_name)
            shutil.move(starting_point, end_point)
            organized_files += 1 # Actúa como contador que rastrea cuántas veces se ha ejecutado una acción exitosamente

    new_dir = os.path.basename(end_dir)
    old_dir = os.path.basename(start_dir)
    if organized_files >0:
        print(f"Organización de ficheros completada! Revisa el directorio '{new_dir}.'")
    else:
        print("[!] PROCESO INTERRUMPIDO")
        print(f"Atención! La carpeta '{old_dir}' no encuentra archivos para organizar.\n""Coloque los archivos a organizar en la carpeta para comenzar.")
except FileNotFoundError:
    dir_name = os.path.basename(start_dir)
    print(f"Error! No se encontró la carpeta '{dir_name}'. Asegúrate de que existe.")
except Exception as e:
    print(f"Ocurrió un error inesperado: {e}")