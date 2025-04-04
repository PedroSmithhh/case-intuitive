import requests
from bs4 import BeautifulSoup
import zipfile
import os
from pathlib import Path

# URL do site
url = "https://www.gov.br/ans/pt-br/acesso-a-informacao/participacao-da-sociedade/atualizacao-do-rol-de-procedimentos"

# Especificar o caminho para salvar os arquivos
root_path = Path.cwd()
pdf_path_1 = root_path / "questao_um" / "data" / "pdf" / "Anexo_1.pdf"
pdf_path_2 = root_path / "questao_um" / "data" / "pdf" / "Anexo_2.pdf"
zip_path = root_path / "questao_um" / "data" / "zip" / "anexos.zip"

# Fazendo a requisição ao site e pegando o conteúdo da página
response = requests.get(url)
soup = BeautifulSoup(response.content, 'html.parser')  # Analisando o HTML

pdf_links = []

# Buscamos tags <a> com a classe "internal-link" e que contenham "Anexo I" ou "Anexo II" no texto ou no atributo data-tippy (verificado no DevTools)
for busca in soup.find_all('a', class_='internal-link', href=True):
    # Pegando o texto do link e o valor do atributo data-tippy
    link_pdf = busca.get_text(strip=True)  # Texto dentro da tag <a>
    data_tippy = busca.get('data-tippy', '')  # Valor do atributo data-tippy, ou vazio se não existir
    
    # Verificando se "Anexo I" ou "Anexo II" está no texto ou no data-tippy
    if ('Anexo I' in link_pdf or 'Anexo I' in data_tippy) and busca['href'].endswith('.pdf'):
        pdf_links.append({'href': busca['href'], 'anexo': 'Anexo I'})
    if ('Anexo II' in link_pdf or 'Anexo II' in data_tippy) and busca['href'].endswith('.pdf'):
        pdf_links.append({'href': busca['href'], 'anexo': 'Anexo II'})

# Removendo duplicatas com base no href
pdf_links = list({link['href']: link for link in pdf_links}.values())

# Verificando se encontramos os links
if not pdf_links:
    print("Nenhum link para Anexo I ou Anexo II encontrado.")
    exit()

# Lista para armazenar os nomes dos arquivos baixados
arquivos_baixados = []

# Baixando os PDFs
for link_info in pdf_links:
    link = link_info['href']
    anexo = link_info['anexo']
    
    # Se o link for relativo (ex.: "/arquivo.pdf"), convertemos para absoluto
    if not link.startswith('http'):
        link = 'https://www.gov.br' + link
    print(f"Baixando: {link}")
    
    # Fazendo o download do PDF
    pdf_response = requests.get(link)
    
    # Escolhendo o caminho de destino com base no anexo
    if anexo == 'Anexo I':
        pdf_path = pdf_path_1  # Anexo I
    elif anexo == 'Anexo II':
        pdf_path = pdf_path_2  # Anexo II
    else:
        continue  # Ignora links que não são Anexo I ou Anexo II
    
    # Salvando o PDF
    with open(pdf_path, 'wb') as f:  # wb - Escrita binária
        f.write(pdf_response.content)
    arquivos_baixados.append(pdf_path)  # Adicionando o caminho completo à lista

# Remove duplicatas da lista, caso haja
arquivos_baixados = list(set(arquivos_baixados))

# Compactando os PDFs em um arquivo ZIP
with zipfile.ZipFile(zip_path, 'w') as zipf:  # 'w' significa modo de escrita
    for pdf in arquivos_baixados:
        # Adicionando o PDF ao ZIP, mas usando apenas o nome do arquivo dentro do ZIP
        zipf.write(pdf, arcname=pdf.name)  # arcname define o nome do arquivo dentro do ZIP

print(f"Arquivos compactados em: {zip_path}")
