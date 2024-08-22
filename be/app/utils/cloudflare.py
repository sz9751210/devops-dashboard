import requests


class CloudflareManager:
    def __init__(self, api_key, email):
        self.api_key = api_key
        self.email = email
        self.base_url = "https://api.cloudflare.com/client/v4/zones"

    def fetch_all_domains_and_records(self):
        headers = {
            "X-Auth-Email": self.email,
            "Authorization": "Bearer " + self.api_key,
            "Content-Type": "application/json",
        }
        all_domains_info = []
        page = 1
        per_page = 50

        while True:
            try:
                response = requests.get(self.base_url, headers=headers, params={
                                        "page": page, "per_page": per_page})
                if response.status_code != 200:
                    raise Exception(
                        f"Error fetching domains: {response.status_code}")
                response_data = response.json()
                zones = response_data.get("result", [])
                if not zones:
                    break

                for zone in zones:
                    domain_name = zone["name"]
                    print(f"Fetching records for {domain_name}")
                    records_url = f"{self.base_url}/{zone['id']}/dns_records"
                    records_response = requests.get(records_url, headers=headers)
                    if records_response.status_code != 200:
                        raise Exception(
                            f"Error fetching records: {records_response.status_code}, {records_response.text}")

                    records = records_response.json().get("result", [])
                    for record in records:
                        if record["type"] in ["A", "CNAME"] and not record.get(
                            "proxied", False
                        ):
                            subdomain = record["name"]
                            if subdomain.startswith("_"):
                                continue
                            if domain_name == subdomain:
                                continue
                            all_domains_info.append((domain_name, subdomain))
                result_info = response_data.get("result_info", {})
                if result_info.get("page") * result_info.get("per_page") >= result_info.get("total_count"):
                    break
                page += 1
            except Exception as e:
                print(f"Error fetching records for page {page}: {e}")
                break
        return all_domains_info
