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
    # 核心修复点：使用绝对路径 /add_welder，并添加简单的 CSS 样式
    # 在 Streamlit Cloud 上，pages/add_welder.py 的标准路由就是 /add_welder
    st.markdown("""
        <a href="/add_welder" target="_blank" style="text-decoration: none;">
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
            # 核心修复点：编辑链接也改为绝对路径格式
            edit_url = f"/edit_welder?id={row['id_card']}"
            ce.markdown(f'<a href="{edit_url}" target="_blank" style="color:#007bff; text-decoration:none;">编辑</a>', unsafe_allow_html=True)
            
            if cd.button("删除", key=f"del_{row['id_card']}"):
                ctrl.handle_delete(row['id_card'])
                st.rerun()
else:
    st.info("💡 库中尚无数据。")
