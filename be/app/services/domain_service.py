class DomainService:
    def __init__(self, client):
        db = client['it']
        self.collection = db['cert']

    def get_domain_list(self):
        domains = list(self.collection.find({}))
        for domain in domains:
            print(domain)
        return domains
