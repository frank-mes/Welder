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
            # 1. 打开表格
            sh = self.gc.open_by_key(self.spreadsheet_id)
            worksheet = sh.get_worksheet(0)
            
            # 2. 核心修复：处理 NaN 值，防止 JSON 报错
            # fillna("") 会将所有空值替换成空字符串
            clean_df = df.fillna("")
            
            # 3. 准备数据：包含表头 + 数据行
            # 确保转换后的列表不包含任何 numpy.nan 对象
            header = [clean_df.columns.values.tolist()]
            rows = clean_df.values.tolist()
            data = header + rows
            
            # 4. 覆盖写入
            worksheet.clear()
            worksheet.update('A1', data)
            return True
        except Exception as e:
            st.error(f"写入失败: {e}")
            return None
