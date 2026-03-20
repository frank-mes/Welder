# core/dao.py 建议更新为：

import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 建立连接
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        # 如果 worksheet="Sheet1" 依然报 NotFound，
        # 说明你的表格标签页可能不叫 Sheet1（可能是“工作表1”）
        # 尝试不写 worksheet 参数，让它默认打开第一个标签页
        try:
            return self.conn.read(ttl=0)
        except Exception as e:
            # 如果不带参数也失败，再尝试带参数
            return self.conn.read(worksheet="Sheet1", ttl=0)

    def update_storage(self, df: pd.DataFrame):
        try:
            # 直接更新数据
            return self.conn.update(data=df)
        except Exception as e:
            st.error(f"写入失败: {e}")
            return None
