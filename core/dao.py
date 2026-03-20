import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 建立连接
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        """
        读取数据。如果 Sheet1 不存在，则尝试不带参数读取第一个工作表。
        """
        try:
            # 方案 A：显式指定工作表名称（请确保你的表格底部标签确实叫 Sheet1）
            return self.conn.read(worksheet="Sheet1", ttl=0)
        except Exception:
            try:
                # 方案 B：如果不叫 Sheet1，则尝试默认读取第一个工作表
                return self.conn.read(ttl=0)
            except Exception as e:
                st.error("无法找到指定的电子表格或工作表。")
                st.info(f"请检查服务账号是否已获授权，且 Spreadsheet ID 正确。")
                raise e

    def update_storage(self, df: pd.DataFrame):
        """
        更新数据到云端
        """
        try:
            # 强制覆盖写入
            return self.conn.update(worksheet="Sheet1", data=df)
        except Exception as e:
            # 如果写入失败，尝试不带 worksheet 参数自动匹配
            try:
                return self.conn.update(data=df)
            except Exception as final_error:
                st.error(f"写入失败: {final_error}")
                return None
