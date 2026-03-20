import streamlit as st
from core.controller import WelderController

st.set_page_config(page_title="焊工资质管理", layout="wide")
ctrl = WelderController()

st.title("👨‍🏭 焊工人员资质管理系统")

# 1. 顶部操作区
col_btn1, col_btn2, col_search = st.columns([1, 1, 4])
with col_btn1:
    # 引导至新标签页
    st.markdown('<a href="/新增人员" target="_blank"><button style="width:100%;height:40px;background-color:#28a745;color:white;border:none;border-radius:5px;cursor:pointer;">➕ 新增人员</button></a>', unsafe_allow_html=True)
with col_search:
    keyword = st.text_input("", placeholder="输入姓名或身份证号查询...", label_visibility="collapsed")

# 2. 数据展示区
df = ctrl.dispatch_get_list(keyword)

if not df.empty:
    # 模拟大厂的操作栏：遍历数据并生成按钮
    header_cols = st.columns([1, 1, 2, 1, 1, 1, 1, 1, 2])
    fields = ["姓名", "性别", "身份证号", "钢印号", "车间", "班组", "大证", "小证", "操作"]
    for col, field in zip(header_cols, fields):
        col.write(f"**{field}**")
    
    for _, row in df.iterrows():
        cols = st.columns([1, 1, 2, 1, 1, 1, 1, 1, 2])
        cols[0].write(row['name'])
        cols[1].write(row['gender'])
        cols[2].write(row['id_card'])
        cols[3].write(row['stamp_code'])
        cols[4].write(row['workshop'])
        cols[5].write(row['team'])
        cols[6].write(row['cert_large'])
        cols[7].write(row['cert_small'])
        
        # 操作栏按钮
        with cols[8]:
            c_edit, c_del = st.columns(2)
            # 编辑按钮跳转新标签页 (带参数)
            edit_url = f"/编辑人员?id={row['id_card']}"
            c_edit.markdown(f'<a href="{edit_url}" target="_blank">编辑</a>', unsafe_allow_html=True)
            if c_del.button("删除", key=f"del_{row['id_card']}"):
                ctrl.dispatch_delete(row['id_card'])
                st.rerun()
else:
    st.warning("暂无匹配数据")
