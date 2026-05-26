import requests,json

class API():
    def __init__(self,data,hostname,port,username,password):
        self.data = data
        self.hostname = hostname
        self.port = port
        self.username = username
        self.password = password

    def API_send(self):
        json_bu2 = self.data.to_json(orient='records')

        url = self.hostname

        payload = json.dumps(json.loads(json_bu2))
        headers = {
        'Authorization': f'{self.password}',
        'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)

        print(response.text,response)