import streamlit as st
from streamlit_gsheets import GSheetsConnection

class WelderDAO:
    """数据持久层：只负责与 Google Sheets 交换原始数据"""
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def fetch_all(self):
        # ttl=0 禁用缓存，保证大厂业务数据的实时性
        return self.conn.read(ttl=0)

    def commit(self, df):
        return self.conn.update(data=df)
