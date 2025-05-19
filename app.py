from flask import Flask, render_template, request, jsonify
from analisador import analisa_terreno
from analisador2 import extrair_dados
from analisador3 import somaVetor

app = Flask(__name__)

@app.route("/", methods = ['POST', 'GET'])

def home():
    resultado = None

    if request.method == "POST":
        form = request.form
        if (int(form["codigo"][5:]) != 0):
            resultado = extrair_dados(
                codigo = form["codigo"]
            )

        else:
            resultado = analisa_terreno(
                codigo     = form["codigo"],
                largura    = form.get("largura", 0) or 0,
                altura     = form.get("altura", 0) or 0,
                area_input = form.get("area") or None,
                macrozona      = form["macro"],
                zoneamento       = form["zona"]
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

if __name__ == '__main__':
    app.run(debug=True, port=5500)