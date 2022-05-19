import pytest
from sys import path
path.append("../")
import app

#переназначил путь файла с постами для теста
app.posts = app.ToGet("../data/posts.json")


#проверка путей
def test_api_to_get():
    """проверяет отзывчивость страницы"""
    resp = app.app.test_client().get("/api/posts/", follow_redirects=True)
    assert resp.status_code == 200, "статус кода запроса не верный"
    assert resp.mimetype == "application/json", "получен не json"


#все посты
def test_api_type():
    """проверяет тип json"""
    resp = app.app.test_client().get("/api/posts/", follow_redirects=True)
    assert type(resp.json) == list, "не верный json"
    assert len(resp.json) == 8, "не верное кол-во постов"

def test_api_one_get():
    """проверяет правильны ли получены данные"""
    resp = app.app.test_client().get("/api/posts/", follow_redirects=True)
     
    keys = {"poster_name", "poster_avatar", "pic", "content", "views_count", "likes_count", "pk"}
    first_keys = set(resp.json[0].keys())
    assert keys == first_keys, "полученные ключи не совпадают"


#один пост
def test_api_one_post_get():
    """проверяет что один пост с правильной отдачей"""
    resp = app.app.test_client().get("/api/posts/1", follow_redirects=True)
    assert resp.status_code == 200, "статус кода запроса не верный"
    assert resp.mimetype == "application/json", "получен не json"
    assert type(resp.json) == dict, "не верный json"
    
    
