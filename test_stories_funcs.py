""" Tests for functions in stories api"""
from unittest.mock import MagicMock
from stories_functions import (
load_all_stories,
update_stories,
make_new_story,
find_story_with_id,
add_votes,
delete_story,
sort_stories,
find_specific_story,
count_votes
)


def test_get_all_stories():
    """Tests if the stories load"""

    mock_connection = MagicMock()
    mock_fetch = mock_connection.cursor().fetchall
    mock_close = mock_connection.cursor().close


    mock_fetch.return_value = [{
    "created_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "id": 2441,
    "score": 0,
    "title": "Kayode HOMEPAGE",
    "updated_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "url": "www.kayode.co.uk"
  },
  {
    "created_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "id": 2443,
    "score": 2,
    "title": "Everton chairman Kenwright dies aged 78",
    "updated_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "url": "https://www.bbc.co.uk/sport/football/67203234"
  }]

    result = load_all_stories(mock_connection)

    mock_fetch.assert_called_once()

    assert "Kayode" in result[0]["title"]
    assert isinstance(result, list)
    assert mock_close.call_count == 1



def test_make_story():
    """Tests if story is added"""

    mock_connection = MagicMock()
    mock_execute = mock_connection.cursor().execute
    mock_commit = mock_connection.commit
    mock_close = mock_connection.cursor().close

    title = "goodstory"
    url = "www.goodstory.com"

    mock_query = "INSERT INTO stories (title, url, created_at, updated_at)\
        VALUES (%s, %s, current_timestamp, current_timestamp);"
    make_new_story(mock_connection, url, title)

    assert mock_execute.call_count == 1
    assert mock_execute.call_args[0][0] == mock_query
    assert mock_execute.call_args[0][1] == (title, url)
    assert mock_commit.call_count == 1
    assert mock_close.call_count == 1


def test_update_story():
    """Tests if the stories update"""

    mock_connection = MagicMock()
    mock_execute = mock_connection.cursor().execute
    mock_commit = mock_connection.commit
    mock_close = mock_connection.cursor().close

    title = "update"
    url = "www.update.com"

    mock_query = """UPDATE stories
        SET title = %s, url = %s, updated_at = current_timestamp 
        WHERE id = %s;"""
    update_stories(mock_connection, url, title, 2)

    assert mock_execute.call_count == 1
    assert mock_execute.call_args[0][0] == mock_query
    assert mock_execute.call_args[0][1] == (title, url, 2)
    assert mock_commit.call_count == 1
    assert mock_close.call_count == 1


def test_find_specific_story():
    """Tests if specific story can be found"""

    mock_connection = MagicMock()
    mock_fetch = mock_connection.cursor().fetchone
    mock_close = mock_connection.cursor().close
    searched_id = 2441

    mock_fetch.return_value = [{
    "created_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "id": 2441,
    "score": 0,
    "title": "Kayode HOMEPAGE",
    "updated_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "url": "www.kayode.co.uk"
  }]

    result = find_story_with_id(mock_connection, searched_id)

    mock_fetch.assert_called_once()
    assert result[0].get("id") == 2441
    assert isinstance(result, list)
    assert mock_close.call_count == 1


def test_make_vote():
    """Tests if vote is added"""

    mock_connection = MagicMock()
    mock_execute = mock_connection.cursor().execute
    mock_commit = mock_connection.commit
    mock_close = mock_connection.cursor().close

    direction = "up"

    mock_query = """INSERT INTO votes(direction, created_at, updated_at, story_id)
            VALUES (%s, current_timestamp, current_timestamp, %s);"""
    add_votes(mock_connection, direction, 56)

    assert mock_execute.call_count == 1
    assert mock_execute.call_args[0][0] == mock_query
    assert mock_execute.call_args[0][1] == (direction, 56)
    assert mock_commit.call_count == 1
    assert mock_close.call_count == 1


def test_count_votes():
    """Tests if vote count changes correctly"""

    mock_connection = MagicMock()
    mock_fetch = mock_connection.cursor().fetchone
    mock_close = mock_connection.cursor().close
    searched_id = 32

    mock_fetch.return_value = [{
    "created_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "id": 32,
    "score": 4,
    "title": "Kayode HOMEPAGE",
    "updated_at": "Thu, 26 Oct 2023 12:46:00 GMT",
    "url": "www.kayode.co.uk"
  }]

    result = count_votes(mock_connection, searched_id)

    mock_fetch.assert_called_once()
    assert result[0].get("score") == 4
    assert isinstance(result, list)
    assert mock_close.call_count == 1
