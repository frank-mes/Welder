import streamlit as st
from core.entity import WelderEntity
from core.controller import WelderController

# 必须位于首行，且没有其他逻辑干扰
st.set_page_config(page_title="新增人员", layout="centered")

# 注入 CSS 隐藏侧边栏
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

st.header("➕ 录入新焊工档案")
ctrl = WelderController()

with st.form("add_form", clear_on_submit=True):
    # (表单内容...)
    name = st.text_input("姓名")
    id_card = st.text_input("身份证号")
    # ...
    submit_btn = st.form_submit_button("保存")

if submit_btn:
    # (处理逻辑...)
    pass
