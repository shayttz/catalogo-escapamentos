# pdf_extractor.py (VERSÃO MAIS INTELIGENTE - IGNORA ANOS)
import fitz # PyMuPDF
import json
import re

def identificar_tipo_peca(descricao):
    # ... (esta função continua a mesma) ...
    desc = descricao.lower()
    if 'silencioso traseiro' in desc: return 'Silencioso Traseiro'
    if 'silencioso intermediário' in desc: return 'Silencioso Intermediário'
    if 'tubo intermediário' in desc: return 'Tubo Intermediário'
    if 'coletor com catalisador' in desc: return 'Coletor com Catalisador'
    if 'catalisador' in desc: return 'Catalisador'
    if 'tubo do motor' in desc: return 'Tubo de Motor'
    if 'flexível' in desc: return 'Flexível'
    if 'coletor' in desc: return 'Coletor'
    return 'Outros'

def processar_pdf(nome_arquivo_pdf):
    pecas_catalogadas = []
    current_car_model = "Não identificado"

    try:
        doc = fitz.open(nome_arquivo_pdf)
        print(f"Processando {doc.page_count} páginas de '{nome_arquivo_pdf}'...")

        for num_pagina in range(doc.page_count):
            pagina = doc.load_page(num_pagina)
            texto_da_pagina = pagina.get_text("text")
            
            if "ÍNDICE DE PEÇAS" in texto_da_pagina or "ÍNDICE\nÍNDICE" in texto_da_pagina:
                print(f"Página {num_pagina + 1}: Ignorando (página de índice).")
                continue
            
            print(f"Página {num_pagina + 1}: Processando...")
            
            linhas = texto_da_pagina.split('\n')
            is_reading_parts = False
            
            for i, linha in enumerate(linhas):
                linha_original = linha.strip()
                if not linha_original: continue

                if linha_original.upper() == 'IGE' and i + 2 < len(linhas):
                    if linhas[i+1].strip().upper() == 'MONTADORA' and linhas[i+2].strip().upper() == 'DESCRIÇÃO':
                        is_reading_parts = True
                        for j in range(i - 1, -1, -1):
                            linha_anterior = linhas[j].strip()
                            if len(linha_anterior) > 12 and linha_anterior.upper() == linha_anterior:
                                current_car_model = linha_anterior
                                break
                        continue

                if len(linha_original) > 12 and linha_original.upper() == linha_original and not 'IGE' in linha_original:
                    is_reading_parts = False

                if is_reading_parts:
                    if linha_original.upper() in ['IGE', 'MONTADORA', 'DESCRIÇÃO', 'PREÇO R$']:
                        continue
                    
                    codigo_ige = "A VERIFICAR"
                    linha_para_analise = linha_original

                    # --- NOVA LÓGICA PARA IGNORAR ANOS ---
                    # 1. Removemos padrões de ano comuns (ex: "a 1991", "a ...", "jul/1977") do final da linha
                    #    antes de procurar pelo código.
                    linha_sem_anos = re.sub(r'-\s*\d{4}\s*a\s*\.{3}', '', linha_para_analise)
                    linha_sem_anos = re.sub(r'a\s+\w{3}/\d{4}', '', linha_sem_anos)
                    linha_sem_anos = re.sub(r'a\s+\d{4}', '', linha_sem_anos)
                    linha_sem_anos = re.sub(r'-\s*\w{3}/\d{2,4}\s*a\s*\w*/?\d* a?\s*\.{0,3}', '', linha_sem_anos)


                    # 2. Agora, procuramos pelo código IGE na linha já "limpa"
                    match_ige = re.search(r'\b(\d{3,4})$', linha_sem_anos.strip())
                    
                    if match_ige:
                        codigo_potencial = match_ige.group(1)
                        # Verificação final: O código não pode ser um ano.
                        if not (1950 <= int(codigo_potencial) <= 2030):
                             codigo_ige = codigo_potencial
                    
                    descricao_final = linha_original
                    tipo_peca = identificar_tipo_peca(descricao_final)
                    comentarios = f"(IGE) {descricao_final}"

                    if descricao_final and len(descricao_final) > 3:
                        nova_peca = {
                            "codigo": codigo_ige,
                            "carro": current_car_model,
                            "tipo": tipo_peca,
                            "comentarios": comentarios,
                            "foto": ""
                        }
                        pecas_catalogadas.append(nova_peca)

        doc.close()

        if pecas_catalogadas:
            nome_arquivo_saida = "ige_importado_final.json"
            with open(nome_arquivo_saida, 'w', encoding='utf-8') as f:
                json.dump(pecas_catalogadas, f, indent=4, ensure_ascii=False)
            print(f"\nPROCESSO CONCLUÍDO! {len(pecas_catalogadas)} peças foram extraídas e salvas em '{nome_arquivo_saida}'.")
        else:
            print("\nNenhuma peça foi extraída. Verifique os padrões no PDF.")

    except Exception as e:
        print(f"Ocorreu um erro ao processar o PDF: {e}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    NOME_DO_ARQUIVO_PDF = "123.pdf"
    processar_pdf(NOME_DO_ARQUIVO_PDF)