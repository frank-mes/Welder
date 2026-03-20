import streamlit as st
from core.controller import WelderController
from core.entity import WelderEntity

st.title("📝 编辑/删除资质")
ctrl = WelderController()

search_id = st.text_input("输入身份证号查询并编辑")
df = ctrl.get_all()
target = df[df['id_card'] == search_id]

if not target.empty:
    row = target.iloc[0]
    with st.form("edit_form"):
        # 回显数据逻辑 (使用 value=row['xxx'])
        name = st.text_input("姓名", value=row['name'])
        stamp_code = st.text_input("钢印号", value=row['stamp_code'])
        # ... 其他字段省略，同新增页面回显 ...
        
        btn_update = st.form_submit_button("更新信息")
        btn_delete = st.form_submit_button("删除人员")
        
        if btn_update:
            new_entity = WelderEntity(name=name, id_card=search_id, stamp_code=stamp_code) # 补全其他
            ctrl.update(search_id, new_entity)
            st.success("更新成功")
        if btn_delete:
            ctrl.delete(search_id)
            st.warning("已删除")
