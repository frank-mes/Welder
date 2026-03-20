import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd
import gspread

class WelderDAO:
    def __init__(self):
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        try:
            # 1. 尝试标准读取
            return self.conn.read(ttl=0)
        except Exception:
            try:
                # 2. 深度修复：直接利用 secrets 里的凭据手动构建 client
                # 这样可以绕过 st.connection 可能存在的配置读取 Bug
                conf = st.secrets.connections.gsheets
                spreadsheet_id = conf.spreadsheet
                
                # 获取底层 client 并直接通过 ID 打开
                sh = self.conn.client.open_by_key(spreadsheet_id)
                worksheet = sh.get_worksheet(0) # 打开第一个标签页
                
                records = worksheet.get_all_records()
                return pd.DataFrame(records)
            except Exception as e:
                st.error("🚨 致命错误：Google 依然报告找不到该表格。")
                st.info("请检查 Google Cloud 是否同时开启了 Sheets 和 Drive API，并确认表格已分享给 Service Account 邮箱。")
                return pd.DataFrame()

    def update_storage(self, df: pd.DataFrame):
        try:
            # 预处理：将所有 NaN 转换为字符串，防止 API 报错
            df = df.fillna("")
            return self.conn.update(data=df)
        except Exception as e:
            st.error(f"保存失败: {e}")
            return None
