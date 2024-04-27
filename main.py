from flask import Flask, jsonify, render_template
import fundamentus
import pandas as pd
import os

app = Flask(__name__, template_folder='static')

@app.route('/ativos', methods=['GET'])
def obter_informacoes_ativo():
    try:
        df = fundamentus.get_resultado()
        print('tamanho inicial ' + str(df.shape[0]))
        plmin = df.pl > 3  
        plmax = df.pl < 10
        pvpmin = df.pvp > 0.5
        pvpmax = df.pvp < 2
        divYieldmin = (df.dy * 100) > 7
        divYieldmax = (df.dy * 100) < 15
        roemin = (df.roe * 100) > 15
        roemax = (df.roe * 100) < 30
        liq2mounth = df.liq2m > 1000000
        cresc5years = df.c5y * 100 > 10
        arFilters = [plmin, plmax, pvpmin, pvpmax, divYieldmin, divYieldmax, roemin, roemax, liq2mounth, cresc5years]
        filtered_dfs = []
        for filter in arFilters:
            df = df[filter]
            print('tamanho ' + str(df.shape[0]))
        df.to_csv('arquivo.csv')
        ativos = df.to_dict()
        return render_template('ativos.html', ativos=ativos)
    except Exception as e:
        return jsonify({'erro': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
