from flask import Flask, request, jsonify
from flask_cors import CORS
import pandas as pd
from pathlib import Path
import numpy as np

app = Flask(__name__)
CORS(app)  # Permitir requisições de qualquer origem

# Carregar o CSV
csv_path = Path(__file__).parent.parent / "data" / "Relatorio_cadop.csv"
print(f"Carregando CSV de: {csv_path}")
df = pd.read_csv(csv_path, sep=';', encoding='utf-8')
print(f"CSV carregado com {len(df)} linhas")

# Renomear as colunas para garantir consistência
df = df.rename(columns={
    'Registro_ANS': 'Registro_ANS',
    'Nome_Fantasia': 'Nome_Fantasia',
    'Razao_Social': 'Razao_Social',
    'Cidade': 'Cidade',
    'UF': 'UF'
})

# Substituir NaN por None (que será serializado como null em JSON)
df = df.replace({np.nan: None})
print("Valores NaN substituídos por None")

# Função para realizar a busca textual
def search_operadoras(query):
    if not query:
        print("Query vazia, retornando todos os registros")
        return df.to_dict(orient='records')

    # Converter a query para minúsculas para busca case-insensitive
    query = query.lower()
    print(f"Buscando por: {query}")

    # Criar uma coluna de pontuação para relevância
    df['score'] = 0

    # Campos para busca: Nome_Fantasia, Razao_Social, Cidade, UF
    for column in ['Nome_Fantasia', 'Razao_Social', 'Cidade', 'UF']:
        # Verificar se o termo está presente em cada campo (case-insensitive)
        print(f"Valores de exemplo na coluna {column}:", df[column].head().tolist())
        mask = df[column].astype(str).str.lower().str.contains(query, na=False)
        df.loc[mask, 'score'] += 1
        print(f"Coluna {column}: {sum(mask)} registros encontrados")

    # Ordenar por pontuação (maior relevância primeiro) e remover a coluna score
    result = df[df['score'] > 0].sort_values(by='score', ascending=False).drop(columns=['score'])
    print(f"Total de resultados encontrados: {len(result)}")
    if len(result) > 0:
        print("Primeiros resultados:", result.head().to_dict(orient='records'))
    return result.to_dict(orient='records')

# Rota para busca
@app.route('/api/search', methods=['GET'])
def search():
    query = request.args.get('query', '')
    results = search_operadoras(query)
    response = jsonify(results)
    response.headers['Content-Type'] = 'application/json'
    return response

# Rota inicial para verificar se o servidor está funcionando
@app.route('/')
def home():
    return "Servidor de busca de operadoras está funcionando!"

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)