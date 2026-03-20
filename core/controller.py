from core.service import WelderService

class WelderController:
    def __init__(self):
        self.service = WelderService()

    def handle_get(self, q=None):
        return self.service.get_list(q)

    def handle_add(self, entity):
        return self.service.add_welder(entity)

    def handle_edit(self, id_card, entity):
        return self.service.update_welder(id_card, entity)

    def handle_delete(self, id_card):
        return self.service.delete_welder(id_card)
