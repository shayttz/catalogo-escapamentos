# recortar_blocos_pdf.py (VERSÃO FINAL COM LIMIAR FIXO E SEGURO)
import fitz # PyMuPDF
import cv2 # OpenCV
import numpy as np
import os

def extrair_blocos_do_pdf(nome_arquivo_pdf):
    PASTA_SAIDA = "blocos_recortados_final"
    
    if not os.path.exists(PASTA_SAIDA):
        os.makedirs(PASTA_SAIDA)
        print(f"Pasta '{PASTA_SAIDA}' criada com sucesso.")

    try:
        doc = fitz.open(nome_arquivo_pdf)
        print(f"Iniciando processamento de {doc.page_count} páginas...")

        total_blocos_salvos = 0

        for num_pagina in range(doc.page_count):
            pagina = doc.load_page(num_pagina)
            
            texto_da_pagina = pagina.get_text("text")
            if "ÍNDICE DE PEÇAS" in texto_da_pagina or "ÍNDICE\nÍNDICE" in texto_da_pagina:
                print(f"Página {num_pagina + 1}: Ignorando (página de índice).")
                continue

            imagem_original = None
            
            imagens_na_pagina = pagina.get_images(full=True)
            imagens_grandes = [img for img in imagens_na_pagina if img[2] > 500 and img[3] > 500]

            if imagens_grandes:
                print(f"Página {num_pagina + 1}: Detectada como Raster (imagem). Extraindo na qualidade original...")
                maior_imagem_xref = max(imagens_grandes, key=lambda img: img[2] * img[3])[0]
                pix = fitz.Pixmap(doc, maior_imagem_xref)
            else:
                print(f"Página {num_pagina + 1}: Detectada como Vetorial. Renderizando com 300 DPI...")
                pix = pagina.get_pixmap(dpi=300)

            img_np = np.frombuffer(pix.samples, dtype=np.uint8).reshape(pix.h, pix.w, pix.n)
            if img_np.shape[2] == 4:
                imagem_original = cv2.cvtColor(img_np, cv2.COLOR_RGBA2BGR)
            else:
                imagem_original = cv2.cvtColor(img_np, cv2.COLOR_RGB2BGR)

            cinza = cv2.cvtColor(imagem_original, cv2.COLOR_BGR2GRAY)
            _, limiar = cv2.threshold(cinza, 240, 255, cv2.THRESH_BINARY_INV)
            contornos, _ = cv2.findContours(limiar, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            
            blocos_encontrados_na_pagina = 0
            for contorno in contornos:
                area = cv2.contourArea(contorno)
                if area > 100000:
                    x, y, w, h = cv2.boundingRect(contorno)
                    bloco_recortado = imagem_original[y:y+h, x:x+w]
                    
                    recorte_cinza = cv2.cvtColor(bloco_recortado, cv2.COLOR_BGR2GRAY)
                    
                    # --- A CORREÇÃO DEFINITIVA ---
                    # Voltamos ao limiar fixo, mas com um valor alto (220) para ser seguro.
                    # Isso significa: "qualquer coisa que não for quase branca, vira preta".
                    # Isso preserva os detalhes finos.
                    _, recorte_final_bw = cv2.threshold(recorte_cinza, 220, 255, cv2.THRESH_BINARY)
                    
                    nome_arquivo_saida = os.path.join(PASTA_SAIDA, f"pagina_{num_pagina + 1}_bloco_{blocos_encontrados_na_pagina + 1}.png")
                    cv2.imwrite(nome_arquivo_saida, recorte_final_bw)
                    
                    blocos_encontrados_na_pagina += 1
            
            if blocos_encontrados_na_pagina > 0:
                print(f" -> Sucesso! {blocos_encontrados_na_pagina} bloco(s) salvo(s) com alto contraste.")
                total_blocos_salvos += blocos_encontrados_na_pagina
            else:
                print(f" -> Nenhum bloco grande encontrado nesta página.")

        doc.close()
        print(f"\nPROCESSO CONCLUÍDO! Total de {total_blocos_salvos} blocos salvos na pasta '{PASTA_SAIDA}'.")

    except Exception as e:
        print(f"Ocorreu um erro: {e}")
        import traceback
        traceback.print_exc()

# --- Execução Principal ---
if __name__ == '__main__':
    NOME_DO_ARQUIVO_PDF = "123.pdf"
    extrair_blocos_do_pdf(NOME_DO_ARQUIVO_PDF)