import streamlit as st
from streamlit_lottie import st_lottie
import json
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


st.set_page_config(page_title="fitcampro",layout="wide")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)


local_css("style/style.css")

#animasyon
def load_lottiefile(filepath:str):
    with open(filepath, "r") as f:
        return json.load(f)

dumbell_anim = load_lottiefile("animations/circleDumbell.json")
pose_anim = load_lottiefile("animations/poseanimation.json")
calc_anim = load_lottiefile("animations/calculatur.json")



col1, col2, col3 = st.columns(3)
with col1:
    st.title(":red[FITCAMPRO ⚡]")
    st.subheader(" Hoş Geldiniz! Spor ve sağlıklı yaşamın vazgeçilmez bir parçası olduğuna inanıyoruz.Bu nedenle, egzersizlerinizi daha verimli ve keyifli hale getirecek yenilikçi bir platform geliştirdik.Web sitemizde, antrenmanlarınızı optimize etmek için ihtiyacınız olan tüm araçlar bir arada:")
    st.write("---")



with col3 :
    st_lottie(
        dumbell_anim,
        speed=1,
        loop=True,
        quality="medium",
        height=500,
        width=500,)





col1, col2, col3 = st.columns(3)
with col1:
    st.title("1-EGZERSSIZ TESPIT MODULU")
    st.subheader(
        "kullanıcıların egzersiz formlarını takip etmelerine ve tekrar sayısını hesaplamalarına yardımcı olan kullanışlı"
        " bir araçtır. MediaPipe Pose kütüphanesinin kullanımıyla gerçek zamanlı"
        " vücut eklem tespiti ve açı hesaplaması yapılarak egzersiz hareketlerinin tanınması sağlanmıştır.")
    st.write("---")


with col3 :
    st_lottie(
        pose_anim,
        speed=1,
        loop=True,
        quality="medium",
        height=400,
        width=500, )


col1, col2, col3 = st.columns(3)
with col1:
    st.title("2-KALORI HESAPLAYICI")
    st.subheader(
        " Kalori hesaplayıcı, günlük kalori "
        "ihtiyacınızı belirlemenize yardımcı olan kullanışlı bir araçtır. Sağlıklı bir yaşam tarzı sürdürmek,"
        " kilo vermek veya kas yapmak istiyorsanız, kalori alımınızı yönetmek önemlidir."
    )


with col3 :
    st_lottie(
        calc_anim,
        speed=1,
        loop=True,
        quality="medium",
        height=400,
        width=500, )




# ---- CONTACT ----
with st.container():
    st.write("---")
    st.header("Bize ulaşın!")
    st.write("##")

    contact_form = """
    <form action="https://formsubmit.co/mamoibrahim604@gmail.com" method="POST">
        <input type="hidden" name="_captcha" value="false">
        <input type="text" name="name" placeholder="Your name" required>
        <input type="email" name="email" placeholder="Your email" required>
        <textarea name="message" placeholder="Your message here" required></textarea>
        <button type="submit">Send</button>
    </form>
    """
    left_column, right_column = st.columns(2)
    with left_column:
        st.markdown(contact_form, unsafe_allow_html=True)
    with right_column:
        st.empty()









