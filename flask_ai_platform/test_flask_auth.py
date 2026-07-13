from app import create_app
app = create_app()
app.config['TESTING'] = True
app.config['WTF_CSRF_ENABLED'] = False

with app.test_client() as client:
    try:
        response = client.post('/auth/register', data={
            'username': 'testuser',
            'email': 'test@example.com',
            'password': 'password123',
            'confirm_password': 'password123'
        })
        print(response.status_code)
        print(response.data.decode('utf-8')[:500])
    except Exception as e:
        import traceback
        traceback.print_exc()
