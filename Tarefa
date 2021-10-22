Aqui na Safety Soluções em Radioproteção, nós realizamos testes e calibrações em equipamentos de diagnóstico por imagem a fim de manter a qualidade dos diagnósticos realizados por estes aparelhos. Como medida de melhorar ainda mais a saúde dos brasileiros garantindo um diagnóstico seguro, a Safety criou o Safe One, um software que realiza análise automática das calibrações dos aparelhos de Raios-x, Tomografia, Ressonância Magnética, Ultrassom e Mamografia.

 Você pode conferir mais detalhes do sistema no site:

[https://safetyrad.com/portfolio/controle-de-qualidade-diario-e-semanal/](https://safetyrad.com/portfolio/controle-de-qualidade-diario-e-semanal/)

  
 Esse sistema é web e roda em contêineres na infraestrutura da AWS. Nessa vaga de estágio você irá aprender um pouco de infraestrutura, desenvolvimentos de  _apis_  e processamento de imagens médicas.

  

**Teste Prático:**

O teste é bem simples e vai envolver alguns conhecimentos básicos relacionados as atividades que você irá desempenhar.

Aconselhamos ler o artigos:

-   [https://medium.com/@hengloose/a-comprehensive-starter-guide-to-visualizing-and-analyzing-dicom-images-in-python-7a8430fcb7ed](https://medium.com/@hengloose/a-comprehensive-starter-guide-to-visualizing-and-analyzing-dicom-images-in-python-7a8430fcb7ed)

-   [https://gist.github.com/somada141/df9af37e567ba566902e](https://gist.github.com/somada141/df9af37e567ba566902e)


Você irá escrever uma classe que:

1 - Realiza a leitura das imagens DICOM (DICOM é um formato de imagem usado na medicina)

2 - Para cada imagem realizar 5 crops e calcular a média e desvio padrão dos Números de Housfield.

3 - Retornar um objeto json contendo uma identificação única da imagem e cada uma das regiões onde foi realizados os cálculo. 

**Observações:**
  

Repositório com as imagens dicom:

[https://github.com/safetyrad/vagapython](https://github.com/safetyrad/vagapython)

  

Para realizar a leitura dicom, você irá usar a biblioteca pydicom:

[https://pydicom.github.io/pydicom/stable/tutorials/installation.html](https://pydicom.github.io/pydicom/stable/tutorials/installation.html)

  

Exemplos de leitura do DICOM

[https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html](https://pydicom.github.io/pydicom/stable/auto_examples/input_output/plot_read_dicom.html)

  

Exemplos de Tags Dicom

[https://dicom.innolitics.com/ciods/ct-image](https://dicom.innolitics.com/ciods/ct-image)

  

  

O crop será conforme ilustra a figura abaixo, para cada quadrado amarelo, você irá calcular a média dos numeros de hounsfield e o desvio padrão de cada região.

[https://gist.github.com/somada141/df9af37e567ba566902e](https://gist.github.com/somada141/df9af37e567ba566902e)

  

  

Ao final você ira retornar um objeto json da seguinte forma:

  
```javascript
   {
   "PatientID":{
      "IMG1":{
         "title":"imagem 1",
         "id":"ID IMAGEM 1",
         "regioes":{
            "superior_esquerda":{
               "media":"xxx",
               "std":"xxx"
            },
            "superior_direita":{
               "media":"xxx",
               "std":"xxx"
            },
            "centro":{
               "media":"xxx",
               "std":"xxx"
            },
            "inferior_esquerda":{
               "media":"xxx",
               "std":"xxx"
            },
            "inferior_direita":{
               "media":"xxx",
               "std":"xxx"
            }
         }
      },
      "...

...

..

..""IMG n":{
         "title":"imagem n",
         "id":"ID IMAGEM n",
         "regioes":{
            "superior_esquerda":{
               "media":"xxx",
               "std":"xxx"
            },
            "superior_direita":{
               "media":"xxx",
               "std":"xxx"
            },
            "centro":{
               "media":"xxx",
               "std":"xxx"
            },
            "inferior_esquerda":{
               "media":"xxx",
               "std":"xxx"
            },
            "inferior_direita":{
               "media":"xxx",
               "std":"xxx"
            }
         }
      }
   }
}



```
  

  

  

Ao final faça um pull request para o repositório  [https://github.com/safetyrad/vagapython](https://github.com/safetyrad/vagapython)

  

  

  

Vamos começar?
