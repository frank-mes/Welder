import streamlit as st
from core.controller import WelderController

st.set_page_config(page_title="焊工管理系统", layout="wide")
ctrl = WelderController()

st.title("👨‍🏭 焊工人员资质管理系统")
st.info("大厂经典架构：Controller-Service-DAO-Entity")

df = ctrl.get_all()
st.subheader("人员数据看板")
st.dataframe(df, use_container_width=True, hide_index=True)
