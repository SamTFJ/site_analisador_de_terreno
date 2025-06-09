import pandas as pd #Acessar arquivos .CSV
import requests # Ler arquivos
import fitz  # PyMuPDF (Ler arquivos)
import io # Ler arquivos
import decimal # Para cálculos mais precisos

# Arquivo dos dados de dicionários
from dictionaries import macrozonas, zonas, frentes_opostas, faixa_restriçao, lados

# Funções principais

def somaVetor(vetor):
    soma = decimal.Decimal(0)
    for elemento in vetor:
        soma += decimal.Decimal(elemento)

    return soma

def detlaterais(lados_recebidos, frentes_opostas, lados):
    lados1 = lados.copy()
    match len(lados_recebidos):
        case 1:
            oposto = frentes_opostas.get(lados_recebidos[0])
            lados1.remove(oposto)
            lados1.remove(lados_recebidos[0])
            return lados1, oposto
        case 2:
            lados1.remove(lados_recebidos[0])
            lados1.remove(lados_recebidos[1])
            return lados1, None
        case 3:
            lados1.remove(lados_recebidos[0])
            lados1.remove(lados_recebidos[1])
            lados1.remove(lados_recebidos[2])
            return lados1, None
        case _:
            return [], None

def analisa_terreno(codigo, largura, altura, area_input, macrozona, zoneamento, faixa, pe_esquerdo):
    bairro_encontrado = "Não encontrado"
    quadra = "Não encontrada"

    bairrosjp_db = pd.read_csv('bairros.csv', delimiter=',')

    #Transformando em lista para poder comparar
    bairros = bairrosjp_db['N_BAIRRO'].tolist()

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
                        quadra = int(loc[3:5])
                        lote = int(lote)     
                        break

    except requests.exceptions.RequestException as e:
        print("Esse dado não existe ou foi digitado incorretamente - Erro na requisição")

    valores = [decimal.Decimal(largura), decimal.Decimal(altura)]
    macro = macrozona
    valormz = macrozonas.get(macro, [0]) # valor padrão: [0], para não interferir com o decimal
    IDAP = decimal.Decimal(float(valormz[0])) # valor padrão [0]
    zona = zoneamento
    valorz = zonas.get(zona, [0])
    TO = decimal.Decimal(float(valorz[0]))

    if (area_input not in (None, "", 0)):
        area = decimal.Decimal(area_input)
        area_aproveitada = area*IDAP
        area_por_pav = area*(TO/100)
        pavimentos = (area*IDAP)/((TO/100)*area)
        if (faixa not in (None, "", 0)):
            valorAlt = decimal.Decimal(faixa_restriçao.get(faixa, [decimal.Decimal(0)])[0])
            pavimentos = int(valorAlt / decimal.Decimal(pe_esquerdo))
        taxa_de_ocupaçao = (area_por_pav / area)

    else:
        area = decimal.Decimal(valores[0] * valores[1])
        area_aproveitada = area*IDAP
        area_por_pav = area*(TO/100)
        pavimentos = (area*IDAP)/((TO/100)*area)
        if (faixa not in (None, "", 0)):
            valorAlt = decimal.Decimal(faixa_restriçao.get(faixa, [decimal.Decimal(0)])[0])
            pavimentos = int(valorAlt / decimal.Decimal(pe_esquerdo))
        taxa_de_ocupaçao = (area_por_pav / area)

    area_com_escadarias = (area_por_pav*decimal.Decimal(0.7)).quantize(decimal.Decimal('0.001'))
    porcent_area = ((area_com_escadarias/area_por_pav)*100)

    return{
        "bairro": bairro_encontrado,
        "quadra": quadra,
        "lote": lote,
        "area_total": str(area),
        "area_aproveitada": str(area_aproveitada),
        "area_por_pavimento": str(area_por_pav),
        "area_com_escadarias": str(area_com_escadarias),
        "porcent_area": str(porcent_area),
        "num_de_pavimentos": str(pavimentos),
        "taxa_de_ocupaçao": str(taxa_de_ocupaçao*100),
        "link_do_overlay": url
    }

def calcRecuoPavimentos(zona, lados_recebidos, testada_real, profundidade, pavimentos):
    area_pavs = []
    num_frentes = len(lados_recebidos)

    #Descobre as laterais e o fundo
    laterais, fundo = detlaterais(lados_recebidos, frentes_opostas, lados)

    # Realizar o cálculo da área de cada pavimento
    for i in range(pavimentos):
        testada_real_for = testada_real
        profundidade_for = profundidade

        if fundo != None:
            if i <= 3:
                if fundo%2 == 0:
                    testada_real_for = testada_real_for - zonas.get(zona)[i+8]
                else:
                    profundidade_for = profundidade_for - zonas.get(zona)[i+8]

            else:
                if fundo%2 == 0:
                    testada_real_for = testada_real_for - eval(zonas.get(zona)[12], {}, {"N": i})
                else:
                    profundidade_for = profundidade_for - eval(zonas.get(zona)[12], {}, {"N": i})

        # Faz os cálculos dos recuos laterais
        for k in range(len(laterais)):
            if i <= 3:
                if laterais[k]%2 == 0:
                    testada_real_for = testada_real_for - zonas.get(zona)[i+3]
                else:
                    profundidade_for = profundidade_for - zonas.get(zona)[i+3]

            else:
                if laterais[k]%2 == 0:
                    testada_real_for = testada_real_for - eval(zonas.get(zona)[7], {}, {"N": i})
                else:
                    profundidade_for = profundidade_for - eval(zonas.get(zona)[7], {}, {"N": i})

        # Faz o cálculos de cada pavimento de acordo com o número de frentes
        for j in range(num_frentes):
            # Verifica se o lado é par ou ímpar
            if lados_recebidos[j]%2 == 0:
                # Subtraindo as frentes
                testada_real_for = testada_real_for - zonas.get(zona)[2]

            else:
                profundidade_for = profundidade_for - zonas.get(zona)[2]

        ResArea = testada_real_for * profundidade_for
        ResArea = round (ResArea, 3)
        area_pavs.append(ResArea)
    
    return area_pavs

