from flask import jsonify
from app.services.link_list_service import LinkListService


class LinkListController:
    def __init__(self, db):
        self.link_list_service = LinkListService(db)

    def get_link_list(self):
        link_list = self.link_list_service.get_link_list()
        return jsonify({"code": 200, "message": "success", "data": link_list})
