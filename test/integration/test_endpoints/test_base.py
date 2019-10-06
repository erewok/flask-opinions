"""
test_base.py

Test base endpoints
"""


def test_index(client):
    """obvious"""
    response = client.get('/')
    assert b"opinions" in response.data


def test_health(client):
    """obvious"""
    response = client.get('/health')
    assert b"Healthy" in response.data
