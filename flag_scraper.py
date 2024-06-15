import requests
from bs4 import BeautifulSoup
import sys
import io
import json

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

#Especial atención a la sección external links: https://en.wikipedia.org/wiki/National_flag

def get_flags_endpoints():
    url = "https://en.wikipedia.org/wiki/Gallery_of_sovereign_state_flags"

    response = requests.get(url)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find("body")
    first_div = body.find("div", class_="mw-page-container")
    second_div = first_div.find("div", class_="mw-page-container-inner")
    third_div = second_div.find("div", class_="mw-content-container")
    first_main = third_div.find("main", class_="mw-body")
    fourth_div = first_main.find("div", {"class": ["vector-body", "ve-init-mw-desktopArticleTarget-targetContainer"]})
    fith_div = fourth_div.find("div", class_="mw-body-content")
    sixth_div = fith_div.find("div", {"class": ["mw-content-ltr", "mw-parser-output"]})
    uls = sixth_div.find_all("ul", {"class": ["gallery", "mw-gallery-traditional"]})

    hrefs = []

    for ul in uls:
        lis = ul.find_all("li")
        for li in lis:
            div = li.find("div", class_="gallerytext")
            if div:
                a = div.find("a")
                if a:
                    href = a.get('href')
                    hrefs.append(href)
    
    return hrefs

def get_flag_info(href):
    base_url = "https://en.wikipedia.org"
    response = requests.get(base_url + href)
    soup = BeautifulSoup(response.content, "html.parser")
    body = soup.find("body")
    first_div = body.find("div", class_="mw-page-container")
    second_div = first_div.find("div", class_="mw-page-container-inner")
    third_div = second_div.find("div", class_="mw-content-container")
    first_main = third_div.find("main", class_="mw-body")
    fourth_div = first_main.find("div", {"class": ["vector-body", "ve-init-mw-desktopArticleTarget-targetContainer"]})
    fith_div = fourth_div.find("div", class_="mw-body-content")
    sixth_div = fith_div.find("div", {"class": ["mw-parser-output", "mv-content-ltr"]})
    tables = sixth_div.find_all("table", class_="infobox")

    dicts = []
    td_image_prev = False

    for table in tables:
        if td_image_prev is True:
            td_image_prev = False
            dicts.append(dict)

        dict = {}
        caption = table.find("caption", class_="infobox-title")
        tbody = table.find("tbody")
        trs = tbody.find_all("tr")

        for tr in trs:
            td_name = tr.find("td", class_="infobox-subheader")
            
            if td_name is not None:
                b = td_name.find('b')
                if b is not None:
                    dict["name"] = b.text
            
            if td_name is None and caption is not None:
                dict["name"] = caption.text

            th = tr.find("th")
            if th is not None:
                td = tr.find("td")
                if td is not None:
    
                    text = td.text
                    
                    dict[th.text.lower()] = text.replace("\n", "").replace("\xa0", " ")

            td_image = tr.find("td", class_="infobox-image")

            if td_image is not None:
                span = td_image.find("span", class_="mw-image-border")
                if span:
                    a = span.find("a", class_="mw-file-description")
                    img = a.find("img")
                    srcset = img.get("srcset")
                    srcset_list = srcset.split(", ")
                    if td_image_prev is True:
                        dicts.append(dict)
                        dict = {}
                    dict["flag_url"] = srcset_list[-1].split(" ")[0]
                    td_image_prev = True
    
        if dict is not None:
            dicts.append(dict)

    return dicts

def main():
    list_of_flags = []
    flags_endpoints = get_flags_endpoints()
    for endpoint in flags_endpoints:
        flag_infos = get_flag_info(endpoint)
        for flag_info in flag_infos:
            list_of_flags.append(flag_info)
    
    # Escribir la lista de diccionarios en un archivo JSON
    with open('flags.json', 'w', encoding='utf-8') as f:
        json.dump(list_of_flags, f, ensure_ascii=False, indent=4)
    
    print("Archivo JSON generado correctamente: flags.json")

if __name__ == "__main__":
    main()