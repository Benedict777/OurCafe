import pytest
from django.contrib.auth.models import User
from django.urls import reverse

from core.models import MenuItem, Order, Table


@pytest.mark.django_db
def test_menu_page_is_public(client):
    MenuItem.objects.create(name="Osh", price=45000)
    response = client.get(reverse('menu_list'))
    assert response.status_code == 200
    assert "Osh" in response.content.decode()


@pytest.mark.django_db
def test_orders_require_login(client):
    response = client.get(reverse('order_list'))
    assert response.status_code == 302
    assert '/login/' in response.url


@pytest.mark.django_db
def test_order_total_price():
    user = User.objects.create_user('ali', password='12345')
    table = Table.objects.create(number=1, seats=4)
    osh = MenuItem.objects.create(name="Osh", price=45000)
    choy = MenuItem.objects.create(name="Choy", price=8000)
    order = Order.objects.create(user=user, table=table)
    order.items.set([osh, choy])
    assert order.total_price() == 53000


@pytest.mark.django_db
def test_api_menu_list(client):
    MenuItem.objects.create(name="Kofe", price=18000)
    response = client.get('/api/menu/')
    assert response.status_code == 200
    assert response.json()[0]['name'] == "Kofe"