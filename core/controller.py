from core.service import WelderService

class WelderController:
    def __init__(self):
        self.service = WelderService()

    def dispatch_get_list(self, query=None):
        return self.service.fetch_list(query)

    def dispatch_add(self, entity):
        return self.service.add_welder(entity)

    def dispatch_update(self, id_card, entity):
        return self.service.update_welder(id_card, entity)

    def dispatch_delete(self, id_card):
        return self.service.delete_welder(id_card)
