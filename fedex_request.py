import requests

class req():
    def __init__(self, req_url, cred_dict):
        self.url = req_url
        self.parent_key = cred_dict['parent_key']
        self.parent_password = cred_dict['parent_password']
        self.user_key = cred_dict['user_key']
        self.user_password = cred_dict['user_password']
        self.client_account = cred_dict['client_account']
        self.client_meter = cred_dict['client_meter']

    def track(self, tack_id):
        with open("track_body.xml", "r") as payload_file:
            payload_raw = payload_file.read()

        payload = payload_raw.format(parent_key = self.parent_key, parent_password = self.parent_password,
                                    user_key = self.user_key, user_password = self.user_password,
                                    client_account = self.client_account, client_meter = self.client_meter,
                                    tracking_number = tack_id)
        headers = {
        'Content-Type': 'application/xml',
        'Cookie': 'siteDC=wtc'
        }

        response = requests.request("POST", self.url, headers=headers, data=payload)
        return response
