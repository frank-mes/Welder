import streamlit as st
from core.controller import WelderController
from core.entity import WelderEntity

st.set_page_config(page_title="编辑人员", layout="centered")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

ctrl = WelderController()
# 获取 URL 参数
params = st.query_params
tid = params.get("id")

st.header(f"📝 编辑人员信息")

if tid:
    df = ctrl.handle_get()
    target = df[df['id_card'].astype(str) == str(tid)]
    
    if not target.empty:
        row = target.iloc[0]
        with st.form("edit_form"):
            c1, c2 = st.columns(2)
            with c1:
                u_name = st.text_input("姓名", value=str(row['name']))
                u_gender = st.selectbox("性别", ["男", "女"], index=0 if row['gender']=="男" else 1)
                u_id = st.text_input("身份证号", value=str(row['id_card']), disabled=True)
                u_stamp = st.text_input("钢印号", value=str(row['stamp_code']))
            with c2:
                u_work = st.text_input("车间", value=str(row['workshop']))
                u_team = st.text_input("班组", value=str(row['team']))
                u_l = st.text_input("大证", value=str(row['cert_large']))
                u_s = st.text_input("小证", value=str(row['cert_small']))
            
            if st.form_submit_button("更新数据"):
                updated = WelderEntity(u_name, u_gender, u_id, u_stamp, u_work, u_team, u_l, u_s)
                ok, msg = ctrl.handle_edit(u_id, updated)
                if ok: st.success("更新成功！")
                else: st.error(msg)
    else:
        st.error("查无此人")
else:
    st.warning("请从主页列表进入")
