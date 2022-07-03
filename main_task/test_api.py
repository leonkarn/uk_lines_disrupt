from main import app


def test_post_request():
    data = {"time": "20-11-12", "lines": ["victoria"], "description": "test_description", "type": "test_type",
            "updated": "2022"}
    response = app.test_client().post('/tasks', json=data)

    assert response.text == "inserted record into db"


def test_get_tasks():
    response = app.test_client().get('/tasks')
    assert response.status_code == 200
