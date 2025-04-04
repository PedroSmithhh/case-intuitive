import pandas as pd
from pathlib import Path
from charset_normalizer import detect

# Função para detectar o encoding de um arquivo
def get_file_encoding(file_path):
    try:
        with open(file_path, 'rb') as f:
            raw_data = f.read(10000)
            result = detect(raw_data)
            encoding = result['encoding']
            if encoding is None:
                print(f"Não foi possível detectar o encoding de {file_path.name}. Usando latin-1 como fallback.")
                return 'latin-1'  # Fallback para latin-1 se a detecção falhar
            return encoding
    except Exception as e:
        print(f"Erro ao detectar o encoding de {file_path.name}: {e}. Usando latin-1 como fallback.")
        return 'latin-1'

# Função para converter o encoding
def convert_to_utf8(file_path):
    # Detectando o encoding do arquivo
    encoding = get_file_encoding(file_path)
    print(f"Arquivo {file_path.name}: Encoding detectado = {encoding}")

    try:
        # Lendo o arquivo com o encoding detectado
        df = pd.read_csv(file_path, encoding=encoding, sep=';')

        # Ajustando o formato das colunas decimais (substituindo vírgula por ponto para importação SQL)
        if 'VL_SALDO_INICIAL' in df.columns and 'VL_SALDO_FINAL' in df.columns:
            print(f"Ajustando formato decimal em {file_path.name}...")
            # Substituir vírgulas por pontos e converter para float
            df['VL_SALDO_INICIAL'] = df['VL_SALDO_INICIAL'].astype(str).str.replace(',', '.').astype(float)
            df['VL_SALDO_FINAL'] = df['VL_SALDO_FINAL'].astype(str).str.replace(',', '.').astype(float)

         # Salvando o arquivo em UTF-8
        df.to_csv(file_path, encoding='utf-8-sig', index=False, sep=';')
        print(f"Arquivo {file_path.name} processado com sucesso.")
    except Exception as e:
            print(f"Erro ao processar {file_path.name}: {e}")

# Diretórios
root_path = Path.cwd()
demonstrações_2023_path = root_path / "questao_tres" / "data" / "demonstracoes_contabeis" / "2023"
demonstrações_2024_path = root_path / "questao_tres" / "data" / "demonstracoes_contabeis" / "2024"
operadoras_path = root_path / "questao_tres" / "data" / "operadoras_de_plano_de_saude_ativas" / 'Relatorio_cadop.csv'

# Lista de arquivos a processar de demonstrações financeiras em 2023
csv_files_d_2023 = [
    "1T2023.csv",
    "2t2023.csv",
    "3T2023.csv",
    "4T2023.csv",
]

# Processar cada arquivo de 2023
for csv_file in csv_files_d_2023:
    path = demonstrações_2023_path / csv_file
    convert_to_utf8(path)

# Lista de arquivos a processar de demonstrações financeiras em 2024
csv_files_d_2024 = [
    "1T2024.csv",
    "2T2024.csv",
    "3T2024.csv",
    "4T2024.csv",
]

# Processar cada arquivo de 2024
for csv_file in csv_files_d_2024:
    path = demonstrações_2024_path / csv_file
    convert_to_utf8(path)

# Processar CSV de operadoras
convert_to_utf8(operadoras_path)

print('Processamento concluído.')