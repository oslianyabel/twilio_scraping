import openpyxl
from openpyxl.styles import Font
from bs4 import BeautifulSoup
import requests, os

wb = openpyxl.Workbook()
ws = wb.active
ws['A1'] = 'Nombre'
ws['B1'] = 'Descripción'
ws['C1'] = 'Imagen'
ws['D1'] = 'SKU'
font_azul = Font(color='0000FF') 

url = "https://nueva.eciglogistica.com/novedades"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3",
}

def scrape_page():
    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        soup = BeautifulSoup(response.content, 'html.parser')
        productos = soup.find_all("div", class_="product card-product box")
        print(len(productos))
        productos_info = []
        base_dir = os.path.dirname(os.path.abspath(__file__))
        static_dir = os.path.join(base_dir, 'static')

        counter = 2
        for producto in productos:
            nombre = producto.find("h5").text.strip()
            descripcion = producto.find("div", class_="product-body").text.strip()
            imagen = producto.find("img", class_="img-fluid")["src"]
            sku = producto.find("a", class_="product-header")["href"]
            
            ws.cell(row=counter, column=1).value = nombre
            ws.cell(row=counter, column=2).value = descripcion
            ws.cell(row=counter, column=3).value = imagen
            ws.cell(row=counter, column=3).hyperlink = imagen
            ws.cell(row=counter, column=3).font = font_azul
            ws.cell(row=counter, column=4).value = sku
            ws.cell(row=counter, column=4).hyperlink = sku
            ws.cell(row=counter, column=4).font = font_azul
            
            p_info = {"nombre": nombre, "descripcion": descripcion, "imagen": imagen, "sku": sku}
            productos_info.append(p_info)

            counter+=1

        wb.save(os.path.join(static_dir, 'productos.xlsx'))
        print("Datos guardados en productos.xlsx")
        return productos_info
    else:
        print("Error al realizar la solicitud")
        return False
