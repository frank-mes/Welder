import pandas as pd
from core.dao import WelderDAO

class WelderService:
    def __init__(self):
        self.dao = WelderDAO()

    def get_all_welders(self):
        return self.dao.select_all()

    def create_welder(self, entity):
        df = self.dao.select_all()
        # 校验：身份证号唯一性
        if entity.id_card in df['id_card'].values:
            return False, "错误：该身份证号已存在！"
        
        # 转换 Entity 为 DataFrame 行并追加
        new_row = pd.DataFrame([entity.to_dict()])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        self.dao.update_sheet(updated_df)
        return True, "人员新增成功！"

    def delete_welder(self, id_card):
        df = self.dao.select_all()
        updated_df = df[df['id_card'] != id_card]
        self.dao.update_sheet(updated_df)
        return True, "人员已删除"
