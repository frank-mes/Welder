import streamlit as st
from core.controller import WelderController

st.set_page_config(page_title="焊工管理系统", layout="wide")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

ctrl = WelderController()
  # 创建了一个名叫 WelderController 的类的实例（对象），并把这个对象赋值给了变量 ctrl
st.title("👨‍🏭 焊工人员资质管理系统")
  # st 是 Streamlit 的核心模块

c1, c2, c3 = st.columns([1, 1, 4])
with c1:
    # 修复：直接使用相对路径 /add_welder，并对应 pages/add_welder.py
    st.markdown("""
        <a href="/add_welder" target="_blank" style="text-decoration: none;">
            <div style="background-color:#28a745;color:white;padding:10px;text-align:center;border-radius:5px;cursor:pointer;font-weight:bold;width:150px;">
                ➕ 新增人员
            </div>
        </a>
    """, unsafe_allow_html=True)

with c3:
    keyword = st.text_input("", placeholder="搜索姓名、身份证或钢印号...", label_visibility="collapsed")

df = ctrl.handle_get(keyword)

if not df.empty:
    cols = st.columns([1, 1, 2, 1, 1, 1, 1, 1, 2])
    labels = ["姓名", "性别", "身份证", "钢印号", "车间", "班组", "大证", "小证", "操作栏"]
    for col, label in zip(cols, labels):
        col.write(f"**{label}**")
    
    for _, row in df.iterrows():
        c = st.columns([1, 1, 2, 1, 1, 1, 1, 1, 2])
        c[0].write(row['name'])
        c[1].write(row['gender'])
        c[2].write(row['id_card'])
        c[3].write(row['stamp_code'])
        c[4].write(row['workshop'])
        c[5].write(row['team'])
        c[6].write(row['cert_large'])
        c[7].write(row['cert_small'])
        
        with c[8]:
            ce, cd = st.columns(2)
            # 修复：对应 pages/edit_welder.py
            edit_url = f"/edit_welder?id={row['id_card']}"
            ce.markdown(f'<a href="{edit_url}" target="_blank" style="color:#007bff; text-decoration:none;">编辑</a>', unsafe_allow_html=True)
            
            if cd.button("删除", key=f"del_{row['id_card']}"):
                ctrl.handle_delete(row['id_card'])
                st.rerun()
