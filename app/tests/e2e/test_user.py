import http


def test_create_user(user_data):
    created_user_data, res = user_data
    assert res == http.HTTPStatus.CREATED
