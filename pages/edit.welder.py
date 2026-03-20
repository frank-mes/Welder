import streamlit as st
from core.controller import WelderController
from core.entity import WelderEntity

st.set_page_config(page_title="编辑人员", layout="centered")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

ctrl = WelderController()

# 修复点：增强参数读取的兼容性
params = st.query_params
tid = params.get("id") or params.get_all("id")[0] if "id" in params else None

st.header("📝 编辑人员信息")

if tid:
    df = ctrl.handle_get()
    # 强制转换为字符串比对，避免 int/str 不匹配导致的 404
    target = df[df['id_card'].astype(str) == str(tid)]
    
    if not target.empty:
        row = target.iloc[0]
        with st.form("edit_form"):
            c1, c2 = st.columns(2)
            with c1:
                u_name = st.text_input("姓名", value=str(row['name']))
                u_gender = st.selectbox("性别", ["男", "女"], index=0 if str(row['gender'])=="男" else 1)
                u_id = st.text_input("身份证号", value=str(row['id_card']), disabled=True)
                u_stamp = st.text_input("钢印号", value=str(row['stamp_code']))
            with c2:
                u_work = st.text_input("车间", value=str(row['workshop']))
                u_team = st.text_input("班组", value=str(row['team']))
                u_l = st.text_input("大证", value=str(row['cert_large']))
                u_s = st.text_input("小证", value=str(row['cert_small']))
            
            if st.form_submit_button("更新并保存"):
                updated = WelderEntity(
                    name=u_name, gender=u_gender, id_card=u_id, 
                    stamp_code=u_stamp, workshop=u_work, 
                    team=u_team, cert_large=u_l, cert_small=u_s
                )
                ok, msg = ctrl.handle_edit(u_id, updated)
                if ok:
                    st.success("✅ 更新成功！您可以关闭此标签页并刷新主页。")
                else:
                    st.error(msg)
    else:
        st.error(f"❌ 未找到身份证号为 {tid} 的记录")
else:
    st.warning("⚠️ 请从主页列表点击'编辑'进入，或缺少必要参数 ID。")
