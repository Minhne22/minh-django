data = '''login: conmemay@cc.com
password: asfwA131
recaptcha: 
fingerprint: 
recaptchaToken: '''
hic = "&".join([
    x.replace(': ', '=') for x in data.split('\n')
])

print(hic)