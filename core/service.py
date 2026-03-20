import pandas as pd
from core.dao import WelderDAO

class WelderService:
    """业务逻辑层：处理校验、逻辑计算"""
    def __init__(self):
        self.dao = WelderDAO()

    def list_all(self):
        df = self.dao.fetch_all()
        # 确保返回的是 DataFrame 即使没有数据
        if df is None:
            return pd.DataFrame()
        return df

    def add_process(self, entity):
        df = self.dao.fetch_all()
        # 业务校验：身份证号去重
        if not df.empty and entity.id_card in df['id_card'].values:
            return False, "该身份证号已存在！"
        
        # 将 Entity 转为行并追加
        new_row = pd.DataFrame([entity.to_dict()])
        updated_df = pd.concat([df, new_row], ignore_index=True)
        self.dao.commit(updated_df)
        return True, "成功"

    def update_process(self, id_card, entity):
        df = self.dao.fetch_all()
        if id_card not in df['id_card'].values:
            return False, "未找到该人员"
        
        idx = df.index[df['id_card'] == id_card]
        for key, value in entity.to_dict().items():
            df.loc[idx, key] = value
            
        self.dao.commit(df)
        return True, "更新完成"

    def delete_process(self, id_card):
        df = self.dao.fetch_all()
        df = df[df['id_card'] != id_card]
        self.dao.commit(df)
        return True, "删除成功"
