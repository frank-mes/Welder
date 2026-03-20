from core.service import WelderService

class WelderController:
    """控制器：View 的唯一接口，不包含业务逻辑"""
    def __init__(self):
        self.service = WelderService()

    def get_all(self):
        return self.service.list_all()

    def create(self, entity):
        return self.service.add_process(entity)

    def update(self, id_card, entity):
        return self.service.update_process(id_card, entity)

    def delete(self, id_card):
        return self.service.delete_process(id_card)
