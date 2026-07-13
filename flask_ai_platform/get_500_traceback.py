import urllib.request
import urllib.error

try:
    response = urllib.request.urlopen('http://127.0.0.1:5000/auth/register')
    print("Success! Response Code:", response.getcode())
except urllib.error.HTTPError as e:
    print("HTTP Error:", e.code)
    body = e.read().decode('utf-8')
    # The body is an HTML page from werkzeug. Let's find the exception line.
    import re
    match = re.search(r'<title>(.*?)</title>', body)
    if match:
        print("Exception Title:", match.group(1))
    
    # Try to find the specific traceback message
    match2 = re.search(r'<h2>(.*?)</h2>', body)
    if match2:
        print("Exception Detail:", match2.group(1))
        
    print("Full body snippet:", body[:500])
except Exception as e:
    print("Other Exception:", e)
