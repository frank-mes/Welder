import streamlit as st
from core.controller import WelderController

st.set_page_config(page_title="焊工管理系统", layout="wide")
ctrl = WelderController()

st.title("👨‍🏭 焊工人员资质管理系统")
st.info("大厂经典架构：Controller-Service-DAO-Entity")

df = ctrl.get_all()
st.subheader("人员数据看板")
st.dataframe(df, use_container_width=True, hide_index=True)

# 临时插入 app.py 进行测试
try:
    df = ctrl.get_all()
except Exception as e:
    st.error(f"连接数据库失败，请检查 Google Sheets 共享设置。错误详情: {e}")
    st.stop() # 停止运行后续代码
