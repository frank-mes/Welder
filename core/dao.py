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
            # 这里的 spreadsheet 参数会自动寻找 secrets 里的配置
            df = self.conn.read(ttl=0)
            
            if df is None:
                st.error("❌ 数据库连接返回了 None，请检查 Secrets 中的 URL 是否正确。")
                return pd.DataFrame()
                
            return df
        except Exception as e:
            # 捕获具体的 HTTP 错误代码
            st.error(f"⚠️ 无法读取表格。常见原因：权限未设为'知道链接的所有人'。具体报错：{e}")
            return pd.DataFrame()

    def commit(self, df):
        try:
            return self.conn.update(data=df)
        except Exception as e:
            st.error(f"写入失败: {e}")
            return None
