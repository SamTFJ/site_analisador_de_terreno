from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException

import decimal

zonas = {
        #Zonas  /  TO máxima  / TAP mínima  / recuo Frontal  / recuo lateral  /  Recuo Fundo
        "Zona Habitacional 1": [50,10],
        "Zona Habitacional 2": [55,5],
        "Zona Habitacional 3": [50,5],
        "Zona Habitacional 4": [50,15],
        "Zona Habitacional 5": [50,15],
        "Zona de Comércio e Serviço 1": [80,5],
        "Zona de Comércio e Serviço 2": [70,5],
        "Zona de Comércio e Serviço 3": [65,5],
        "Zona de Comércio e Serviço 4": [65,5],
        "Zona de Comércio e Serviço 5": [50,25],
        "Zona de Comércio e Serviço 6": [30,30],
        "Zona de Comércio e Serviço 7": [65,10],
        "Zona Espcial de Proteção Ambiental 2": [40,40],
        "Zona Espcial de Proteção Ambiental 3": [40, 40],
        "Zona Industrial 1": [50,10],
        "Zona Industrial 2": [50,10],
        "Zona de Baixa Densidade": [10,80],
        "Setor Espcial de Áreas Verdes": [40,15],
    }

macrozonas = {
        #Macrozonas / IDAPMAX  / IDAPMIN
        "Macrozona Adensável 1": [6,1],
        "Macrozona Adensável 2": [4,1],
        "Macrozona Adensável 3": [2,1],
        "Macrozona de Baixa Densidade": [0.5],
        "Macrozona de Proteção Ambiental": [1]
    }

def extrair_dados(codigo):

    # modo headless, em segundo plano
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    #navegador = webdriver.Chrome(options=chrome_options)

    # abrir navegador
    navegador = webdriver.Chrome(options=chrome_options)

    navegador.get("https://www.joaopessoa.pb.gov.br/pc/fichaCadastralImovel.xhtml")

    # Colocar em tela cheia
    navegador.maximize_window()

    # selecionar um elemento na tela
    loc_cart = navegador.find_element('xpath', "/html/body/div[1]/div/form/div[1]/div[2]/div/table/tbody/tr[2]/td[2]/label")
    loc_cart.click()

    # Preencher loc
    loc_cart_input = navegador.find_element('xpath', "/html/body/div[1]/div/form/div[1]/div[2]/div/table/tbody/tr[2]/td[3]/input")
    loc_cart_input.click()
    loc_cart_input.send_keys(str(codigo) +"00000000")

    # Apertar consultar
    botao_consultar = navegador.find_element('xpath', "/html/body/div[1]/div/form/div[1]/div[2]/button/span[2]")
    botao_consultar.click()

    def extract_data(driver, locator_type, locator, attribute=None, timeout=10):
        try:
            element = WebDriverWait(driver, timeout).until(
                EC.presence_of_element_located((locator_type, locator))
            )

            if attribute:
                return element.get_attribute(attribute)
            else:
                return element.text

        except TimeoutException:
            print(f"Element with {locator_type}={locator} not found after {timeout} seconds.")
            return None
        except NoSuchElementException:
            print(f"Element with {locator_type}={locator} was not found.")
            return None
        except Exception as e:
            print(f"An error occurred while extracting data: {e}")
            return None
        
    bairro = extract_data(navegador, By.XPATH, "/html/body/div[1]/div/form/div[1]/div[2]/div/div/div[1]/table/tbody/tr[9]/td[2]")

    lote_button = navegador.find_element('xpath', "/html/body/div[1]/div/form/div[1]/div[2]/div/ul/li[2]/a")
    lote_button.click()

    areatotal = extract_data(navegador, By.XPATH, "/html/body/div[1]/div/form/div[1]/div[2]/div/div/div[2]/table/tbody/tr[16]/td[2]")

    edificacao_button = navegador.find_element('xpath', "/html/body/div[1]/div/form/div[1]/div[2]/div/ul/li[3]/a")
    edificacao_button.click()

    macrozona = extract_data(navegador, By.XPATH, "/html/body/div[1]/div/form/div[1]/div[2]/div/div/div[3]/table/tbody/tr[26]/td[2]")
    zona = extract_data(navegador, By.XPATH, "/html/body/div[1]/div/form/div[1]/div[2]/div/div/div[3]/table/tbody/tr[27]/td[2]")

    navegador.quit()

    valormz = macrozonas.get(macrozona, [0]) # valor padrão: [0], para não interferir com o decimal
    IDAP = decimal.Decimal(float(valormz[0])) # valor padrão [0]
    valorz = zonas.get(zona, [0])
    TO = decimal.Decimal(float(valorz[0]))

    area = decimal.Decimal(areatotal.replace(",","."))
    area_aproveitada = area*IDAP
    area_por_pav = area*(TO/100)
    pavimentos = (area*IDAP)/((TO/100)*area)
    taxa_de_ocupaçao = (area_por_pav / area)

    loc = codigo
    loc = loc[:2]+"_"+str(int(loc[2:5]))

    # URL do PDF
    url = 'https://filipeia.joaopessoa.pb.gov.br/overlay/' + loc + '.pdf'

    return{
        "bairro" :  bairro[6:],
        "quadra": int(codigo[3:5]),
        "lote": int(codigo[6:]),
        "area_total": areatotal,
        "macrozona": macrozona,
        "zona": zona,
        "area_aproveitada": str(area_aproveitada),
        "area_por_pavimento": str(area_por_pav),
        "area_com_escadarias": str((area_por_pav*decimal.Decimal(0.7)).quantize(decimal.Decimal('0.001'))),
        "num_de_pavimentos": str(pavimentos),
        "taxa_de_ocupaçao": str(taxa_de_ocupaçao*100),
        "link_do_overlay": url
    }