import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 建立连接
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        # 读取第一个工作表
        return self.conn.read(ttl=0)

    def update_storage(self, df: pd.DataFrame):
        # 显式指定写入行为
        try:
            # 如果你的表格里有多个 Sheet，请在这里指定 worksheet="Sheet1"
            return self.conn.update(data=df)
        except Exception as e:
            st.error(f"写入失败：请检查 Service Account 是否已获该表格的 'Editor' 权限。")
            st.code(str(e))
            return None
