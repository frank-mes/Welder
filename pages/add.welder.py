import streamlit as st
from core.entity import WelderEntity
from core.controller import WelderController

st.set_page_config(page_title="新增人员")
ctrl = WelderController()

st.header("➕ 录入新焊工资质")
with st.form("add_form", clear_on_submit=True):
    # 表单布局... (此处同之前新增代码)
    name = st.text_input("姓名")
    id_card = st.text_input("身份证号")
    # ...其他字段...
    if st.form_submit_button("保存并入库"):
        entity = WelderEntity(name=name, id_card=id_card, ...) 
        success, msg = ctrl.dispatch_add(entity)
        if success: st.success(msg)
        else: st.error(msg)
