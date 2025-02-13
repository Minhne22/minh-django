import requests

cookies = {
    'bm_sz': '2FDABC297EB41ABD7E94338F7E6F8659~YAAQqxQgF0Qqz9+UAQAAhsN/9RoSWT9XYwbAf6IDTw27OMczFVyfNCw5F/jHUZfEMc3zc9jLZQi4jNzKXQB3go+5bZaxz+G8/aKLk/iZ+tSVinZRstIPkmDGF2cFggL1Dm4iNUhmAFXnW1wCv2rMaDhzqM5kM0FhI/CwX0DnMLgEg9uTq/FCGHFEZBFiNDRDo+532J6XjCvly7WXXN6BKmfxOYYEP49qS2Ohrp4VzFeKC64lyObyLZARsTt3Yx0vGvJHobH31WZbwzyywSu2MtBXOK3rIiVZ/UgW0YW1jpICGHnk58hd/NdFyBegPtOBcZdGGWbPv7MHK8qrJrayOInqGunnbnmGsHUmi8NZoWwnDTKv9uiQjeiTKrgRdPhARyXvAKGMBL1xYMk5~4469812~3420468',
    'PIM-SESSION-ID': 'friOxL8m2vtPiRyw',
    '_abck': '62D1A2757A5847A4565F0B8853FCD298~-1~YAAQqxQgF7Qqz9+UAQAAV8Z/9Q2Hl3IeJoftqPYCXNVzvjzpKEz8xf8QbjPcJkxWRHz6NeRqN8CVu8Oum0klt7ChqjlaiLZNxa5gwN17snolv8zmLctF5NRNGnWYQInWQnsJOD/RYHFK59v0Goix4kw5419P+EWyynRii93JKCZYqy2QDSQ4s3xu8UH4whCnACy5WrM82ty/rpz8VSdBJjoOtoEXs9bBjnQhN6+vvASta6oJ7GSmQKqbeHA4IU4aDxBTpJ3bGFzaIsxcLfaj7TZHJvGDlbL5fXzYXaebUy/B9+UqxQY3CIUOyS1P4vt1yG7Ea8mx7B2vCKNrfZjRqsQOMoTCL+m0vckxL0HstAGbc0C4Xu0CWz+LXUWnVEc+wHd700XMNIRNZsYtAVUakBv65QL/Aw7ZqVovg3TECcYSGzdrj7gmerju1SmMEWbKSDeJntXSXl+lBSDkHWQQ5zpS~-1~-1~-1',
    'dtCookie': 'v_4_srv_-2D46_sn_BT32TAOSBHVSLMCHCE9BHU93U8DFDOB5',
    'rxVisitor': '1739285579761U6U4RLKAPHL7QL5OQSB5UV84DMPS6601',
    'ak_bmsc': '36EE4049A9766134F832E057A99F2BE9~000000000000000000000000000000~YAAQqxQgFywrz9+UAQAAYsp/9RqTGKsCYVXSwB3XYp7F1aGKDpSPJUBFJO+18g97p4T3uzhZd2eoilAUsCUbAGy99vnWNxCwbsL0OqjN8oDkL3HokO79g28JzYyn9Q/EAVfvhuP20ygaLSEMo8VhVodxpxi8HEFWRwK8g1iZTKPjsLuduU11U608pUDAEgNDW5zcxSXmuFt7hIb0C/tl0V/Xh4whGiAbRlatPgOHjZn8a3bj0bNKPIi5JGpDJNkqBpjTlc5cJTbhWy6Du4mt0xxxtA7fg3WrqNQ/2Q7sXAd2MQv1ZihDlgrNr82v0vI6XG2emHqatB7ew5GZl/Cm8BpQHbPvxKNlBQDTprbANOtXpD+WJGff7QX4xcX7HHKigXZQ4lWEMAoYt2cckeqr1VeTuHmU/gwO4TSflek30YJLwYtk',
    'rxvt': '1739287380806|1739285579764',
    'dtPC': '-46$485579757_50h5vFBIRHVRCASFHRTLITCURKHGPAEBFUAFC-0e0',
    'dtSa': 'true%7CC%7C-1%7Clogin-cta%7C-%7C1739285580814%7C485579757_50%7Chttps%3A%2F%2Fwww.keurig.com%2F%7C%7C%7C%7C',
    'RT': '"z=1&dm=keurig.com&si=p6u7oiswhep&ss=m70lq6ff&sl=1&tt=0&obo=1&ld=u4&r=3d55f6e5dabf3f0a94f317c8b510caeb&ul=u5"',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-US,en;q=0.9',
    # 'cookie': 'bm_sz=2FDABC297EB41ABD7E94338F7E6F8659~YAAQqxQgF0Qqz9+UAQAAhsN/9RoSWT9XYwbAf6IDTw27OMczFVyfNCw5F/jHUZfEMc3zc9jLZQi4jNzKXQB3go+5bZaxz+G8/aKLk/iZ+tSVinZRstIPkmDGF2cFggL1Dm4iNUhmAFXnW1wCv2rMaDhzqM5kM0FhI/CwX0DnMLgEg9uTq/FCGHFEZBFiNDRDo+532J6XjCvly7WXXN6BKmfxOYYEP49qS2Ohrp4VzFeKC64lyObyLZARsTt3Yx0vGvJHobH31WZbwzyywSu2MtBXOK3rIiVZ/UgW0YW1jpICGHnk58hd/NdFyBegPtOBcZdGGWbPv7MHK8qrJrayOInqGunnbnmGsHUmi8NZoWwnDTKv9uiQjeiTKrgRdPhARyXvAKGMBL1xYMk5~4469812~3420468; PIM-SESSION-ID=friOxL8m2vtPiRyw; _abck=62D1A2757A5847A4565F0B8853FCD298~-1~YAAQqxQgF7Qqz9+UAQAAV8Z/9Q2Hl3IeJoftqPYCXNVzvjzpKEz8xf8QbjPcJkxWRHz6NeRqN8CVu8Oum0klt7ChqjlaiLZNxa5gwN17snolv8zmLctF5NRNGnWYQInWQnsJOD/RYHFK59v0Goix4kw5419P+EWyynRii93JKCZYqy2QDSQ4s3xu8UH4whCnACy5WrM82ty/rpz8VSdBJjoOtoEXs9bBjnQhN6+vvASta6oJ7GSmQKqbeHA4IU4aDxBTpJ3bGFzaIsxcLfaj7TZHJvGDlbL5fXzYXaebUy/B9+UqxQY3CIUOyS1P4vt1yG7Ea8mx7B2vCKNrfZjRqsQOMoTCL+m0vckxL0HstAGbc0C4Xu0CWz+LXUWnVEc+wHd700XMNIRNZsYtAVUakBv65QL/Aw7ZqVovg3TECcYSGzdrj7gmerju1SmMEWbKSDeJntXSXl+lBSDkHWQQ5zpS~-1~-1~-1; dtCookie=v_4_srv_-2D46_sn_BT32TAOSBHVSLMCHCE9BHU93U8DFDOB5; rxVisitor=1739285579761U6U4RLKAPHL7QL5OQSB5UV84DMPS6601; ak_bmsc=36EE4049A9766134F832E057A99F2BE9~000000000000000000000000000000~YAAQqxQgFywrz9+UAQAAYsp/9RqTGKsCYVXSwB3XYp7F1aGKDpSPJUBFJO+18g97p4T3uzhZd2eoilAUsCUbAGy99vnWNxCwbsL0OqjN8oDkL3HokO79g28JzYyn9Q/EAVfvhuP20ygaLSEMo8VhVodxpxi8HEFWRwK8g1iZTKPjsLuduU11U608pUDAEgNDW5zcxSXmuFt7hIb0C/tl0V/Xh4whGiAbRlatPgOHjZn8a3bj0bNKPIi5JGpDJNkqBpjTlc5cJTbhWy6Du4mt0xxxtA7fg3WrqNQ/2Q7sXAd2MQv1ZihDlgrNr82v0vI6XG2emHqatB7ew5GZl/Cm8BpQHbPvxKNlBQDTprbANOtXpD+WJGff7QX4xcX7HHKigXZQ4lWEMAoYt2cckeqr1VeTuHmU/gwO4TSflek30YJLwYtk; rxvt=1739287380806|1739285579764; dtPC=-46$485579757_50h5vFBIRHVRCASFHRTLITCURKHGPAEBFUAFC-0e0; dtSa=true%7CC%7C-1%7Clogin-cta%7C-%7C1739285580814%7C485579757_50%7Chttps%3A%2F%2Fwww.keurig.com%2F%7C%7C%7C%7C; RT="z=1&dm=keurig.com&si=p6u7oiswhep&ss=m70lq6ff&sl=1&tt=0&obo=1&ld=u4&r=3d55f6e5dabf3f0a94f317c8b510caeb&ul=u5"',
    'priority': 'u=0, i',
    'referer': 'https://www.keurig.com/',
    'sec-ch-ua': '"Not A(Brand";v="8", "Chromium";v="132", "Google Chrome";v="132"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'same-site',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/132.0.0.0 Safari/537.36',
}

params = {
    'client_id': 'kqRwx9GzIfhobyPbap2DvfSaWWGSNayu',
    'scope': 'openid profile email offline_access',
    'redirect_uri': 'https://www.keurig.com/authCallBack',
    'audience': 'customers-apis',
    'ext-baseredirecturi': 'https://www.keurig.com/authCallBack',
    'ui_locales': 'en',
    'response_type': 'code',
    'response_mode': 'query',
    'state': '',
    'nonce': '',
    'code_challenge': '',
    'code_challenge_method': 'S256',
    'auth0Client': '',
}

response = requests.get('https://login.keurig.com/authorize', params=params, headers=headers)
print(response.text)
print(response.url)
with open('caidai.html', 'w+', encoding='utf8') as f:
    f.write(response.text)