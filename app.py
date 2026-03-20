import streamlit as st
from core.controller import WelderController

# 1. 基础配置
st.set_page_config(page_title="焊工管理系统", layout="wide")

# 2. 强制隐藏左侧菜单栏
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

# 定义基础 URL（请根据你的部署地址微调）
BASE_URL = "https://welder-uuvjqqkl6banajtz3b9ri4.streamlit.app"

ctrl = WelderController()
st.title("👨‍🏭 焊工人员资质管理系统")

# 3. 顶部操作区
c1, c2, c3 = st.columns([1, 1, 4])
with c1:
    # 修复点：直接指向全路径，强制浏览器寻找该资源
    st.markdown(f"""
        <a href="{BASE_URL}/add_welder" target="_blank" style="text-decoration: none;">
            <div style="
                background-color: #28a745;
                color: white;
                padding: 10px;
                text-align: center;
                border-radius: 5px;
                cursor: pointer;
                font-weight: bold;
                width: 150px;
            ">
                ➕ 新增人员
            </div>
        </a>
    """, unsafe_allow_html=True)

with c3:
    keyword = st.text_input("", placeholder="搜索姓名、身份证或钢印号...", label_visibility="collapsed")

# 4. 获取数据并渲染列表
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
            # 修复点：全路径 + Query Params
            edit_url = f"{BASE_URL}/edit_welder?id={row['id_card']}"
            ce.markdown(f'<a href="{edit_url}" target="_blank" style="color:#007bff; text-decoration:none;">编辑</a>', unsafe_allow_html=True)
            
            if cd.button("删除", key=f"del_{row['id_card']}"):
                ctrl.handle_delete(row['id_card'])
                st.rerun()
