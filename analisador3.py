import decimal


def somaVetor(vetor):
    soma = decimal.Decimal(0)
    for elemento in vetor:
        soma += decimal.Decimal(elemento)

    return soma

faixa_restriçao = {
        #Faixa / altura
        1: 12.9,
        2: 16.5,
        3: 19.5,
        4: 22.5,
        5: 25.5,
        6: 28.5,
        7: 31.5,
        8: 34,
        9: 35,
    }