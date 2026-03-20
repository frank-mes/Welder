import streamlit as st
from core.controller import WelderController

# 配置页面与隐藏侧边栏
st.set_page_config(page_title="焊工管理系统", layout="wide")
st.markdown("<style>[data-testid='stSidebarNav'] {display: none;}</style>", unsafe_allow_html=True)

ctrl = WelderController()
st.title("👨‍🏭 焊工人员资质管理系统")

# 顶部导航与搜索
c1, c2, c3 = st.columns([1, 1, 4])
with c1:
    # 跳转至 pages/add_welder.py
    st.markdown('<a href="/add_welder" target="_blank"><button style="width:100%;height:38px;background-color:#28a745;color:white;border:none;border-radius:4px;cursor:pointer;">➕ 新增人员</button></a>', unsafe_allow_html=True)

with c3:
    keyword = st.text_input("", placeholder="搜索姓名、身份证或钢印号...", label_visibility="collapsed")

df = ctrl.handle_get(keyword)

# 渲染列表
if not df.empty:
    # 表头
    cols = st.columns([1, 1, 2, 1, 1, 1, 1, 1, 2])
    labels = ["姓名", "性别", "身份证", "钢印号", "车间", "班组", "大证", "小证", "操作栏"]
    for col, label in zip(cols, labels):
        col.write(f"**{label}**")
    
    # 行数据
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
        
        # 操作逻辑
        with c[8]:
            ce, cd = st.columns(2)
            # 跳转至 pages/edit_welder.py
            ce.markdown(f'<a href="/edit_welder?id={row["id_card"]}" target="_blank">编辑</a>', unsafe_allow_html=True)
            if cd.button("删除", key=f"del_{row['id_card']}"):
                ctrl.handle_delete(row['id_card'])
                st.rerun()
else:
    st.info("💡 库中尚无数据或未找到匹配项。")
