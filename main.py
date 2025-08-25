# main.py - VERSÃO CORRIGIDA

# 1. Nossos dados (no futuro, isso virá de um arquivo JSON)
banco_de_dados = [
    {
        "codigo": "VW01-T",
        "carro": "Gol G5",
        "ano": "2008-2012",
        "motor": "1.0",
        "comentarios": "Silencioso traseiro. Peça similar ao do Fox, mas o suporte é diferente.",
        "foto": "vw01-t.jpg"
    },
    {
        "codigo": "FI05-I",
        "carro": "Palio Fire",
        "ano": "2002-2007",
        "motor": "1.0 8v",
        "comentarios": "Tubo intermediário. Atenção para a versão com ou sem catalisador no coletor.",
        "foto": "fi05-i.jpg"
    }
]

# 2. Nossa função de busca (NÃO PRECISA MUDAR NADA AQUI, ELA JÁ ESTÁ CORRETA)
def buscar_peca_por_carro(modelo_carro):
    """Busca todas as peças que correspondem ao modelo de carro informado."""
    print(f"\nBuscando peças para: {modelo_carro}...")
    resultados = []
    for peca in banco_de_dados:
        if modelo_carro.lower() in peca["carro"].lower():
            resultados.append(peca)
    
    return resultados

# 3. Usando o programa (AQUI ESTÁ A MUDANÇA)

# Primeiro, pedimos a informação ao usuário E GUARDAMOS na variável 'termo_de_busca'
termo_de_busca = input("Digite o modelo do carro que deseja buscar: ")

# Agora, usamos a VARIÁVEL com a resposta do usuário para chamar a função
resultados_da_busca = buscar_peca_por_carro(termo_de_busca)

# O resto do código para mostrar o resultado continua igual
if resultados_da_busca:
    for peca in resultados_da_busca:
        print("---")
        print(f"Código: {peca['codigo']}")
        print(f"Aplicação: {peca['carro']} ano {peca['ano']}")
        print(f"Comentários: {peca['comentarios']}")
else:
    print("Nenhuma peça encontrada para o termo digitado.")