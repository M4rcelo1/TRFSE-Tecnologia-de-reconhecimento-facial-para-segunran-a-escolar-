import cv2
import os
import numpy
import main as m

data_path = 'dataset/User.'
face_classifier = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

def capturar_rosto(frame):
    cinza = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rostos = face_classifier.detectMultiScale(cinza, 1.3, 6)

    if rostos == ():
        return None

    for (x, y, w, h) in rostos:
        cropped_face = frame[y:y + h, x:x + w]

    return cropped_face


def program(id):
    cap = cv2.VideoCapture(0)
    fotos = 10
    count = 0
    countg = 0
    page = 0
    while True:
        ret, frame = cap.read()
        imagem = frame
        if capturar_rosto(frame) is not None:
            count += 1
            countg += 1
            cv2.imshow('Rostos na sua webcam', imagem)

            face = cv2.resize(capturar_rosto(frame), (300, 300))
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)

            arquivo = data_path + str(id) + '.' + str(countg) + '.jpg'
            cv2.imwrite(arquivo, face)
            cv2.putText(face, str(count), (50, 50), cv2.FONT_HERSHEY_COMPLEX, 1, (168, 200, 173), 2)

            if count >= fotos:
                count = 0
                if page == 0:
                    page0 = m.face_right()
                    page += 1
                    if page0:
                        continue
                    else:
                        m.home_page()
                        break
                if page == 1:
                    page1 = m.face_left()
                    page += 1
                    if page1:
                        continue
                    else:
                        m.home_page()
                        break
                if page == 2:
                    page2 = m.face_up()
                    page += 1
                    if page2:
                        continue
                    else:
                        m.home_page()
                        break

                if page == 3:
                    page3 = m.face_down()
                    page += 1
                    if page3:
                        continue
                    else:
                        m.home_page()
                        break
                if page == 4:
                    break


        else:
            cv2.imshow('Rostos na sua webcam', imagem)
            print("Face Not Found")
            pass

        if cv2.waitKey(1) == ord('q'):
            break

    cap.release()
    cv2.destroyAllWindows()
    os.system('python Treino.py')
    m.sucess('Muito bem! Usuário cadastrado com sucesso!')

