import streamlit as st
from core.entity import WelderEntity
from core.controller import WelderController

# 必须是页面第一行代码
st.set_page_config(page_title="新增人员", layout="centered")

ctrl = WelderController()

st.header("➕ 录入新焊工资质")

with st.form("add_form", clear_on_submit=True):
    col1, col2 = st.columns(2)
    with col1:
        name = st.text_input("姓名")
        gender = st.selectbox("性别", ["男", "女"])
        id_card = st.text_input("身份证号")
        stamp_code = st.text_input("钢印号")
    with col2:
        workshop = st.text_input("车间")
        team = st.text_input("产线/班组")
        cert_large = st.text_input("大证编号")
        cert_small = st.text_input("小证编号")
    
    submit_btn = st.form_submit_button("保存并入库")

if submit_btn:
    if not name or not id_card:
        st.error("姓名和身份证号为必填项！")
    else:
        # 严格对应 Entity 构造函数
        entity = WelderEntity(
            name=name, 
            gender=gender, 
            id_card=id_card, 
            stamp_code=stamp_code, 
            workshop=workshop, 
            team=team, 
            cert_large=cert_large, 
            cert_small=cert_small
        )
        success, msg = ctrl.dispatch_add(entity)
        if success:
            st.success(msg)
        else:
            st.error(msg)
