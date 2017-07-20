from datetime import datetime
from dateutil.parser import parse
from flask import current_app
from dungeonjournal import db

def get_posts(page = 0):
    """Get a list of posts from the pagination page specified by the 0 indexed page number."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT title, link, created_datetime, preview_content FROM posts ORDER BY created_datetime DESC LIMIT ?,?", (page * current_app.config["POST_PAGINATION_AMOUNT"], current_app.config["POST_PAGINATION_AMOUNT"]))
    posts = cursor.fetchall()

    return convert_posts(posts)

def get_post_by_link(post_link):
    """Get the post specified by the post link."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT title, link, created_datetime, content FROM posts WHERE link = ?", (post_link,))
    post = cursor.fetchone()

    return convert_post(post)

def get_archive_posts():
    """Get the archive list of all posts."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT title, link, created_datetime FROM posts ORDER BY created_datetime DESC")
    archive_posts = cursor.fetchall()
    for i, post in enumerate(archive_posts):
        created_date = parse(post["created_datetime"])
        archive_posts[i] = {"title": post["title"], "link": post["link"], "created_year": created_date.strftime("%Y"), "created_month": created_date.strftime("%B")}

    return convert_archive_posts(archive_posts)

def convert_posts(posts):
    """Convert a list of SQL post rows to the format used for display within the post templates."""
    for i, post in enumerate(posts):
        posts[i] = convert_post(post)
    return posts

def convert_post(post):
    """Convert an SQL post row to the format used for display within the post templates."""
    converted_post = {
        "title": post["title"] if "title" in post.keys() else "",
        "link": post["link"] if "link" in post.keys() else ""
    }

    try:
        converted_post["created_date"] = parse(post["created_datetime"]).strftime("%d/%m/%Y")
    except (KeyError, TypeError, ValueError):
        converted_post["created_date"] = ""

    if "content" in post.keys():
        converted_post["content"] = post["content"]
    if "preview_content" in post.keys():
        converted_post["preview_content"] = post["preview_content"]

    return converted_post

def convert_archive_posts(archive_posts):
    """Convert a list of SQL post rows to the format used for display within the post archive."""
    converted_archive = [];

    current_year = ""
    current_month = ""

    for post in archive_posts:
        # If the posts created year is not the current year being parsed, push that year.
        if post["created_year"] != current_year:
            current_year = post["created_year"]
            converted_archive.append({"year": current_year, "months": []})

        months = converted_archive[len(converted_archive) - 1]["months"]

        # If the posts created month is not the current month being parsed, push that month.
        if post["created_month"] != current_month:
            current_month = post["created_month"]
            months.append({"month": current_month, "posts": []})

        posts = months[len(months) - 1]["posts"]

        posts.append({"title": post["title"], "link": post["link"]})

    return converted_archive
