!pip install pyttsx3

import cv2
import mediapipe as mp
import numpy as np
import pyttsx3
import time
import threading

sobrancelha_esq=[285,295]
sobrancelha_dir=[55,65]

sobrancelhas = sobrancelha_esq+sobrancelha_dir
sobrancelhas

p_olho_esq = [380, 373]
p_olho_dir = [144, 153]

p_olhos = p_olho_esq+p_olho_dir
p_olhos

p_boca = [82, 87, 13, 14, 312, 317, 78, 308]

def calculo_mar(face,p_boca):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        face_boca = face[p_boca,:]

        mar = (np.linalg.norm(face_boca[0]-face_boca[1])+np.linalg.norm(face_boca[2]-face_boca[3])+np.linalg.norm(face_boca[4]-face_boca[5]))/(2*(np.linalg.norm(face_boca[6]-face_boca[7])))
    except:
        mar = 0.0
    
    return mar

pontos = np.array(p_olhos + sobrancelhas)
pontos

def calculo_dist_sobrancelha_olho(face, sobrancelhas, p_olhos):
    try:
        face = np.array([[coord.x, coord.y] for coord in face])
        pontos = np.array(p_olhos + sobrancelhas)
        face_sob_olho = face[pontos]
        
        dso = (
            np.linalg.norm(face_sob_olho[0] - face_sob_olho[4]) +
            np.linalg.norm(face_sob_olho[1] - face_sob_olho[5]) +
            np.linalg.norm(face_sob_olho[2] - face_sob_olho[6])
        ) / (2 * np.linalg.norm(face_sob_olho[3] - face_sob_olho[7]))
        
    except:
        dso = 0.0
    return dso


# Inicialize o mecanismo de texto para fala
engine = pyttsx3.init()

# Configurações do Mediapipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils

# Funções (assuma que calculo_dist_sobrancelha_olho e calculo_mar já estão definidas)

# Inicialize a captura de vídeo
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)  # Reduz a largura do frame
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)  # Reduz a altura do frame

# Variáveis para controle
ultima_emocao = None
ultima_execucao = 0
intervalo_minimo = 3  # Intervalo mínimo entre execuções de áudio
frame_count = 0  # Contador de frames
processar_cada_n_frames = 10  # Processa 1 em cada 10 frames

# Função para executar o áudio em um thread separado
def falar_emocao(emocao):
    engine = pyttsx3.init()
    engine.say(emocao)
    engine.runAndWait()

# Loop principal
with mp_face_mesh.FaceMesh(min_detection_confidence=0.3, min_tracking_confidence=0.3) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print('Ignorando o frame vazio da câmera.')
            continue

        frame_count += 1
        if frame_count % processar_cada_n_frames != 0:
            # Mostra o frame sem processar
            cv2.imshow('Camera', frame)
            if cv2.waitKey(10) & 0xFF == ord('c'):
                break
            continue

        comprimento, largura, _ = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)

        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                # Desenha os landmarks (opcional)
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec=mp_drawing.DrawingSpec(color=(255, 102, 102), thickness=1, circle_radius=1),
                    connection_drawing_spec=mp_drawing.DrawingSpec(color=(102, 204, 0), thickness=1, circle_radius=1))

                face = face_landmarks.landmark

                # Cálculos de MAR e DSO
                dso = calculo_dist_sobrancelha_olho(face, sobrancelhas, p_olhos)
                mar = calculo_mar(face, p_boca)

                # Adiciona informações ao frame
                cv2.rectangle(frame, (0, 1), (290, 140), (58, 58, 55), -1)
                cv2.putText(frame, f"DSO: {round(dso, 2)}", (1, 24),
                            cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)
                cv2.putText(frame, f"MAR: {round(mar, 2)}", (1, 50),
                            cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2)

                # Determine emoção com base nos valores de MAR e DSO
                if 0.9 <= mar <= 1.5 and 1.40 <= dso <= 1.45:
                    emocao = "Parece que está surpreso"
                elif 0.2 <= mar <= 0.5 and 1.48 <= dso <= 1.55:
                    emocao = "Parece que está feliz"
                elif 1.57 <= dso <= 1.70:
                    emocao = "Parece que está com raiva"
                else:
                    emocao = "Parece que está normal"

                # Mostra a emoção no frame
                cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                cv2.putText(frame, emocao, (180, 450),
                            cv2.FONT_HERSHEY_DUPLEX, 0.85, (58, 58, 55), 1)

                # Fala a emoção apenas se mudou e respeita o intervalo de tempo
                agora = time.time()
                if emocao != ultima_emocao and (agora - ultima_execucao >= intervalo_minimo):
                    threading.Thread(target=falar_emocao, args=(emocao,)).start()
                    ultima_emocao = emocao
                    ultima_execucao = agora

        except Exception as e:
            print(f"Erro no processamento: {e}")
            pass

        # Mostra o frame
        cv2.imshow('Camera', frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break

cap.release()
cv2.destroyAllWindows()