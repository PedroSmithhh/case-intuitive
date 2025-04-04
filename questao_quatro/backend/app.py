from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from pathlib import Path

app = Flask(__name__)
CORS(app)  # Permitir requisições de qualquer origem

# Carregar o CSV
csv_path = Path(__file__).parent.parent / "data" / "Relatorio_cadop.csv"
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')

# Função para realizar a busca textual
def search_operadoras(query):
    if not query:
        return df.to_dict(orient='records')  # Retorna todos os registros se a query estiver vazia

    # Converter a query para minúsculas para busca case-insensitive
    query = query.lower()

    # Criar uma coluna de pontuação para relevância
    df['score'] = 0

    # Campos para busca: Nome_Fantasia, Razao_Social, Cidade, UF
    for column in ['Nome_Fantasia', 'Razao_Social', 'Cidade', 'UF']:
        # Verificar se o termo está presente em cada campo (case-insensitive)
        mask = df[column].astype(str).str.lower().str.contains(query, na=False)
        df.loc[mask, 'score'] += 1

    # Ordenar por pontuação (maior relevância primeiro) e remover a coluna score
    result = df[df['score'] > 0].sort_values(by='score', ascending=False).drop(columns=['score'])
    return result.to_dict(orient='records')

# Rota para busca
@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = search_operadoras(query)
    return jsonify(results)

# Rota inicial para verificar se o servidor está funcionando
@app.route('/')
def home():
    return "Servidor de busca de operadoras está funcionando!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)