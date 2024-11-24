##copiar e colar na ultima célula do arquivo projeto.ipynb e colocar para rodar e vê se trava

start_time = None
estado_atual = None

engine = pyttsx3.init()

cap = cv2.VideoCapture(0)

def falar_emocao(emocao):
    engine = pyttsx3.init()
    engine.say(emocao)
    engine.runAndWait()

with mp_face_mesh.FaceMesh(min_detection_confidence=0.5, min_tracking_confidence=0.5) as facemesh:
    while cap.isOpened():
        sucesso, frame = cap.read()
        if not sucesso:
            print('Ignorando o frame vazio da câmera.')
            continue
        comprimento, largura, _ = frame.shape

        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        saida_facemesh = facemesh.process(frame)
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
        
        try:
            for face_landmarks in saida_facemesh.multi_face_landmarks:
                mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                    landmark_drawing_spec = mp_drawing.DrawingSpec(color=(255,102,102),thickness=1,circle_radius=1),
                    connection_drawing_spec = mp_drawing.DrawingSpec(color=(102,204,0),thickness=1,circle_radius=1))
                face = face_landmarks.landmark
                for id_coord, coord_xyz in enumerate(face):
                    if id_coord in p_olhos:
                       coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x,coord_xyz.y, largura, comprimento)
                       cv2.circle(frame, coord_cv, 2, (255,0,0), -1)
                    if id_coord in sobrancelhas:
                       coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x,coord_xyz.y, largura, comprimento)
                       cv2.circle(frame, coord_cv, 2, (255,0,0), -1)
                    if id_coord in p_boca:
                       coord_cv = mp_drawing._normalized_to_pixel_coordinates(coord_xyz.x,coord_xyz.y, largura, comprimento)
                       cv2.circle(frame, coord_cv, 2, (255,0,0), -1)

                dso = calculo_dist_sobrancelha_olho(face, sobrancelhas, p_olhos)
                cv2.rectangle(frame, (0,1),(290,140),(58,58,55),-1)
                cv2.putText(frame, f"DSO: {round(dso, 2)}", (1, 24),
                                cv2.FONT_HERSHEY_DUPLEX,
                                0.9, (255, 255, 255), 2)
                mar = calculo_mar(face,p_boca)
                cv2.putText(frame, f"MAR: {round(mar, 2)}", (1, 50),
                                cv2.FONT_HERSHEY_DUPLEX,
                                0.9, (255, 255, 255), 2)


                if 0.9 <= mar <= 1.5 and 1.40 <= dso <= 1.45:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Parece que esta surpreso", (180, 450),
                                        cv2.FONT_HERSHEY_DUPLEX, 
                                        0.85, (58,58,55), 1)
                    if estado_atual != "surpreso":
                        # Se o estado mudou, reinicia o temporizador
                        estado_atual = "surpreso"
                        start_time = time.time()
                    elif time.time() - start_time >= 0.5:
                        # Se a condição persistir por 0,5 segundo
                        emocao = "Parece que está surpreso"
                        falar_emocao(emocao)
                        start_time = None  # Reseta o temporizador após a ação
                        estado_atual = None  # Volta para o estado inicial

                elif 0.2 <= mar <= 0.5 and 1.48 <= dso <= 1.55:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Parece que esta feliz", (180, 450),
                                        cv2.FONT_HERSHEY_DUPLEX, 
                                        0.85, (58,58,55), 1)
                    if estado_atual != "feliz":
                        # Se o estado mudou, reinicia o temporizador
                        estado_atual = "feliz"
                        start_time = time.time()
                    elif time.time() - start_time >= 0.5:
                        # Se a condição persistir por 0,5 segundo
                        emocao = "Parece que está feliz"
                        falar_emocao(emocao)
                        start_time = None  # Reseta o temporizador após a ação
                        estado_atual = None
        
                elif 1.57 <= dso <= 1.70:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Parece que esta com raiva", (180, 450),
                                        cv2.FONT_HERSHEY_DUPLEX, 
                                        0.85, (58,58,55), 1)
                    if estado_atual != "raiva":
                        # Se o estado mudou, reinicia o temporizador
                        estado_atual = "raiva"
                        start_time = time.time()
                    elif time.time() - start_time >= 0.5:
                        # Se a condição persistir por 0,5 segundo
                        emocao = "Parece que esta com raiva"
                        falar_emocao(emocao)
                        start_time = None  # Reseta o temporizador após a ação
                        estado_atual = None
                else:
                    cv2.rectangle(frame, (30, 400), (610, 452), (109, 233, 219), -1)
                    cv2.putText(frame, f"Parece que esta normal", (180, 450),
                                        cv2.FONT_HERSHEY_DUPLEX, 
                                        0.85, (58,58,55), 1)
                    
        except:
            pass

        cv2.imshow('Camera',frame)
        if cv2.waitKey(10) & 0xFF == ord('c'):
            break
cap.release()
cv2.destroyAllWindows()