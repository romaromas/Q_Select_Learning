import pandas as pd
import streamlit as st
from google.oauth2 import service_account
from sklearn.preprocessing import MinMaxScaler
import gspread
import pandas as pd
import numpy as np

datarow = 79


def get_courseware() -> pd.DataFrame:
    """google spred sheetから教材表を読み込む

    Args:
        None

    Return:
        df(pd.DataFrame):教材の表
    """

    # スプレッドシートの認証
    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]
    credentials = service_account.Credentials.from_service_account_info(
        st.secrets["gcp_service_account"], scopes=scopes
    )
    gc = gspread.authorize(credentials)
    # スプレッドシートからデータ取得
    SPREDSHEET_KEY = st.secrets.SPREDSHEET_KEY.key  # スプレッドシートのキー
    spreadsheet = gc.open_by_key(SPREDSHEET_KEY)

    df = pd.DataFrame(
        spreadsheet.sheet1.get_all_values()[1:],
        columns=spreadsheet.sheet1.get_all_values()[0],
    ).iloc[:datarow, :14]

    return df


def gen_cwvec(df: pd.DataFrame) -> pd.DataFrame:
    """教材の辞書からパラメータをだけのarrayを作る

    Args:
        df(pd.DataFrame):教材リストのデータフレーム

    Returns:
        df_vec(pd.DataFrame):パラメータ数3のデータフレーム
    """
    scaler = MinMaxScaler()
    # 空文字対策
    df[["ページ数", "時間[s]"]] = df[["ページ数", "時間[s]"]].replace("", np.nan).fillna(0)

    df["level_norm"] = scaler.fit_transform(df[["TOEICレベル"]])
    df["commentcount_norm"] = scaler.fit_transform(df[["口コミ数"]])
    df["page_norm"] = scaler.fit_transform(df[["ページ数"]])
    df["time_norm"] = scaler.fit_transform(df[["時間[s]"]])

    df["weight"] = df["page_norm"] + df["time_norm"]
    df_vec = df[["level_norm", "commentcount_norm", "weight"]]
    return df_vec


def courseware2matrix(coursewares: pd.DataFrame, Npara: int) -> np.ndarray:
    """教材の辞書からパラメータをだけのarrayを作る

    Args:
        coursewares(pd.DataFrame):教材リスト

    Returns:
        mat(np.array):パラメータ配列
    """
    Nmater = len(coursewares)
    mat = np.zeros([Nmater, Npara])
    for i in range(Nmater):
        mat[i, :] = coursewares[i : i + 1]
    # print(mat)
    return mat


# def get_courseware() -> pd.DataFrame:
#     """google spred sheetから教材表を読み込む

#     Args:
#         None

#     Return:
#         df(pd.DataFrame):教材の表
#     """

#     # dotenv_path = r"D:\insiders\Q_Select_Learning\.env"
#     dotenv_path = join(dirname(__file__), "../.env")

#     load_dotenv(verbose=True)

#     load_dotenv(dotenv_path)

#     GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
#     SPREDSHEET_KEY = os.environ.get("SPREDSHEET_KEY")

#     from google.oauth2 import service_account
#     import gspread
#     import google.auth

#     scopes = [
#         "https://www.googleapis.com/auth/spreadsheets",
#         "https://www.googleapis.com/auth/drive",
#     ]

#     # Credentials 情報を取得 デフォルトではGOOGLE_APPLICATION_CREDENTIALSに設定されてるJSONファイルを使用している
#     credentials, project = google.auth.default(scopes=scopes)

#     # クレデンシャルを使用してGoogleAPIにログイン
#     gc = gspread.authorize(credentials)

#     spreadsheet = gc.open_by_key(SPREDSHEET_KEY)

#     df = pd.DataFrame(
#         spreadsheet.sheet1.get_all_values()[1:],
#         columns=spreadsheet.sheet1.get_all_values()[0],
#     ).iloc[:datarow, :14]
#     return df


def gen_vec(blood_type: str, toeic_level: str, constellation: str):
    bt = {"A": 0, "B": 1, "AB": 2, "O": 3}
    const = {
        "おひつじ座（牡羊座、Aries）": 0,
        "おうし座（牡牛座、Taurus）": 1,
        "ふたご座（双子座、Gemini）": 2,
        "かに座（蟹座、Cancer）": 3,
        "しし座（獅子座、Leo）": 4,
        "おとめ座（乙女座、Virgo）": 5,
        "てんびん座（天秤座、Libra）": 6,
        "さそり座（蠍座、Scorpius）": 7,
        "いて座（射手座、Sagittarius）": 8,
        "やぎ座（山羊座、Capricornus）": 9,
        "みずがめ座（水瓶座、Aquarius）": 10,
        "うお座（魚座、Pisces）": 11,
    }
    level = int(toeic_level)
    return [bt[blood_type] / 3, level / 6, const[constellation] / 11]


def make_dist_mat(mat, s, Nmater):
    """教材パラメータから対角行列をつくる

    Args:
        mat(np.ndarray):教材パラメータ配列
        s(np.ndarray):利用者の座標
        Nmater:

    Returns:
        dist_mat(np.array):パラメータの対角行列
        dist(dict):観測点からの距離のリスト

    """
    dist = {}
    # for i in range(Nmater):
    #     dist[i] = euclidean_distance(s, mat[i, :])
    #     print(dist[i])

    for i, li in enumerate(mat):
        dist[i] = np.linalg.norm(li - s)

    # distを対角行列化
    new_dist = np.array([])  # 新しい配列を初期化

    for i in range(Nmater):
        new_dist = np.append(new_dist, dist[i])
    dist = new_dist
    dist_mat = np.diag(dist)
    print(dist_mat)

    return dist_mat, dist
