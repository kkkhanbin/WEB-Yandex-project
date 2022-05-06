import requests


class TestUserResource:
    @staticmethod
    def test_delete_user_success():
        test_data = {'nickname': '88', 'email': 'example3@gmail.com',
                     'password': '132231231'}
        requests.post(
            'http://127.0.0.1:5000/api/users?apikey=4931cd24-'
            'ab93-4557-b454-c0175ad363fd', json=test_data)

        response = requests.delete(
            'http://127.0.0.1:5000/api/user/88?apikey=4931cd24-ab93-'
            '4557-b454-c0175ad363fd').json()

        assert response == {'success': 'OK'}
