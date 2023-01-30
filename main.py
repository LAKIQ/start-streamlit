import streamlit as st 
from streamlit_webrtc import webrtc_streamer
import cv2

st.set_page_config(page_title="โปรเจคตรวจจับยาแผง")

st.title("ตรวจ ยาแผง")

st.markdown("Code for Open camera")
code = '''import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("ทดสอบกล้อง")

webrtc_streamer(key="test",
                media_stream_constraints={"video": True,"audio": False})'''
st.code(code , language='python')

st.title("ทดสอบกล้อง")

webrtc_streamer(key="test",
                media_stream_constraints={"video": True,"audio": False})