import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        try:
            self.conn = st.connection("gsheets", type=GSheetsConnection)
        except Exception as e:
            st.error("无法建立 Google Sheets 连接，请检查 Secrets 配置。")
            raise e

    def fetch_all(self):
        try:
            # 增加 ttl 缓存时间（例如 1 分钟）减少请求压力，或者保持 0 实时获取
            df = self.conn.read(ttl=0)
            if df is None or df.empty:
                return self._get_empty_schema()
            return df
        except Exception as e:
            # 捕获 HTTPError 并给出友好提示
            st.error(f"读取数据失败：请确保 Google 表格已开启‘知道链接所有人可查看’权限。")
            return self._get_empty_schema()

    def _get_empty_schema(self):
        """定义标准表结构，防止 Service 层报错"""
        columns = ['id', 'name', 'gender', 'id_card', 'stamp_code', 'workshop', 'team', 'cert_large', 'cert_small']
        return pd.DataFrame(columns=columns)

    def commit(self, df):
        return self.conn.update(data=df)
