import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 自动识别 secrets 中的 service_account 进行读写授权
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        # ttl=0 确保 CRUD 后立即读取最新数据
        return self.conn.read(ttl=0)

    def update_storage(self, df: pd.DataFrame):
        # 将原 save_all 改名为 update_storage，与 Service 层对接
        return self.conn.update(data=df)
