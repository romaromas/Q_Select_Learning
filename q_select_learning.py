import streamlit as st
import pandas as pd
from google.oauth2 import service_account
import gspread
from roma import func as rfc
from plascript import functions as pfc


st.title("Q Select Learning")

K = st.slider("選択したい教材数", 1, 5, 3, step=1)
# budget = st.slider("予算を教えてください", 0, 100000, 2000, step=1000)
# budget = st.slider("かけられる時間を教えてください[時間]", 10, 10000, 100, step=10)
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

num_reads = st.number_input("反復回数", min_value=10, max_value=1000)

df_courseware = rfc.get_courseware()


if st.button("SELECT"):
    # 観測点の座標。要素数はNparaと合わせる
    # s = [0, 0, 0]  # 観測点の座標
    s = rfc.gen_vec(blood_type, toeic_level, constellation)  # 観測点の座標を計算

    Nmater = len(df_courseware)  # 教材の数

    # 罰則項の作成
    N = Nmater
    # 選択する教材数
    # K = 3

    # サンプル教材作成
    # TODO:スプレッドシートから読み込む
    coursewares = pfc.make_sample()
    # パラメータ配列作成
    mat = pfc.courseware2matrix(coursewares)

    dist_mat, dist = pfc.make_dist_mat(mat, s)
    QUBO = pfc.create_penalty(N, K)

    result = pfc.sample(QUBO, num_reads)

    dist_df = pd.DataFrame({"距離": dist})
    st.write(dist_df)

    selected = []
    for key, value in result.items():
        if value == 1:
            # selected.append(key)
            selected.append(df_courseware.loc[key]["name"])
    print(selected)

    st.write("この教材がおすすめ！")
    for i in selected:
        st.write("・", i)
