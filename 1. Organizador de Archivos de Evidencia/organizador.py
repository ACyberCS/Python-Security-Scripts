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