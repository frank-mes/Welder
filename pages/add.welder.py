import streamlit as st
from core.entity import WelderEntity
from core.controller import WelderController

st.title("➕ 新增焊工信息")
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
        cert_large = st.text_input("大证编号")
        cert_small = st.text_input("小证编号")
    
    if st.form_submit_button("提交存入云端数据库"):
        new_data = WelderEntity(
            name=name, gender=gender, id_card=id_card, 
            stamp_code=stamp_code, workshop=workshop, 
            team=team, cert_large=cert_large, cert_small=cert_small
        )
        success, msg = ctrl.add_welder(new_data)
        if success: st.success(msg)
        else: st.error(msg)
