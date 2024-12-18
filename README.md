# Detecção Facial em Tempo Real

Este código implementa uma aplicação de **detecção facial em tempo real**, utilizando as bibliotecas **MediaPipe** e **OpenCV** para detectar emoções com base em medidas faciais, como a distância sobrancelha-olho (DSO) e a taxa de abertura da boca (MAR). A aplicação realiza a captura da imagem da câmera em tempo real e processa as informações para identificar características faciais e suas respectivas emoções.

## Tecnologias Utilizadas

- **Linguagem de Programação**: Python
- **Editor de Texto**: VSCode
- **Ambiente Virtual**: Anaconda
- **Bibliotecas**: OpenCV, para captura de vídeo e processamento de imagens.
- **Framework**: MediaPipe, para detecção de pontos faciais e análise de expressões.

## Funcionalidades

- **Detecção de Rosto**: Utiliza o MediaPipe para identificar e rastrear pontos-chave do rosto.
- **Cálculo de Métricas**: Mede a distância sobrancelha-olho (DSO) e a taxa de abertura da boca (MAR) para inferir a emoção.
- **Exibição em Tempo Real**: Processa o vídeo da câmera e exibe o resultado com as medições faciais.

## Como Rodar

1. Clone este repositório.
2. Crie um ambiente virtual no Anaconda:
   ```bash
   conda create -n deteccao_facial python=3.9
   conda activate deteccao_facial
3. Instale as dependências:
   ```bash
    !pip install opencv-python==4.6.0.66
    !pip install mediapipe
    !pip install numpy==1.22.3
4. Execute o código.
