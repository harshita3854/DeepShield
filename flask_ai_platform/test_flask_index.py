import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://127.0.0.1:5000/')
    print("Success! Response Code:", response.getcode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    body = e.read().decode('utf-8')
    import re
    match = re.search(r'<title>(.*?)</title>', body)
    if match:
        print("Exception Title:", match.group(1))
    
    match2 = re.search(r'<h2>(.*?)</h2>', body)
    if match2:
        print("Exception Detail:", match2.group(1))
        
    print("Full body snippet:", body[:500])
except Exception as e:
    print("Other Exception:", e)
