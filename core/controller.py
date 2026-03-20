from core.service import WelderService

class WelderController:
    def __init__(self):
        self.service = WelderService()

    def get_list(self):
        return self.service.get_all_welders()

    def add_welder(self, entity):
        return self.service.create_welder(entity)

    def remove_welder(self, id_card):
        return self.service.delete_welder(id_card)
