from flask import Flask, render_template, request, jsonify
from analisador import analisa_terreno, somaVetor, calcRecuoPavimentos, detlaterais
import decimal

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])

def home():
    resultado = None

    if request.method == "POST":
        form = request.form
        resultado = analisa_terreno(
            codigo     = form["codigo"],
            largura    = form.get("largura", 0) or 0,
            altura     = form.get("altura", 0) or 0,
            area_input = form.get("area") or None,
            macrozona  = form["macro"],
            zoneamento = form["zona"],
            faixa      = form["faixa"] or None,
            pe_esquerdo= form["pe_esquerdo"] or 2.8
        )      

    return render_template("index.html", resultado = resultado)

@app.route('/atualizar', methods=['POST', 'GET'])

def rota_atualizar():
    data = request.get_json(force = True)
    valores = data.get('valores', [])

    somaTotalPav = somaVetor(valores)
    return jsonify({'somaTotalPav': str(somaTotalPav)})

@app.route('/atualizar_escadarias', methods=['POST'])
def atualizar_escadarias():
    data = request.get_json()
    nova_area = float(data.get('nova_area_com_escadarias'))  # Recebe o valor como float
    # Faça algo com nova_area (por exemplo, salvar no banco de dados)
    return jsonify({'message': 'Valor atualizado com sucesso!'})

@app.route('/api/lados', methods=['POST'])
def receber_lados():
    # Verifica se a requisição contém dados JSON
    if not request.is_json:
        # Retorna um erro se o Content-Type não for application/json
        return jsonify({"erro": "Content-Type deve ser application/json"}), 400

    # Obtém os dados JSON da requisição
    data = request.get_json()

    # Extrai o array de 'lados' do JSON.
    # Usa .get() para evitar KeyError se 'lados' não estiver presente.
    lados_recebidos = data.get('lados', [])

    resultado1 = analisa_terreno(
            codigo     = data["codigo"],
            largura    = data.get("largura", 0) or 0,
            altura     = data.get("altura", 0) or 0,
            area_input = data.get("area") or None,
            macrozona  = data["macro"],
            zoneamento = data["zona"],
            faixa      = data["faixa"] or None,
            pe_esquerdo= data["pe_esquerdo"] or 2.8
        )

    recuo_pavs = None

    if (decimal.Decimal(data.get("largura", 0)) != 0 and decimal.Decimal(data.get("altura", 0)) != 0):
        recuo_pavs = calcRecuoPavimentos(
            zona = data["zona"],
            lados_recebidos = lados_recebidos,
            testada_real    = data.get("largura", 0) or 0,
            profundidade    = data.get("altura", 0) or 0,
            pavimentos      = resultado1.num_pavimentos
        )

    return jsonify({
        "mensagem": "Dados dos lados recebidos com sucesso!",
        "ladosRecebidos": lados_recebidos, # Retorna os lados recebidos de volta
        "recuopavs": recuo_pavs
    })

if __name__ == '__main__':
    app.run(debug=True, port=5500)