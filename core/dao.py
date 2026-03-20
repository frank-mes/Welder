import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 自动识别 secrets 中的 service_account 进行读写授权
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def update_storage(self):
        return self.conn.read(ttl=0)

    def save_all(self, df: pd.DataFrame):
        return self.conn.update(data=df)
