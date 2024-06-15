import json
import re
import io
import os
import sys
import requests
import uuid 
import time
import signal

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

header = {'User-Agent': 'AstroFlagBot/0.0 (https://github.com/Alejeglez/flags-project/blob/main/README.md)'}

def save_to_json(countries):
    with open("flags.json", "w", encoding="utf-8") as file:
        json.dump(countries, file, ensure_ascii=False, indent=4)
    print("Archivo JSON actualizado correctamente.")

def signal_handler(sig, frame):
    print('Interrupción detectada, guardando datos...')
    save_to_json(countries)
    sys.exit(0)

signal.signal(signal.SIGINT, signal_handler)

def main():
    global countries

    with open("flags.json", encoding="utf-8") as file:
        countries = json.load(file)

    if not os.path.exists('flags_images'):
        os.makedirs('flags_images')

    for country in countries:
        flag_url = country.get("flag_url")
        design = country.get("design")
        name = country.get("name")
        uuid_value = country.get("uuid")

        if uuid_value is not None:
            continue

        elif flag_url is not None and design is not None:
            try:
                response = requests.get("https:" + str(flag_url), headers=header)
                response.raise_for_status()

                file_extension = os.path.splitext(flag_url)[-1]
                uuid_file_name = str(uuid.uuid4())
                unique_file_name_img = uuid_file_name + file_extension
                unique_file_name_text = uuid_file_name + ".txt"
                file_path_img = os.path.join('flags_images', unique_file_name_img)

                with open(file_path_img, 'wb') as file:
                    file.write(response.content)

                file_path_text = os.path.join('flags_images', unique_file_name_text)
                
                with open(file_path_text, 'w', encoding='utf-8') as file:
                    if name is not None:
                        file.write(f"{name} ")
                    file.write(f"{design}")
                
                country["uuid"] = uuid_file_name
                print(f"Imagen de {flag_url} descargada correctamente.")
                time.sleep(15)


            except requests.RequestException as e:
                print(f"Error al descargar la imagen de {flag_url}: {e}")
    
    save_to_json(countries)
    print("Proceso finalizado")

if __name__ == "__main__":
    main()
