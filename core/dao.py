import streamlit as st
from streamlit_gsheets import GSheetsConnection

class WelderDAO:
    def __init__(self):
        # 初始化连接
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        # ttl=0 确保不使用缓存，实时获取最新数据
        return self.conn.read(ttl=0)

    def update_sheet(self, df):
        return self.conn.update(data=df)
