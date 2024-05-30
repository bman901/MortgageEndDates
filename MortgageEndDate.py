import requests
class PFP(object):
    def __init__(self, template_id):
        self.template_id = template_id
        self.PFP_url = 'https://app.precisefp.com/api/v3/form-engagements'

        infile = open("Bearer.txt", "r")
        Bearer = infile.read()
        infile.close()

        self.data = {}
        self.headers = {
            'Accept': 'application/json',
            'Authorization': Bearer
        }

    def set_id(self, template_id):
        self.template_id = template_id

    def get_id(self):
        return self.template_id
    def get_engagements(self):
        """
        Using the template ID find matching engagements
        """
        url = self.PFP_url + '?sort=-created_at&limit=200&offset=200&template_id=' + self.template_id
        get_engage = requests.get(url, data=self.data, headers=self.headers).json()
        items = get_engage['items']
        output = []
        for i in range(10):
            output.append(items[i]['id'])
        return output

    def get_engagement_data(self):
        """
        Load the engagement data
        """
        engage_data = []
        engage_id = self.get_engagements()
        for id in engage_id:
            close = self.PFP_url + '/' + id + '/close'
            requests.post(close, data=self.data,headers=self.headers).json()  # Ensures the engagement is closed, which is a requirement to get the data
            url = 'https://app.precisefp.com/api/v3/form-engagements/' + id + '/data'
            get_data = requests.get(url, data=self.data, headers=self.headers).json()  # Gets the engagement data
            engage_data.append(get_data)
        return (engage_data)

single_ff = '2607bae9-bce4-4fa7-877e-088cc8b1fad2'

single = PFP(single_ff)

print(single.get_engagement_data())