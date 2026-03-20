import pandas as pd
from core.dao import WelderDAO

class WelderService:
    def __init__(self):
        self.dao = WelderDAO()

    def fetch_list(self, keyword=None):
        df = self.dao.select_all()
        if keyword and not df.empty:
            # 实现模糊查询逻辑
            mask = df.apply(lambda row: keyword in str(row.values), axis=1)
            return df[mask]
        return df

    def add_welder(self, entity):
        df = self.dao.select_all()
        if not df.empty and entity.id_card in df['id_card'].values:
            return False, "该身份证号已存在"
        new_df = pd.concat([df, pd.DataFrame([entity.to_dict()])], ignore_index=True)
        self.dao.save_all(new_df)
        return True, "新增成功"

    def update_welder(self, id_card, entity):
        df = self.dao.select_all()
        idx = df.index[df['id_card'] == id_card]
        if not idx.empty:
            for k, v in entity.to_dict().items():
                df.loc[idx, k] = v
            self.dao.save_all(df)
            return True, "修改成功"
        return False, "未找到该人员"

    def delete_welder(self, id_card):
        df = self.dao.select_all()
        df = df[df['id_card'] != id_card]
        self.dao.save_all(df)
        return True, "删除成功"
