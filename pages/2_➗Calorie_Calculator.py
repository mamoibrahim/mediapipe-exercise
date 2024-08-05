import streamlit as st
import json
from streamlit_lottie import st_lottie

# Faaliyet Çarpanı Sözlüğü (activity_multiplier dictionary)
faaliyet_carpani = {
    "Hareketsiz": 1.2,
    "Hafif Hareketli": 1.375,
    "Orta Derecede Hareketli": 1.55,
    "Çok Hareketli": 1.725,
    "Aşırı Hareketli": 1.9,
}

# Kalori Ayarlama Sözlüğü (calorie_adjustment dictionary)
kalori_ayarlama = {
    "Koruma": 0,
    "Kilo Verme": -500,
    "Kas Kazanımı": +300,
}


def bazal_metabolik_hiz(agirlik, boy, yas):
    """Mifflin St Jeor denklemini kullanarak Bazal Metabolik Hızı (BMH) hesaplar."""
    bmh = 10 * agirlik + 6.25 * boy - 5 * yas + 5
    return bmh


def günlük_kalori_ihtiyacı(bmh, faaliyet_seviyesi, hedef):
    """BMH, faaliyet seviyesi ve hedefe göre günlük kalori ihtiyacını hesaplar."""
    return bmh * faaliyet_carpani[faaliyet_seviyesi] + kalori_ayarlama[hedef]


def load_lottiefile(filepath:str):
    with open(filepath, "r") as f:
        return json.load(f)

calc_anim = load_lottiefile("animations/Health.json")


col1, col2 , col3  = st.columns(3)
with col1:
    st.title("Kalori Hesaplayıcı ")
    st.subheader("Kalori hesaplayıcı, bireylerin günlük enerji ihtiyaçlarını belirlemelerine yardımcı olan bir araçtır. Bu hesaplayıcı, kişinin yaş, cinsiyet, boy, kilo, fiziksel aktivite seviyesi ve hedeflerine göre günlük kalori ihtiyacını belirler.")


with col3:
    st_lottie(
        calc_anim,
        speed=1,
        loop=True,
        quality="high",
        height=300,
        width=400,
    )
st.write("---")


# Kullanıcı girdisi konteyner içerisinde
with st.container():
    st.markdown("<h2 style='text-align: center;'>Bilgilerinizi Girin</h2>", unsafe_allow_html=True)
    col1, col2 = st.columns(2)
    agirlik = col1.number_input("Ağırlık ⏲️ (kg):")
    boy = col2.number_input("Boy 📏 (cm):")
    yas = st.number_input("Yaş 📅 (yıl):")
    faaliyet_seviyesi = st.selectbox("Faaliyet Seviyesi🏃:", list(faaliyet_carpani.keys()))
    hedef = st.selectbox("Hedef:", ("Koruma", "Kilo Verme", "Kas Kazanımı"))

# BMH'yi konteyner dışında hesapla
bmh = bazal_metabolik_hiz(agirlik, boy, yas)

# Sonuçlar için konteyner, kenar boşluğu ve margin ile
with st.container():
    st.markdown("<h2 style='text-align: center;'>Sonuçlar</h2>", unsafe_allow_html=True)
    st.write("---")

    if bmh is not None:  # Kullanıcı bilgi girdiyse
        gunluk_kalori = günlük_kalori_ihtiyacı(bmh, faaliyet_seviyesi, hedef)

        # Sonuçları göster
        st.write("Bazal Metabolik Hız (BMH):", round(bmh), " kalori")
        st.write(f"'{hedef}' için Tahmini Günlük Kalori İhtiyacı:", round(gunluk_kalori), " kalori")

        # Kalori ayarlamaları hakkında bilgi mesajı (isteğe bağlı)
        if hedef != "Koruma":
            ayarlama_metni = f"'{hedef}' için günlük {kalori_ayarlama[hedef]} kalori ayarlamasıdır"
            st.write(ayarlama_metni)
    else:
        st.warning("Devam etmek için lütfen bilgilerinizi girin.")

