import streamlit as st
from core.controller import WelderController
from core.entity import WelderEntity

st.title("➕ 新增人员资质")
ctrl = WelderController()

with st.form("add_form"):
    c1, c2 = st.columns(2)
    with c1:
        name = st.text_input("姓名")
        id_card = st.text_input("身份证号")
        gender = st.selectbox("性别", ["男", "女"])
        stamp_code = st.text_input("钢印号")
    with c2:
        workshop = st.text_input("车间")
        team = st.text_input("产线/班组")
        cert_large = st.text_input("大证")
        cert_small = st.text_input("小证")
    
    if st.form_submit_button("提交数据"):
        entity = WelderEntity(name=name, id_card=id_card, gender=gender, 
                              stamp_code=stamp_code, workshop=workshop, 
                              team=team, cert_large=cert_large, cert_small=cert_small)
        success, msg = ctrl.create(entity)
        if success: st.success(msg)
        else: st.error(msg)
