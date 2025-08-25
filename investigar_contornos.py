# investigar_contornos.py (VERSÃO FINAL PARA CALIBRAGEM FINA)
import cv2
import numpy as np
import os

def investigar_imagem(caminho_imagem):
    """
    Usa o Threshold Adaptativo para encontrar TODOS os contornos e nos dizer
    suas medidas exatas, para podermos calibrar o filtro de remoção.
    """
    imagem = cv2.imread(caminho_imagem)
    if imagem is None:
        print("Erro: Não foi possível ler a imagem.")
        return

    imagem_cinza = cv2.cvtColor(imagem, cv2.COLOR_BGR2GRAY)

    # Usa exatamente o mesmo método de detecção do script de remoção
    limiar_inv = cv2.adaptiveThreshold(
        imagem_cinza, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
        cv2.THRESH_BINARY_INV, 11, 2
    )

    contornos, _ = cv2.findContours(limiar_inv, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

    print(f"--- ANÁLISE DETALHADA DA IMAGEM: {caminho_imagem} ---")
    print(f"Total de contornos encontrados: {len(contornos)}")

    for contorno in contornos:
        area = int(cv2.contourArea(contorno))
        x, y, w, h = cv2.boundingRect(contorno)
        
        # Desenha o contorno em verde
        cv2.drawContours(imagem, [contorno], -1, (0, 255, 0), 2)
        # Escreve o valor da área em vermelho perto do contorno
        cv2.putText(imagem, str(area), (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 1)

    print("\nUma janela com a imagem analisada vai aparecer.")
    print("Concentre-se nos NÚMEROS DA TABELA e veja os valores de ÁREA em vermelho.")
    print("Pressione qualquer tecla para fechar.")
    cv2.imshow("Imagem Analisada para Calibração Final", imagem)
    cv2.waitKey(0)
    cv2.destroyAllWindows()


# --- Execução Principal ---
if __name__ == '__main__':
    # Use a imagem que sabemos que tem números na tabela
    arquivo_exemplo = 'pagina_7_bloco_2.png' 
    
    if not os.path.exists(arquivo_exemplo):
        print(f"Erro: O arquivo de exemplo '{arquivo_exemplo}' não foi encontrado.")
    else:
        investigar_imagem(arquivo_exemplo)