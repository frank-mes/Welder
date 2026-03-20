import pandas as pd
from core.dao import WelderDAO

class WelderService:
    def __init__(self):
        self.dao = WelderDAO()

    def get_list(self, query=None):
        df = self.dao.select_all()
        if query and not df.empty:
            # 简单的模糊搜索
            mask = df.astype(str).apply(lambda x: query.lower() in x.str.lower().values, axis=1)
            return df[mask]
        return df

    def add_welder(self, entity):
        df = self.dao.select_all()
        if not df.empty and str(entity.id_card) in df['id_card'].astype(str).values:
            return False, "身份证号已存在"
        
        new_row = pd.DataFrame([entity.to_dict()])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        self.dao.update_storage(updated_df)
        return True, "成功存入云端"

    def update_welder(self, id_card, entity):
        df = self.dao.select_all()
        idx = df.index[df['id_card'].astype(str) == str(id_card)]
        if not idx.empty:
            for k, v in entity.to_dict().items():
                df.loc[idx, k] = v
            self.dao.update_storage(df)
            return True, "更新成功"
        return False, "未找到该人员"

    def delete_welder(self, id_card):
        df = self.dao.select_all()
        updated_df = df[df['id_card'].astype(str) != str(id_card)]
        self.dao.update_storage(updated_df)
        return True, "删除成功"
