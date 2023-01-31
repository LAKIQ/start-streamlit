import streamlit as st 
from streamlit_webrtc import webrtc_streamer
import cv2
import numpy as np
import av

st.set_page_config(page_title="โปรเจคตรวจจับยาแผง") 

st.title("ตรวจ ยาแผง")

st.markdown("Code for Open camera")
code1 = '''
st.title("ทดสอบกล้อง")

webrtc_streamer(key="test",
                media_stream_constraints={"video": True,"audio": False})'''
st.code(code1 , language='python')

st.title("ทดสอบกล้อง")

webrtc_streamer(key="test",
                media_stream_constraints={"video": True,"audio": False})


st.title("ทดสอบคำสั่งการกดปุ่ม")

run_btn = st.button("Run")
if run_btn:
    st.markdown("Button has already clicked") 

age_inp = st.number_input("Input")
st.markdown(f"Your input is {age_inp}")       


st.title("ทดสอบอัปโหลดรูป")

st.markdown("Code for Open Photo")
code2 = '''img_file = st.file_uploader("เปิดไฟล์ภาพ")

if img_file is not None:    
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)    
    st.image(img ,caption="OpenCV Format",channels="BGR")'''
st.code(code2 , language='python')

img_file = st.file_uploader("เปิดไฟล์ภาพ")

if img_file is not None:    
    file_bytes = np.asarray(bytearray(img_file.read()), dtype=np.uint8)
    img = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)    
    st.image(img ,caption="OpenCV Format",channels="BGR")


st.markdown("Capture Picture")

#picture = st.camera_input("Take a picture")

#if picture:
    #st.image(picture)


face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

st.title("ตรวจจับใบหน้า")

class VideoProcessor:  
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        #-------------------------------------------
        img = cv2.flip(img,1) 
        img_gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        faces = face_cascade.detectMultiScale(img_gray, 1.3, 5)
        for (x,y,w,h) in faces:
            cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),5)
        #-------------------------------------------
        return av.VideoFrame.from_ndarray(img,format="bgr24")

webrtc_streamer(key="test2",
                video_processor_factory=VideoProcessor,
                media_stream_constraints={"video": True,"audio": False})


st.title("ทดสอบถ่ายรูป")

img_file_buffer = st.camera_input("Take a picture")

if img_file_buffer is not None:
    # To read image file buffer with OpenCV:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    # Check the type of cv2_img:
    # Should output: <class 'numpy.ndarray'>
    # st.write(type(cv2_img))

    #cv2_img2 = cv2.flip(cv2_img,1)
    imgYCrCb  = cv2.cvtColor(cv2_img,cv2.COLOR_BGR2YCR_CB)
    channels = cv2.split(imgYCrCb)
    Cr = channels[1]
    cv2.imshow("Cr",Cr)

    ret,BW = cv2.threshold(Cr,150,255,cv2.THRESH_BINARY)
    cv2.imshow("BW",BW)

    contours, hierarchy = cv2.findContours(BW,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    areas = [cv2.contourArea(c) for c in contours]
    #st.write(areas)
    max_index = np.argmax(areas)
    cnt = contours[max_index]

    x,y,w,h = cv2.boundingRect(cnt)
    cv2.rectangle(cv2_img,(x,y),(x+w,y+h),(0,255,255),4)
    # Check the shape of cv2_img:
    # Should output shape: (height, width, channels)
    # st.write(cv2_img.shape)
    st.image(cv2_img,caption="OpenCV Format",channels="BGR")

