#Dados dos dicionários que serão usados nos outros arquivos
import decimal

macrozonas = {
    #Macrozonas / IDAPMAX  / IDAPMIN
    "ma1": [6,1],
    "ma2": [4,1],
    "ma3": [2,1],
    "mbd": [0.5],
    "mpa": [1]
}

zonas = {
    #Zonas  /  TO máxima  / recuo Frontal por frente / recuo lateral (Primeiro pav), (segundo pav), (terceiro pav), (quarto pav) / fórmula do recuo lateral /  Recuo Fundo (primeiro pav), (segundo pav), (terceiro pav), (quarto pav) / Fórmula do recuo dos fundos
    "zh1": [50,10,5,1.5,1.5,1.5,3,"(3+((N-4)*0.3))",3,3,3,3,"(3+((N-4)*0.30))"],
    "zh2": [55,5,5,1.5,1.5,1.5,3,"(3+((N-4)*0.30))",2,2,3,4,"(3,00+((N-4)*0.30))"],
    "zh3": [50,5,5,1.5,1.5,1.,5,3,"(3+((N-4)*0.30))", 3, 3, 3, 3,"(3+((N-4)*0.30))"],
    "zh4": [50,15,5,2,2,2,4,"(4+((N-4)*0.30))",3,3,3,3,"(4+((N-4)*0.30))"],
    "zh5": [50,15,5,1.5,1.5,3,3,"(3+((N-4)*0.30))",3,3,3,3,"(3+((N-4)*0.30))"],
    "zcs1": [80,5,0,0,0,0,0,"0",2,2,2,2,"2"],
    "zcs2": [70,5,0,0,0,2,2,"(3+((N-4)*0.30))",3,3,3,3,"(3+((N-4)*0.30))"],
    "zcs3": [65,5,5,0,0,2,2,"(3+((N-4)*0.30))",3,3,3,3,"(3+((N-4)*0.30))"],
    "zcs4": [65,5,5,0,0,2,2,"(3+((N-4)*0.30))",2,2,3,3,"(3+((N-4)*0.30))"],
    "zcs5": [50,25,10,5,5,5,5,"(5)",5,5,5,5,"(5)"],
    "zcs6": [30,30,10,8,8,8,8,"(8)",8,8,8,8,"(8)"],
    "zcs7": [65,10,8,4,4,4,4,"(4)",4,4,4,4,"(4)"],
    "zepa2": [40,40,10,1.5,1.5,1.5,3,"( 3+((N-4)*0.30))"],
    "zepa3": [40, 40,10,1.5,1.5,3,3,"(3)",3,3,3,3,"(3)"],
    "zi1": [50,10,6,3,3,3,3,"(3)",3,3,3,3,"(3)"],
    "zi2": [50,10,6,3,3,3,3,"(3)",3,3,3,3,"(3)"],
    "zbd": [10,80,10,10,10,0,0,"(0)",10,10,0,0,"(0)"],
    "seav": [40,15,5,1.5,1.5,1.5,3,"(3+((N-4)*0.30))",2,2,3,3,"(3+((N-4)*0.30))"],
}

frentes = {
    #Número de frentes / Quantidade
    "UMA" : [1],
    "DUAS" : [2],
    "TRÊS" : [3],
    "QUATRO" : [4]
}

frentes_opostas = {
    1:3,
    2:4,
    3:1,
    4:2
}

lados = [1,2,3,4]

faixa_restriçao = {
    #Faixa / altura
    '1': [decimal.Decimal(12.9)],
    '2': [decimal.Decimal(16.5)],
    '3': [decimal.Decimal(19.5)],
    '4': [decimal.Decimal(22.5)],
    '5': [decimal.Decimal(25.5)],
    '6': [decimal.Decimal(28.5)],
    '7': [decimal.Decimal(31.5)],
    '8': [decimal.Decimal(34)],
    '9': [decimal.Decimal(35)],
}