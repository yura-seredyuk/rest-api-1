from app import app, client
from models import Info


def test_post():
    data = {
        'id': 1,
        'title': 'Unit test',
        'description': 'Message 3 description'
    }
    res = client.post('/data', json=data)

    assert res.status_code == 200
    assert res.get_json()['title'] == data['title']

def test_get():
    res = client.get('/data')

    assert res.status_code == 200
    assert len(res.get_json()) == len(Info.query.all())
    assert res.get_json()[0]['id'] == 1

def test_put():
    res = client.put('/data/1', json={'title':'TEST TITLE'})

    assert res.status_code == 200
    assert Info.query.get(1).title == 'TEST TITLE'

# def test_delete():
#     res = client.delete('/data/1')

#     assert res.status_code == 204
#     assert Info.query.get(1) is None

