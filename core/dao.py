import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 建立连接时，明确告诉它我们要用 secrets 里的配置
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        # 如果 read() 报错，尝试不带任何参数，
        # 它会默认读取 spreadsheet 定义的第一个工作表
        try:
            return self.conn.read(ttl=0)
        except Exception:
            # 如果上面失败，手动指定 URL 模式绕过某些版本的 Bug
            # 注意：这里的 spreadsheet 是从 secrets 自动获取的 ID
            return self.conn.read(worksheet="Sheet1", ttl=0)

    def update_storage(self, df: pd.DataFrame):
        try:
            # 确保 data 是 DataFrame 格式
            return self.conn.update(data=df)
        except Exception as e:
            st.error(f"写入失败: {e}")
            return None
