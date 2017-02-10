import requests

key = 'key-d47971b31e4f183660b42cb709f788e4'
sandbox = 'sandbox922b9b0446fb4c688b1a284a8fa6b4c4.mailgun.org'
recipient = 'raghavpiet108@poornima.org'

request_url = 'https://api.mailgun.net/v3/{0}/messages'.format(sandbox)
request = requests.post(request_url, auth=('api', key), data={
    'from': "Mailgun Sandbox <postmaster@sandbox922b9b0446fb4c688b1a284a8fa6b4c4.mailgun.org>",
    'to': recipient,
    'subject': 'Hello',
    'text': 'Hello from Mailgun'
})

print('Status: {0}'.format(request.status_code))
print('Body:   {0}'.format(request.text))
