""" Tests for routes in stories api """
from api import app
import json
from unittest.mock import patch


def test_index():
    """ Tests if the index page returns successfully """

    test_client = app.test_client()
    response = test_client.get('/')

    assert response.status_code == 200


@patch("api.get_db_connection")
@patch("api.load_all_stories")
def test_get_request_all_stories(mock_new_story, mock_database, api_client):
    """Finds all stories on get request"""

    mock_new_story.return_value = [{
        "title": "bob"
    }]
    response = api_client.get("/stories")
    body = response.json

    assert response.status_code == 200
    assert body == [{
        "title": "bob"
    }]


@patch("api.get_db_connection")
@patch("api.load_all_stories")
def test_gets_no_stories(mock_new_story, mock_database, api_client):
    """Finds stories on get request"""

    mock_new_story.return_value = []
    response = api_client.get("/stories")
    body = response.json

    assert response.status_code == 404
    assert body == [{"error": True, "message": "No stories were found"}]


@patch("api.get_db_connection")
@patch("api.make_new_story")
def test_post_story_request_success(mock_new_story, mock_database, api_client):
    """Successful post request of new story"""

    response = api_client.post("/stories", json={
        "title": "Kayode2 Website",
        "url": "www.kayode2.co.uk"
    })


    body = response.json

    assert response.status_code == 201
    assert body == {"success": "New story added"}


@patch("api.get_db_connection")
@patch("api.make_new_story")
def test_invalid_post_story(mock_new_story, mock_database, api_client):
    """Unsuccessful post requests to new story"""

    url_response = api_client.post("/stories", json={
        "title": "Ukraine\u2019s cyber-teams duel with Russians on front lines",
    })
    title_response = api_client.post("/stories", json={
        "url":
        "https://www.vice.com/en/article/xgzxvz/\
        voters-overwhelmingly-back-community-broadband-in-chicago-and-denver"
    })

    title_body = title_response.json
    url_body = url_response.json

    assert url_response.status_code == 400 
    assert url_body == {"error": "missing url"}
    assert title_response.status_code == 400
    assert title_body == {"error": "missing title"}


@patch("api.get_db_connection")
@patch("api.find_story_with_id")
@patch("api.update_stories")
def test_successful_patch_request(story_update, found_story, mock_database, api_client):
    """Successful patch to edit story"""

    found_story.return_value = {
        "url": "https://www.bbc.co.uk//news/uk-politics-67151404",
        "title": "Rishi Sunak backs Israel against 'evil' Hamas",
        "id": 2,
        "score": 0,
        "created_at": "Thursday, 19  2023 16:48:46 GMT",
        "updated_at": "Thursday, 19  2023 16:48:46 GMT"
    }

    response = api_client.patch("/stories/2", json={
        "title": "Kayode2 Website",
        "url": "www.kayode2.co.uk"
    })

    body = response.json

    assert response.status_code == 201
    assert body == {"success": "Story updated"}


@patch("api.get_db_connection")
@patch("api.find_story_with_id")
@patch("api.update_stories")
def test_story_non_existent(story_update, found_story, mock_database, api_client):
    """Story doesn't exist when patch request is made"""

    found_story.return_value = []

    response = api_client.patch("/stories/87687587567", json={
        "title": "Kayode2 Website",
        "url": "www.kayode2.co.uk"
    })

    assert response.status_code == 404
    assert story_update.call_count == 0


@patch("api.get_db_connection")
@patch("api.update_stories")
@patch("api.find_story_with_id")
def test_edit_a_story(mock_find_story, update, mock_database, api_client):
    """ Tests if the index page returns successfully """

    mock_find_story.return_value = [{
        "url": "https://www.bbc.co.uk//news/uk-politics-67151404",
        "title": "Rishi Sunak backs Israel against 'evil' Hamas",
        "id": 2,
        "score": 0,
        "created_at": "Thursday, 19  2023 16:48:46 GMT",
        "updated_at": "Thursday, 19  2023 16:48:46 GMT"
    }]

    response = api_client.patch("/stories/2", json= {
        "url": "https://www.bbc.co.uk/news/world-60525350/news/world-europe-66686584",
        "title": "Ukraine\u2019s cyber-teams duel with Russians on front lines"
    })

    body = response.json
    assert response.status_code == 201
    assert body == {"success": "Story updated"}
