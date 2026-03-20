import streamlit as st
from core.entity import WelderEntity
from core.controller import WelderController

st.set_page_config(page_title="新增人员", layout="centered")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

st.header("➕ 录入新焊工档案")
ctrl = WelderController()

with st.form("add_form", clear_on_submit=True):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("姓名")
        gender = st.selectbox("性别", ["男", "女"])
        id_card = st.text_input("身份证号")
        stamp_code = st.text_input("钢印号")
    with c2:
        workshop = st.text_input("车间")
        team = st.text_input("产线/班组")
        cert_large = st.text_input("大证")
        cert_small = st.text_input("小证")
    
    if st.form_submit_button("提交并保存"):
        if not name or not id_card:
            st.error("姓名和身份证为必填项")
        else:
            new_one = WelderEntity(name, gender, id_card, stamp_code, workshop, team, cert_large, cert_small)
            ok, msg = ctrl.handle_add(new_one)
            if ok: st.success(msg)
            else: st.error(msg)
