import pandas as pd
import streamlit as st
from google.oauth2 import service_account
import gspread
import pandas as pd

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
