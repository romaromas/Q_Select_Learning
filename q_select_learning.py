import streamlit as st

st.title("Q Select Learning")

budget = st.slider("予算を教えてください", 0, 100000, 2000, step=1000)
budget = st.slider("かけられる時間を教えてください[時間]", 10, 10000, 100, step=10)
blood_type = st.selectbox("血液型を教えてください", ("A", "B", "AB", "O"))
toeic_level = st.selectbox("TOEICレベルを教えてください", ("0", "1", "2", "3", "4", "5", "6"))
constellation = st.selectbox(
    "あなたの星座を教えてください",
    (
        "おひつじ座（牡羊座、Aries）",
        "おうし座（牡牛座、Taurus）",
        "ふたご座（双子座、Gemini）",
        "かに座（蟹座、Cancer）",
        "しし座（獅子座、Leo）",
        "おとめ座（乙女座、Virgo）",
        "てんびん座（天秤座、Libra）",
        "さそり座（蠍座、Scorpius）",
        "いて座（射手座、Sagittarius）",
        "やぎ座（山羊座、Capricornus）",
        "みずがめ座（水瓶座、Aquarius）",
        "うお座（魚座、Pisces）",
    ),
)
