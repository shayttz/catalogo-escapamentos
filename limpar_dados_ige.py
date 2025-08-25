# limpar_dados_ige.py
import json
import re

def limpar_e_refinar_dados(nome_arquivo_entrada, nome_arquivo_saida):
    """
    Lê um arquivo JSON de peças extraídas, limpa os dados, melhora a extração
    de códigos e salva em um novo arquivo.
    """
    try:
        with open(nome_arquivo_entrada, 'r', encoding='utf-8') as f:
            dados_brutos = json.load(f)
    except FileNotFoundError:
        print(f"Erro: Arquivo '{nome_arquivo_entrada}' não encontrado.")
        return

    print(f"Iniciando limpeza de {len(dados_brutos)} peças...")
    dados_limpos = []
    
    for peca in dados_brutos:
        comentarios = peca.get('comentarios', '')
        
        # 1. Filtro de "lixo": Ignora peças com comentários inúteis
        if '*' in comentarios or 'na peça' in comentarios or not comentarios.replace("(IGE)", "").strip():
            continue

        codigo_final = peca.get('codigo', 'A VERIFICAR')

        # 2. Nova tentativa, mais inteligente, de encontrar o código IGE, 
        #    mesmo que não esteja no final. Procura por um número de 3 a 5 dígitos.
        if codigo_final == "A VERIFICAR":
            # Procura por um código numérico de 3 a 5 dígitos na linha de comentários
            matches = re.findall(r'\b(\d{3,5})\b', comentarios)
            if matches:
                # Pega o último número encontrado, que é provavelmente o código IGE
                codigo_final = matches[-1]

        # 3. Limpeza final dos comentários
        comentarios_limpos = comentarios.replace("(IGE)", "").strip()
        # Remove o código que acabamos de extrair para não ficar duplicado no texto
        comentarios_limpos = re.sub(r'\s+\d{3,5}$', '', comentarios_limpos).strip()

        peca_limpa = {
            "codigo": codigo_final,
            "carro": peca.get('carro', 'N/A'),
            "tipo": peca.get('tipo', 'Outros'),
            "comentarios": f"(IGE) {comentarios_limpos}",
            "foto": ""
        }
        
        # Só adiciona a peça se ela tiver uma descrição minimamente válida
        if len(comentarios_limpos) > 5:
            dados_limpos.append(peca_limpa)

    # 4. Salva o resultado final
    try:
        with open(nome_arquivo_saida, 'w', encoding='utf-8') as f:
            json.dump(dados_limpos, f, indent=4, ensure_ascii=False)
        print(f"Limpeza concluída! {len(dados_limpos)} peças limpas foram salvas em '{nome_arquivo_saida}'.")
    except Exception as e:
        print(f"Erro ao salvar o arquivo final: {e}")


# --- Execução Principal ---
if __name__ == '__main__':
    limpar_e_refinar_dados('ige_importado.json', 'ige_final.json')