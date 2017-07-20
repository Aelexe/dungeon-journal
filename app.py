import os
import sys
sys.path.insert(0, '/home/aelexe/public_html/cgi-bin/myenv/lib/python2.6/site-packages')
import sqlite3
import re
from datetime import datetime
from dateutil.parser import parse
from flask import Flask, g, request, Response, render_template, abort
from dungeonjournal import dungeon, boss, post, db

app = Flask(__name__)

app.config.update(dict(
    DATABASE = os.path.join(app.root_path, "dungeonjournal.db"),
    POST_PAGINATION_AMOUNT = 10
))

@app.cli.command("initdb")
def initdb_command():
    db.init_db()
    print("Initialized the database.")

@app.teardown_appcontext
def close_db(error):
    if hasattr(g, "db_connection"):
        g.db_connection.close()

@app.route("/")
@app.route("/blog")
@app.route("/blog/page/<int:page>")
def show_posts(page = 1):
    if(page < 1):
        abort(404)

    posts = post.get_posts(page - 1)

    if len(posts) == 0:
        abort(404)

    return render_template("blog/blog.j2", posts = posts, archive = post.get_archive_posts())

@app.route("/blog/post/<post_link>")
def show_post(post_link):
    return render_template("blog/post.j2", post = post.get_post_by_link(post_link), archive = post.get_archive_posts())

@app.route("/dungeon/<dungeon_link>")
def show_dungeon(dungeon_link):
    dungeon_details = dungeon.get_dungeon_display_details(dungeon_link)
    updated_datetime = parse(dungeon_details["updated_datetime"] + "+00:00") # Manually add suffix as SQLite doesn't support timezones.

    if "If-Modified-Since" in request.headers and parse(request.headers["If-Modified-Since"]) >= updated_datetime:
        return "", 304

    response = Response(render_template("dungeon/dungeon.j2", dungeon = dungeon_details))
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Last-Modified"] = updated_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response

@app.route("/dungeon/<dungeon_link>/<boss_link>")
def show_boss(dungeon_link, boss_link):
    boss_details = boss.get_boss_by_links(dungeon_link, boss_link)
    updated_datetime = parse(boss_details["updated_datetime"] + "+00:00") # Manually add suffix as SQLite doesn't support timezones.

    if "If-Modified-Since" in request.headers and parse(request.headers["If-Modified-Since"]) >= updated_datetime:
        return "", 304

    response = Response(render_template("dungeon/boss.j2", boss = boss_details, dungeon_link = dungeon_link, dungeon_name = dungeon.get_dungeon_name_by_link(dungeon_link)))
    response.headers["Cache-Control"] = "no-cache"
    response.headers["Last-Modified"] = updated_datetime.strftime("%a, %d %b %Y %H:%M:%S GMT")
    return response

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.j2'), 404

def replace_links(text):
    pattern = re.compile("\\(([^\\)*]*)\\)(\\[[^\\]]*\\])")

    while True:
        match = pattern.search(text)
        if match is None:
            break;
        text = text.replace(match.group(0), "<span class='ability'><a href='https://www.wowhead.com/" + match.group(1) + "' target='_blank'>" + match.group(2) + "</a></span>")

    return text

app.jinja_env.filters["replace_links"] = replace_links
