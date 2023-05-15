import os
from os.path import join, dirname
from dotenv import load_dotenv
import pandas as pd


def get_courseware() -> pd.DataFrame:
    """google spred sheetから教材表を読み込む

    Args:
        None

    Return:
        df(pd.DataFrame):教材の表
    """
    # dotenv_path = r"D:\insiders\Q_Select_Learning\.env"
    dotenv_path = join(dirname(__file__), "../.env")

    load_dotenv(verbose=True)

    load_dotenv(dotenv_path)

    GOOGLE_APPLICATION_CREDENTIALS = os.environ.get("GOOGLE_APPLICATION_CREDENTIALS")
    SPREDSHEET_KEY = os.environ.get("SPREDSHEET_KEY")

    from google.oauth2 import service_account
    import gspread
    import google.auth

    scopes = [
        "https://www.googleapis.com/auth/spreadsheets",
        "https://www.googleapis.com/auth/drive",
    ]

    # Credentials 情報を取得 デフォルトではGOOGLE_APPLICATION_CREDENTIALSに設定されてるJSONファイルを使用している
    credentials, project = google.auth.default(scopes=scopes)

    # クレデンシャルを使用してGoogleAPIにログイン
    gc = gspread.authorize(credentials)

    spreadsheet = gc.open_by_key(SPREDSHEET_KEY)

    df = pd.DataFrame(
        spreadsheet.sheet1.get_all_values()[1:],
        columns=spreadsheet.sheet1.get_all_values()[0],
    )
    return df
