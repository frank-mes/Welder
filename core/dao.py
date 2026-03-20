import streamlit as st
from streamlit_gsheets import GSheetsConnection
import pandas as pd

class WelderDAO:
    def __init__(self):
        # 建立基础连接
        self.conn = st.connection("gsheets", type=GSheetsConnection)

    def select_all(self):
        """
        读取数据。
        如果 read() 失败，利用底层 client 直接打开。
        """
        try:
            # 尝试标准读取（如果 secrets 配置正确，这通常能行）
            return self.conn.read(ttl=0)
        except Exception:
            # 【核心修复】如果 read() 报错 NotFound，手动调用底层 gspread 客户端
            # spreadsheet_id 从 secrets 中直接获取
            spreadsheet_id = st.secrets.connections.gsheets.spreadsheet
            try:
                # 使用 open_by_key 绕过名称搜索逻辑
                client = self.conn.client
                sh = client.open_by_key(spreadsheet_id)
                # 默认读取第一个工作表
                worksheet = sh.get_worksheet(0)
                data = worksheet.get_all_records()
                return pd.DataFrame(data)
            except Exception as final_e:
                st.error("无法通过 ID 定位电子表格。")
                st.info("请确认：1. Spreadsheet ID 正确；2. 已分享 Editor 权限给服务账号。")
                raise final_e

    def update_storage(self, df: pd.DataFrame):
        """
        写入数据。
        """
        try:
            # 填补空值，避免 JSON 序列化错误
            df = df.fillna("")
            return self.conn.update(data=df)
        except Exception as e:
            st.error(f"写入失败: {e}")
            return None
