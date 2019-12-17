# -*- coding: utf-8 -*-

from six.moves.urllib.parse import urlencode
import pytest
from flask_rest_jsonapi.exceptions import InvalidSort
from flask_rest_jsonapi.data_layers.alchemy import SqlalchemyDataLayer


def test_invalid_sort(client, register_routes):
    with client:
        querystring = urlencode({'sort': 'error'})
        response = client.get('/persons' + '?' + querystring, content_type='application/vnd.api+json')
        assert response.status_code == 400


def test_sqlalchemy_data_layer_sort_query_error(session, person_model, monkeypatch):
    with pytest.raises(InvalidSort):
        dl = SqlalchemyDataLayer(dict(session=session, model=person_model))
        dl.sort_query(None, [dict(field='error')])


@pytest.mark.parametrize("sort_value", [
    'name',
    '-name',
    'name,birth_date',
    'name,-birth_date',
    'name,single_tag.value',
])
def test_valid_sort(sort_value, client, register_routes):
    with client:
        querystring = urlencode({'sort': sort_value})
        response = client.get('/persons' + '?' + querystring, content_type='application/vnd.api+json')
        assert response.status_code == 200

