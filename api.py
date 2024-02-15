"""Backend API for use on Social News scraping site"""
from flask import Flask, current_app, request
from dotenv import load_dotenv
from stories_functions import (
get_db_connection,
load_all_stories,
update_stories,
make_new_story,
find_story_with_id,
add_votes,
delete_story,
sort_stories,
find_specific_story,
count_votes)
from news_scaper import get_html, parse_stories_bs


app = Flask(__name__)
load_dotenv()


@app.route("/", methods=["GET"])
def index():
    """Gets stories page from html static file"""
    return current_app.send_static_file("index.html")


@app.route("/add", methods=["GET"])
def addstory():
    """Endpoint allows user to add story of their choice"""
    return current_app.send_static_file("./addstory/index.html")


@app.route("/scrape", methods=["GET", "POST"])
def scrape():
    """Endpoint allows user to view or make post request to scrape website"""
    db_connection = get_db_connection()

    if request.method == 'POST':
        current_stories = load_all_stories(db_connection)
        data = request.json
        url = data["url"]

        if "bbc.co.uk" not in url:
            return {
                "error": True,
                "message":
                "Can only scrape from BBC homepage or BBC Topic pages at this moment in time"
            }, 400

        html = get_html(url)
        new_scrape_stories = parse_stories_bs(url, html)

        for story in new_scrape_stories:
            new_story = make_new_story(story, current_stories)
            current_stories.append(new_story)

        update_stories(current_stories)
        return {"success": "Scraped stories added"}, 201

    return current_app.send_static_file("./scrape/index.html")


@app.route("/stories", methods=["GET", "POST"])
def get_stories() -> list:
    """Endpoint allows user to create new stories, or filter current stories"""
    db_connection = get_db_connection()

    if request.method == 'POST':
        new_story_info = request.json

        if "url" not in new_story_info:
            return {"error": "missing url"}, 400

        if "title" not in new_story_info:
            return {"error": "missing title"}, 400

        make_new_story(db_connection, new_story_info["url"], new_story_info["title"])

        return {"success": "New story added"}, 201

    if request.method == 'GET':
        stories = load_all_stories(db_connection)
        args = request.args.to_dict()
        search = args.get('search')
        sort = args.get('sort')
        order = args.get('order')

        if stories:

            if search:
                return find_specific_story(db_connection, search), 200

            if sort in {"title", "score", "created", "modified"}:
                return sort_stories(db_connection, sort, order), 200

            return stories, 200

        return [{"error": True, "message": "No stories were found"}], 404


@app.route("/stories/<int:story_id>", methods=["PATCH", "DELETE"])
def edit_stories(story_id: int) -> dict:
    """Endpoint allows user to delete story of their choice"""
    db_connection = get_db_connection()

    story = find_story_with_id(db_connection, story_id)
    if story == []:
        return {"error": "There is no story with this id"}, 404

    if request.method == 'PATCH':
        edited_story_info = request.json

        if "url" not in edited_story_info:
            return {"error": "missing url"}, 400

        if "title" not in edited_story_info:
            return {"error": "missing title"}, 400

        update_stories(db_connection,
                       edited_story_info["url"],
                       edited_story_info["title"],
                       story_id
                       )

        return {"success": "Story updated"}, 201

    if request.method == 'DELETE':
        delete_story(db_connection, story_id)

    return {"success": "Story deleted"}, 200


@app.route("/stories/<int:story_id>/votes", methods=["POST"])
def vote(story_id: int) -> dict:
    """Endpoint allows user to vote story of their choice"""
    db_connection = get_db_connection()

    data = request.json
    direction = data["direction"]

    votes = count_votes(db_connection, story_id)
    score = votes[0].get('score')
    if not score and direction == "down":
        return {
            "error": True,
            "message": "Can't downvote for a story with points of 0"
        }, 400

    add_votes(db_connection, direction, story_id)

    return {"success": "user voted"}, 200


if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=5000)
