import streamlit as st
from core.controller import WelderController

# 1. 基础配置
st.set_page_config(page_title="焊工管理系统", layout="wide")

# 2. 强制隐藏左侧菜单栏
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

ctrl = WelderController()
st.title("👨‍🏭 焊工人员资质管理系统")

# 3. 顶部操作区
c1, c2, c3 = st.columns([1, 1, 4])
with c1:
    # 修复点：改用相对路径 ./add_welder
    st.markdown("""
        <a href="./add_welder" target="_blank">
            <button style="width:100%;height:38px;background-color:#28a745;color:white;border:none;border-radius:4px;cursor:pointer;">
                ➕ 新增人员
            </button>
        </a>
    """, unsafe_allow_html=True)

with c3:
    keyword = st.text_input("", placeholder="搜索姓名、身份证或钢印号...", label_visibility="collapsed")

# 4. 获取数据
df = ctrl.handle_get(keyword)

# 5. 渲染列表
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
            # 修复点：改用相对路径 ./edit_welder 并确保参数格式正确
            edit_link = f"./edit_welder?id={row['id_card']}"
            ce.markdown(f'<a href="{edit_link}" target="_blank" style="text-decoration:none;color:#007bff;">编辑</a>', unsafe_allow_html=True)
            
            if cd.button("删除", key=f"del_{row['id_card']}"):
                ctrl.handle_delete(row['id_card'])
                st.rerun()
else:
    st.info("💡 库中尚无数据或未找到匹配项。")
