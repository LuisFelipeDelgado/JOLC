from flask import Flask, redirect, url_for, render_template, request
from TS.TCI import TCI
from grammar import parse
import base64
import graphviz

app = Flask(__name__)

tmp_val=''
result = None

@app.route("/")# de esta forma le indicamos la ruta para acceder a esta pagina. 'Decoramos' la funcion. 
def home():
    return render_template('index.html')

@app.route("/analyze", methods=["POST","GET"])
def analyze():
    if request.method == "POST":
        inpt = request.form["inpt"]
        global tmp_val
        tmp_val=inpt
        codigoAux = TCI()
        codigoAux.cleanAll()
        codigoR = codigoAux.getInstance()
        global result
        result = parse(tmp_val)
        return render_template('analyze.html',initial=inpt, input=codigoR.getCode())
    else:
        return render_template('analyze.html')

@app.route('/output')
def output():
    global tmp_val
    global result
    return render_template('output.html', input=result.getConsola())

@app.route("/reports")
def reports():
    return render_template('reports.html')

@app.route('/reports/simbols')
def simbols():
    dot = result.tablaS()
    dig = graphviz.Source(dot)
    chart_output = dig.pipe(format='svg')
    chart_output = base64.b64encode(chart_output).decode('utf-8')
    return render_template('reports.html', chart2=chart_output)

if __name__ == "__main__":
    app.run(debug=True)#para que se actualice al detectar cambios
