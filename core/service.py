import pandas as pd
from core.dao import WelderDAO

class WelderService:
     """业务逻辑层：处理复杂的校验和数据加工"""
    def __init__(self):
        self.dao = WelderDAO()

    def list_all(self):
        df = self.dao.fetch_all()
        # 确保返回的是 DataFrame 即使没有数据
        return df if isinstance(df, pd.DataFrame) else pd.DataFrame()
    
    # ... 其他方法保持不变 ...
    

    def add_process(self, entity):
        df = self.dao.fetch_all()
        # 业务校验：防止重复录入
        if entity.id_card in df['id_card'].values:
            return False, f"身份证号 {entity.id_card} 已存在！"
        
        new_df = pd.concat([df, pd.DataFrame([entity.to_dict()])], ignore_index=True)
        self.dao.commit(new_df)
        return True, "录入成功"

    def update_process(self, id_card, entity):
        df = self.dao.fetch_all()
        if id_card not in df['id_card'].values:
            return False, "未找到该人员"
        
        # 逻辑：定位行并替换数据
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
