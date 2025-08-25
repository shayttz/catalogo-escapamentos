# main.py (VERSÃO FINAL COM CAMPO "TIPO")

import json
from scraper import extrair_dados_tuper

# ... (funções carregar_dados e salvar_dados continuam iguais) ...
def carregar_dados():
    try:
        with open('dados.json', 'r', encoding='utf-8') as f: return json.load(f)
    except FileNotFoundError: return []
def salvar_dados(dados):
    with open('dados.json', 'w', encoding='utf-8') as f: json.dump(dados, f, indent=4, ensure_ascii=False)

def buscar_peca(banco_de_dados, termo_busca):
    palavras_chave = termo_busca.lower().split()
    print(f"\nBuscando por peças que contenham TODAS as palavras: {palavras_chave}...")
    resultados = []
    
    for peca in banco_de_dados:
        # Adicionamos o campo 'tipo' à nossa busca!
        texto_pesquisavel = f"{peca.get('codigo', '')} {peca.get('carro', '')} {peca.get('comentarios', '')} {peca.get('tipo', '')}".lower()
        
        if all(palavra in texto_pesquisavel for palavra in palavras_chave):
            resultados.append(peca)
            
    return resultados

def adicionar_peca(banco_de_dados):
    print("\n--- Adicionando Nova Peça Manualmente ---")
    # Pedimos o novo campo ao usuário
    tipo = input("Tipo da peça (ex: Silencioso Traseiro): ")
    codigo = input("Código da peça: ")
    carro = input("Modelo do carro: ")
    comentarios = input("Comentários/macetes: ")
    foto = input("URL ou nome do arquivo da foto: ")

    nova_peca = {
        "codigo": codigo, "carro": carro, "tipo": tipo,
        "comentarios": comentarios, "foto": foto
    }
    banco_de_dados.append(nova_peca)
    salvar_dados(banco_de_dados)
    print("Peça adicionada com sucesso!")

# --- Início do Programa Principal (Menu) ---
banco_de_dados = carregar_dados()

while True:
    # ... (o menu continua o mesmo) ...
    print("\n--- Catálogo Inteligente de Escapamentos ---")
    print("1. Buscar Peça")
    print("2. Adicionar Peça Manualmente")
    print("3. Importar Peças da Tuper (via URL)")
    print("4. Sair")
    escolha = input("Escolha uma opção: ")

    if escolha == '1':
        termo_de_busca = input("Digite o que deseja buscar (ex: silencioso traseiro palio): ")
        resultados_da_busca = buscar_peca(banco_de_dados, termo_de_busca)

        if resultados_da_busca:
            print(f"\n--- {len(resultados_da_busca)} resultado(s) encontrado(s) ---")
            for peca in resultados_da_busca:
                # Exibimos o novo campo 'tipo' para clareza
                print(f"Tipo: {peca.get('tipo', 'N/A')}")
                print(f"Código: {peca.get('codigo', 'N/A')}")
                print(f"Aplicação: {peca.get('carro', 'N/A')}")
                print(f"Comentários: {peca.get('comentarios', 'N/A')}")
                if peca.get('foto'):
                    print(f"Foto: {peca['foto']}")
                print("-" * 20)
        else:
            print("Nenhuma peça encontrada para os termos digitados.")
    
    # ... (as outras opções do menu continuam iguais) ...
    elif escolha == '2': adicionar_peca(banco_de_dados)
    elif escolha == '3':
        url = input("Cole a URL do produto no site da Tuper: ")
        novas_pecas = extrair_dados_tuper(url)
        if novas_pecas:
            banco_de_dados.extend(novas_pecas)
            salvar_dados(banco_de_dados)
            print(f"\nSucesso! {len(novas_pecas)} novas peças foram importadas e salvas.")
        else:
            print("\nNenhuma peça foi importada.")
    elif escolha == '4':
        print("Saindo do programa. Até mais!")
        break
    else:
        print("Opção inválida.")