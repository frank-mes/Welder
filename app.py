import streamlit as st
from core.controller import WelderController

st.set_page_config(page_title="焊工管理系统", layout="wide")
ctrl = WelderController()

st.title("👨‍🏭 焊工资质管理中心")
st.markdown("---")

df = ctrl.get_list()
st.subheader(f"当前在册人员 ({len(df)} 人)")
st.dataframe(df, use_container_width=True, hide_index=True)

if st.button("🔄 刷新数据"):
    st.rerun()
