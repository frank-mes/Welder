from core.service import WelderService
import pandas as pd

class WelderController:
    """控制器：接收前端指令并分发"""
    def __init__(self):
        self.service = WelderService()

    def get_all(self):
        try:
            return self.service.list_all()
        except Exception:
            # 即使后端报错，也返回一个带表头的空表
            return pd.DataFrame(columns=['id', 'name', 'gender', 'id_card', 'stamp_code', 'workshop', 'team', 'cert_large', 'cert_small'])

    def create(self, entity):
        return self.service.add_process(entity)

    def update(self, id_card, entity):
        return self.service.update_process(id_card, entity)

    def delete(self, id_card):
        return self.service.delete_process(id_card)
