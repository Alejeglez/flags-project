import json
import re
import io
import os
import sys
import requests
import uuid 

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

header = {'User-Agent': 'AstroFlagBot/0.0 (https://example.org/coolbot/; coolbot@example.org)'}

def main():

    with open("flags.json", encoding="utf-8") as file:
        countries = json.load(file)

    if not os.path.exists('flags_images'):
        os.makedirs('flags_images')

    for country in countries:
        flag_url = country.get("flag_url")
        design = country.get("design")
        name = country.get("name")
        if flag_url is not None and design is not None:
            try:
                response = requests.get("https:" + str(flag_url))
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
                
                i += 1

            except requests.RequestException as e:
                print("Se consiguieron" + str(i) + "banderas")
                print(f"Error al descargar la imagen de {flag_url}: {e}")
    
    print("Proceso finalizado")

if __name__ == "__main__":
    main()
