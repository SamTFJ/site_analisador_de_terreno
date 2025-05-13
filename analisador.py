# Working with CSV archives
import pandas as pd
import numpy as np

# To visualize the graphics
import seaborn as sns
import matplotlib.pyplot as plt

from re import M
import requests
import fitz  # PyMuPDF
import io
import decimal


def analisa_terreno(codigo, largura, altura, area_input, macrozona, zoneamento):
    bairrosjp_db = pd.read_csv('bairros.csv', delimiter=',')

    #Transformando em lista para poder comparar
    bairros = bairrosjp_db['N_BAIRRO'].tolist()

    #Criando dicionários com as macrozonas e zonas, para associar valores
    macrozonas = {
        #Macrozonas / IDAPMAX  / IDAPMIN
        "ma1": [6,1],
        "ma2": [4,1],
        "ma3": [2,1],
        "mbd": [0.5],
        "mpa": [1]
    }

    zonas = {
        #Zonas  /  TO máxima  / TAP mínima
        "zh1": [50,10],
        "zh2": [55,5],
        "zh3": [50,5],
        "zh4": [50,15],
        "zh5": [50,15],
        "zcs1": [80,5],
        "zcs2": [70,5],
        "zcs3": [65,5],
        "zcs4": [65,5],
        "zcs5": [50,25],
        "zcs6": [30,30],
        "zcs7": [65,10],
        "zepa2": [40,40],
        "zepa3": [40, 40],
        "zi1": [50,10],
        "zi2": [50,10],
        "zbd": [10,80],
        "seav": [40,15],
    }


    loc = codigo
    lote = int(loc[5:])
    loc = loc[:2]+"_"+str(int(loc[2:5]))

    # URL do PDF
    url = 'https://filipeia.joaopessoa.pb.gov.br/overlay/' + loc + '.pdf'

    try:
        # Realiza a requisição HTTP para obter o conteúdo do PDF
        response = requests.get(url)
        response.raise_for_status()  # Verifica se a requisição foi bem-sucedida


        # Lê o conteúdo do PDF diretamente da memória
        with io.BytesIO(response.content) as pdf_file:

            doc = fitz.open(stream=pdf_file, filetype="pdf")
            for page_num, page in enumerate(doc, start=1):
                text = page.get_text()
                for bairro in bairros:
                    if bairro in text:
                        bairro_encontrado = bairro
                        quadra = int(loc[3:6])
                        lote = int(lote)     
                        break

    except requests.exceptions.RequestException as e:
        print("Esse dado não existe ou foi digitado incorretamente - Erro na requisição")

    valores = [decimal.Decimal(largura), decimal.Decimal(altura)]
    macro = macrozona
    IDAP = decimal.Decimal(float(((macrozonas.get(macro))[0])))
    zona = zoneamento
    TO = decimal.Decimal(float(((zonas.get(zona))[0])))

    if (area_input not in (None, "", 0)):
        area = decimal.Decimal(area_input)
        area_aproveitada = area*IDAP
        area_por_pav = area*(TO/100)
        pavimentos = (area*IDAP)/((TO/100)*area)

    else:
        area = decimal.Decimal(valores[0] * valores[1])
        area_aproveitada = area*IDAP
        area_por_pav = area*(TO/100)
        pavimentos = (area*IDAP)/((TO/100)*area)

    return{
        "bairro": bairro_encontrado,
        "quadra": quadra,
        "lote": lote,
        "area_total": str(area),
        "area_aproveitada": str(area_aproveitada),
        "area_por_pavimento": str(area_por_pav),
        "num_de_pavimentos": str(pavimentos),
        "link_do_overlay": url
    }
