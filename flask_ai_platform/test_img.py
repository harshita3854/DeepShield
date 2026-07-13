import requests
print(requests.post('http://127.0.0.1:5000/image/detect', files={'image': ('dummy.jpg', b'dummy_content')}).json())
