# scraper.py (VERSÃO CORRIGIDA COM BASE NA ESTRUTURA REAL DO HTML)
import requests
from bs4 import BeautifulSoup

def extrair_dados_tuper(url):
    """
    Recebe a URL de um produto no site da Tuper, extrai os dados
    e retorna uma lista de dicionários, um para cada peça.
    """
    print(f"Iniciando a extração de dados da URL: {url}")
    
    try:
        headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'}
        response = requests.get(url, headers=headers)
        response.raise_for_status()

        soup = BeautifulSoup(response.content, 'html.parser')
        
        titulo_tag = soup.find('h3')
        if titulo_tag:
            titulo_carro = titulo_tag.text.strip()
        else:
            titulo_tag_h2 = soup.find('h2', class_='font-weight-bold')
            if titulo_tag_h2:
                titulo_carro = titulo_tag_h2.text.strip()
            else:
                titulo_carro = "Modelo não encontrado na página"
                print("AVISO: Nenhuma tag <h3> ou <h2> com o nome do carro foi encontrada.")

        foto_url = ""
        div_foto = soup.find('div', class_='foto')
        if div_foto:
            img_tag = div_foto.find('img')
            if img_tag and img_tag.has_attr('src'):
                foto_url = img_tag['src']
                print(f"Foto encontrada: {foto_url}")
        else:
            print("AVISO: Div com a classe 'foto' não foi encontrada.")

        # --- LÓGICA DE BUSCA CORRIGIDA SEGUINDO A IMAGEM ---
        bloco_infopecas = soup.find('div', class_='infoPecas')
        
        if not bloco_infopecas:
            print("ERRO CRÍTICO: O bloco 'infoPecas' não foi encontrado.")
            return []

        # Procuramos o CORPO da "falsa tabela" (tbody)
        corpo_tabela = bloco_infopecas.find('tbody')
        if not corpo_tabela:
            print("ERRO CRÍTICO: O bloco 'infoPecas' foi encontrado, mas nenhum <tbody> foi encontrado dentro dele.")
            return []

        pecas_encontradas = []
        
        # Iteramos sobre cada LINHA (tr) dentro do corpo da tabela
        for linha in corpo_tabela.find_all('tr'):
            colunas = linha.find_all('td')
            
            # Verificamos se a linha tem pelo menos 2 colunas
            if len(colunas) >= 2:
                # A primeira coluna (índice 0) é o Código Tuper
                codigo_tuper = colunas[0].text.strip()
                # A segunda coluna (índice 1) é a Descrição
                descricao = colunas[1].text.strip()

                # Ignoramos linhas vazias que podem vir no HTML
                if not codigo_tuper and not descricao:
                    continue

                nova_peca = {
                    "codigo": codigo_tuper,
                    "carro": titulo_carro,
                    "ano": "",
                    "motor": "",
                    "comentarios": descricao,
                    "foto": foto_url
                }
                pecas_encontradas.append(nova_peca)

        if not pecas_encontradas:
             print("AVISO: O <tbody> foi encontrado, mas nenhuma peça pôde ser extraída das linhas.")
        else:
            print(f"{len(pecas_encontradas)} peças encontradas com sucesso!")

        return pecas_encontradas

    except requests.exceptions.RequestException as e:
        print(f"Erro ao acessar a página: {e}")
        return []
    except Exception as e:
        print(f"Ocorreu um erro inesperado: {e}")
        import traceback
        traceback.print_exc()
        return []

# --- Teste com a URL ---
if __name__ == '__main__':
    url_teste = 'https://escapamentos.tuper.com.br/produtos/escapamentos-e-catalisadores/palio-14-8v-fire-flex-2009-2011'
    dados_extraidos = extrair_dados_tuper(url_teste)
    
    if dados_extraidos:
        print("\n--- DADOS EXTRAÍDOS ---")
        for peca in dados_extraidos:
            print(peca)