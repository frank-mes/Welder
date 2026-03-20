import streamlit as st
from core.controller import WelderController
from core.entity import WelderEntity

st.set_page_config(page_title="编辑人员")
ctrl = WelderController()

# 从 URL 获取参数 (Streamlit 1.30+ 支持查询参数)
params = st.query_params
target_id = params.get("id")

st.header(f"📝 编辑人员信息 ({target_id})")
df = ctrl.dispatch_get_list()
row = df[df['id_card'] == target_id].iloc[0] if target_id in df['id_card'].values else None

if row is not None:
    with st.form("edit_form"):
        # 回显 row 中的数据...
        new_name = st.text_input("姓名", value=row['name'])
        # ...其他字段...
        if st.form_submit_button("提交修改"):
            new_entity = WelderEntity(name=new_name, id_card=target_id, ...)
            ctrl.dispatch_update(target_id, new_entity)
            st.success("修改成功！可以关闭此标签页。")
