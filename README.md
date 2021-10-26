
# Vaga Python

1.  Rodar **"pip install -r requirements.txt"** para baixar as dependencias

2. Para rodar o projeto, dentro da pasta principal, executar **"python src/main.py"**

Teste para a vaga de estágio em Python.

Você irá escrever uma classe que:
 - Realiza a leitura das imagens DICOM (DICOM é um formato de imagem usado na medicina)

 - Para cada imagem realizar 5 crops e calcular a média e desvio padrão dos Números de Housfield.

 - Retornar um objeto json contendo uma identificação única da imagem e cada uma  das regiões onde foi realizados os cálculo.

Observações: 
> Para realizar a leitura dicom, você irá usar a biblioteca pydicom:
https://pydicom.github.io/pydicom/stable/tutorials/installation.html
> Exemplos de leitura do DICOM
https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html
> Exemplos de Tags Dicom 
https://dicom.innolitics.com/ciods/ct-image
> O crop será conforme ilustra a figura abaixo, para cada quadrado amarelo, você irá calcular a média dos numeros de hounsfield e o desvio padrão de cada região.

![telas](https://raw.githubusercontent.com/safetyrad/vagapython/main/sample.png)
