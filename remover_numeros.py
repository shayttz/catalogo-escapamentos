# remover_numeros.py (VERSÃO FINAL COM THRESHOLD ADAPTATIVO)
import cv2
import numpy as np
import os

def remover_numeros_dos_blocos(pasta_entrada, pasta_saida):
    """
    Usa um threshold adaptativo para encontrar e remover todos os números,
    independentemente de serem escuros ou claros.
    """
    if not os.path.exists(pasta_saida):
        os.makedirs(pasta_saida)
        print(f"Pasta de saída '{pasta_saida}' criada.")

    arquivos = [f for f in os.listdir(pasta_entrada) if f.endswith('.png')]
    print(f"Encontrados {len(arquivos)} blocos para processar...")

    for nome_arquivo in arquivos:
        caminho_arquivo = os.path.join(pasta_entrada, nome_arquivo)
        imagem = cv2.imread(caminho_arquivo, cv2.IMREAD_GRAYSCALE)
        
        if imagem is None:
            print(f"AVISO: Não foi possível ler o arquivo: {nome_arquivo}")
            continue

        imagem_sem_numeros = cv2.cvtColor(imagem, cv2.COLOR_GRAY2BGR)

        # --- A MÁGICA ESTÁ AQUI: THRESHOLD ADAPTATIVO ---
        # Em vez de um valor fixo, o algoritmo calcula o limiar ideal para cada
        # pequena região da imagem.
        limiar_inv = cv2.adaptiveThreshold(
            imagem, 
            255, # O valor máximo (branco)
            cv2.ADAPTIVE_THRESH_GAUSSIAN_C, # Método de cálculo
            cv2.THRESH_BINARY_INV, # Inverte (fundo preto, formas brancas)
            11, # Tamanho da vizinhança (deve ser ímpar)
            2   # Uma constante C subtraída da média
        )

        contornos, _ = cv2.findContours(limiar_inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contorno in contornos:
            x, y, w, h = cv2.boundingRect(contorno)
            area = cv2.contourArea(contorno)
            proporcao = w / float(h) if h > 0 else 0
            
            # Usamos as mesmas regras de calibração que encontramos
            if not (100 < area < 800):
                continue
            if not (0.3 < proporcao < 1.4):
                continue

            # Apaga o número encontrado de forma precisa
            cv2.drawContours(imagem_sem_numeros, [contorno], -1, (255, 255, 255), -1)

        caminho_saida = os.path.join(pasta_saida, nome_arquivo)
        cv2.imwrite(caminho_saida, imagem_sem_numeros)
        print(f"Processado: {nome_arquivo}")

    print(f"\nProcesso concluído! Imagens sem números salvas em '{pasta_saida}'.")


# --- Execução Principal ---
if __name__ == '__main__':
    PASTA_ENTRADA = "blocos_recortados_final"
    PASTA_SAIDA = "blocos_sem_numeros"
    
    if not os.path.exists(PASTA_ENTRADA):
        print(f"Erro: A pasta de entrada '{PASTA_ENTRADA}' não foi encontrada.")
    else:
        remover_numeros_dos_blocos(PASTA_ENTRADA, PASTA_SAIDA)