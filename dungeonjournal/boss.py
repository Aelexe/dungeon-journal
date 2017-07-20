import json
from flask import current_app
from dungeonjournal import db

def get_boss_by_links(dungeon_link, boss_link):
    """Get the boss specified by the provided dungeon and boss link."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT b.name, b.link, b.description, b.difficulties, b.overview, b.strategy, b.updated_datetime FROM bosses b, dungeons d WHERE b.link = ? AND d.link = ? AND b.dungeon_id = d.id", (boss_link, dungeon_link,))
    boss = cursor.fetchone()

    return {"name": boss["name"], "link": boss["link"], "description": boss["description"],
            "difficulties": json.loads(boss["difficulties"]),
            "overview": json.loads(boss["overview"] if boss["overview"] else "[]"),
            "strategy": json.loads(boss["strategy"] if boss["strategy"] else "[]"),
            "updated_datetime": boss["updated_datetime"]
        }
