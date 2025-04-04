import pdfplumber
import pandas as pd
import zipfile
from pathlib import Path
import os

# Caminhos
root_path = Path.cwd()
zip_name = root_path / "questao_dois" / "data" / "zip" / "Teste_PEDROSMITH.zip"
pdf_path = r'questao_um\data\pdf\Anexo_1.pdf'

# Lista para armazenar todas as linhas das tabelas
all_tables = []
header = None  # Para armazenar o cabeçalho

# Abrindo o PDF e extraindo tabelas de todas as páginas
with pdfplumber.open(pdf_path) as pdf:
    for page in pdf.pages:
        table = page.extract_table()  # Extraindo a tabela da página
        if table:
            # Se ainda não temos o cabeçalho, pegamos a primeira linha da primeira tabela
            if header is None:
                header = table[0]  # Primeira linha é o cabeçalho
                all_tables.extend(table[1:])  # Adiciona as linhas de dados
            else:
                # Para as próximas páginas, verificamos se a primeira linha é o cabeçalho
                if table[0] != header:  # Se a primeira linha não for o cabeçalho, adicionamos
                    all_tables.extend(table)
                else:
                    all_tables.extend(table[1:])  # Ignora o cabeçalho e adiciona os dados

# Filtrando linhas vazias e limpando os dados
cleaned_tables = []
for row in all_tables:
    # Remove linhas onde todas as células são None ou vazias
    if row and any(cell is not None and str(cell).strip() != '' for cell in row):
        # Limpa quebras de linha e espaços extras em cada célula
        cleaned_row = [str(cell).replace('\n', ' ').strip() if cell is not None else '' for cell in row]
        cleaned_tables.append(cleaned_row)

# Usar as linhas limpas
all_tables = cleaned_tables

# Criando um DataFrame com os dados extraídos
columns = ['PROCEDIMENTO', 'RN (alteração)', 'VIGÊNCIA', 'OD', 'AMB', 'HCO', 'HSO', 'REF', 'PAC', 'DUT', 'SUBGRUPO', 'GRUPO', 'CAPÍTULO']
df = pd.DataFrame(all_tables, columns=columns)

# Substituindo as abreviações pelas descrições completas
df.rename(columns={'OD': 'Seg. Odontológica', 'AMB': 'Seg. Ambulatorial'}, inplace=True)

# Salvando os dados em um arquivo CSV
csv_path = r'questao_dois\data\anexo_1.csv'
df.to_csv(csv_path, index=False, encoding='utf-8-sig', sep=';')  # index=False evita adicionar uma coluna de índices

# Compactando o CSV em um arquivo ZIP
with zipfile.ZipFile(zip_name, 'w') as zipf:
    zipf.write(csv_path, arcname=os.path.basename(csv_path))  # Adicionando o CSV ao ZIP

print(f"Arquivo compactado em: {zip_name}")