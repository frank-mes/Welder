import streamlit as st
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

class WelderDAO:
    def __init__(self):
        # 1. 直接从 secrets 加载凭据，绕过所有中间件
        scope = [
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/drive'
        ]
        conf = st.secrets.connections.gsheets
        
        # 构建原生凭据对象
        creds = Credentials.from_service_account_info({
            "type": conf.type,
            "project_id": conf.project_id,
            "private_key_id": conf.private_key_id,
            "private_key": conf.private_key,
            "client_email": conf.client_email,
            "client_id": conf.client_id,
            "auth_uri": conf.auth_uri,
            "token_uri": conf.token_uri,
            "auth_provider_x509_cert_url": conf.auth_provider_x509_cert_url,
            "client_x509_cert_url": conf.client_x509_cert_url
        }, scopes=scope)
        
        self.gc = gspread.authorize(creds)
        self.spreadsheet_id = conf.spreadsheet

    def select_all(self):
        try:
            # 2. 尝试用最原始的 open_by_key 打开
            sh = self.gc.open_by_key(self.spreadsheet_id)
            worksheet = sh.get_worksheet(0)
            data = worksheet.get_all_records()
            return pd.DataFrame(data)
        except Exception as e:
            # 3. 如果还是找不到，打印出该账号目前能看到的“所有表格”
            st.error("🚨 还是找不到！系统诊断如下：")
            visible_sheets = [s.title for s in self.gc.openall()]
            st.write(f"当前服务账号能看到的表格列表: {visible_sheets}")
            st.write(f"正在寻找的 ID: {self.spreadsheet_id}")
            st.code(str(e))
            return pd.DataFrame()

    def update_storage(self, df: pd.DataFrame):
        try:
            sh = self.gc.open_by_key(self.spreadsheet_id)
            worksheet = sh.get_worksheet(0)
            # 清除旧数据并写入新数据
            worksheet.clear()
            # 将 DataFrame 转换为带表头的列表
            data = [df.columns.values.tolist()] + df.values.tolist()
            worksheet.update('A1', data)
            return True
        except Exception as e:
            st.error(f"写入失败: {e}")
            return None
