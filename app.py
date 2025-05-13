from flask import Flask, render_template, request
from analisador import analisa_terreno

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
            macrozona      = form["macro"],
            zoneamento       = form["zona"]
        )
    return render_template("index.html", resultado=resultado)

if __name__ == '__main__':
    app.run(debug=True, port=5500)