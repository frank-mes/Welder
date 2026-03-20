import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    """数据持久层：仅负责 Google Sheets 读写"""
    def __init__(self):
        try:
            self.conn = st.connection("gsheets", type=GSheetsConnection)
        except Exception as e:
            st.error("Secrets 配置有误，无法连接。")
            raise e

    def fetch_all(self):
        try:
            # ttl=0 保证数据实时，但在开发调试阶段可设为 1 减轻压力
            df = self.conn.read(ttl=0)
            return df if df is not None else pd.DataFrame()
        except Exception:
            return None

    def commit(self, df):
        try:
            return self.conn.update(data=df)
        except Exception as e:
            st.error(f"写入失败: {e}")
            return None
