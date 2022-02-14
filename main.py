import pydicom
import numpy as np
import json
import os

def crop_imagem(arquivo_imagem, inicio_linha, final_linha, inicio_coluna, final_coluna):
    """ Realiza um corte em um local específico da imagem 

    Args:
        arquivo_imagem (dataset): leitura do arquivo pydicom
        inicio_linha (int): linha que começa a leitura
        final_linha (int): linha que termina a leitura
        inicio_coluna (int): coluna que começa a leitura
        final_coluna (int): coluna que termina a leitura

    Returns:
        array: Uma matriz de um local especifico da imagem
    """
    array = arquivo_imagem.pixel_array
    array_crop = array[inicio_linha:final_linha, inicio_coluna:final_coluna].copy()

    return array_crop

def gera_json(lista_arquivos):
    """ Lê os arquivos, realiza 5 crops em cada imagem e transfere as insformações para um objeto Json

    Args:
        lista_arquivos (list): contêm o local de cada arquivo

    Returns:
        json: informações das imagens
    """
    conjunto_imagens = {}
    valor_imagem = 1

    for arquivo in lista_arquivos:
        arquivo_dicom = pydicom.dcmread(arquivo)

        # Seleção das regions da imagem
        centro = crop_imagem(arquivo_dicom, 220, 260, 220, 260)
        inferior_direito = crop_imagem(arquivo_dicom, 310, 350, 300, 340)
        inferior_esquerdo = crop_imagem(arquivo_dicom, 160, 200, 300, 340)
        superior_direito = crop_imagem(arquivo_dicom, 310, 350, 160, 200)
        superior_esquerdo = crop_imagem(arquivo_dicom, 160, 200, 160, 200)

        # Especificações da imagem para a conversão em Unidades Hounsfield
        interceptacao = arquivo_dicom.RescaleIntercept
        inclinacao = arquivo_dicom.RescaleSlope

        # Formato para a conversão em objeto Json
        informacao_imagem = {
                f"IMG {valor_imagem}": {
                    "title": arquivo,
                        "id": arquivo_dicom.PatientID,
                        "regioes":{
                            "superior_esquerda":{
                                "media": f'{np.mean(superior_esquerdo) * inclinacao + interceptacao:,.2f}',
                                "std": f'{np.std(superior_esquerdo):,.2f}'
                            },
                            "superior_direita":{
                                "media":f'{np.mean(superior_direito) * inclinacao + interceptacao:,.2f}',
                                "std":f'{np.std(superior_direito):,.2f}'
                            },
                            "centro":{
                                "media":f'{np.mean(centro) * inclinacao + interceptacao:,.2f}',
                                "std":f'{np.std(centro):,.2f}'
                            },
                            "inferior_esquerda":{
                                "media":f'{np.mean(inferior_esquerdo) * inclinacao + interceptacao:,.2f}',
                                "std":f'{np.std(inferior_esquerdo):,.2f}'
                            },
                            "inferior_direita":{
                                "media":f'{np.mean(inferior_direito) * inclinacao + interceptacao:,.2f}',
                                "std":f'{np.std(inferior_direito):,.2f}'
                            }
                        }
                    },
                }

        conjunto_imagens.update(informacao_imagem)
        valor_imagem += 1

    conjunto_imagens = {"PatientID":conjunto_imagens}
    dados_json = json.dumps(conjunto_imagens, indent=4)

    return dados_json

def main():
    # Retorna a lista dos nomes dos arquivos em uma pasta
    lista_arquivos = [f'img/{arquivo}' for arquivo in os.listdir('img')]
    arquivo_json = gera_json(lista_arquivos)

    print(arquivo_json)

if __name__ == '__main__':
    main()