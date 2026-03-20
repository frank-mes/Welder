import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 建立连接：它会自动从 .streamlit/secrets.toml 中读取 [connections.gsheets] 配置
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        # ttl=0 强制跳过缓存，确保每次读取都是云端最新数据
        # 显式指定 worksheet 保证读取位置准确
        return self.conn.read(worksheet="Sheet1", ttl=0)

    def update_storage(self, df: pd.DataFrame):
        """
        核心写入方法：将最新的 DataFrame 覆盖写入到 Google Sheets
        """
        try:
            # 关键修复：显式指定 worksheet="Sheet1"
            # 这样可以强制 API 锁定到具体工作表，避免 UnsupportedOperationError
            return self.conn.update(worksheet="Sheet1", data=df)
        except Exception as e:
            st.error("🚨 写入 Google Sheets 失败！")
            with st.expander("点击查看错误详情"):
                st.write("1. 请确认 Service Account 邮箱已在表格中设为 'Editor' 权限。")
                st.write("2. 请确认 .streamlit/secrets.toml 中的 spreadsheet ID 正确且不含 URL 冗余。")
                st.code(str(e))
            return None
