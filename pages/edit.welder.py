import streamlit as st
from core.controller import WelderController
from core.entity import WelderEntity

st.set_page_config(page_title="编辑人员", layout="centered")

ctrl = WelderController()

# 获取跳转参数
params = st.query_params
target_id = params.get("id")

st.header("📝 编辑人员信息")

if not target_id:
    st.warning("请从主页列表点击'编辑'进入此页面。")
    # 提供手动搜索作为备选
    target_id = st.text_input("或手动输入身份证号查询：")

if target_id:
    df = ctrl.dispatch_get_list()
    # 确保数据类型一致
    target_df = df[df['id_card'].astype(str) == str(target_id)]
    
    if not target_df.empty:
        row = target_df.iloc[0]
        with st.form("edit_form"):
            c1, c2 = st.columns(2)
            with c1:
                u_name = st.text_input("姓名", value=str(row['name']))
                u_gender = st.selectbox("性别", ["男", "女"], index=0 if row['gender']=="男" else 1)
                u_id_card = st.text_input("身份证号", value=str(row['id_card']), disabled=True)
                u_stamp = st.text_input("钢印号", value=str(row['stamp_code']))
            with c2:
                u_work = st.text_input("车间", value=str(row['workshop']))
                u_team = st.text_input("产线/班组", value=str(row['team']))
                u_large = st.text_input("大证", value=str(row['cert_large']))
                u_small = st.text_input("小证", value=str(row['cert_small']))
            
            if st.form_submit_button("保存修改"):
                new_entity = WelderEntity(
                    name=u_name, gender=u_gender, id_card=u_id_card,
                    stamp_code=u_stamp, workshop=u_work, team=u_team,
                    cert_large=u_large, cert_small=u_small
                )
                ok, msg = ctrl.dispatch_update(u_id_card, new_entity)
                if ok:
                    st.success("更新成功！")
                else:
                    st.error(msg)
    else:
        st.error(f"未找到身份证号为 {target_id} 的人员信息。")
