from flask import current_app
from dungeonjournal import db

def get_dungeon_display_details(dungeon_link):
    """Get the display details for a dungeon by its dungeon link."""
    dungeon = get_dungeon_by_link(dungeon_link)
    dungeon["wings"] = get_wings_by_link(dungeon_link)

    for i, wing in enumerate(dungeon["wings"]):
        wing["bosses"] = get_bosses_by_wing_id(wing["id"])

    return dungeon

def get_dungeon_by_link(dungeon_link):
    """Get a dungeon by its dungeon link."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT name, link, description, updated_datetime FROM dungeons WHERE link = ?", (dungeon_link,))
    dungeon = cursor.fetchone()

    return {"name": dungeon["name"], "link": dungeon["link"], "description": dungeon["description"], "updated_datetime": dungeon["updated_datetime"]}

def get_dungeon_name_by_link(dungeon_link):
    """Get the name of the dungeon by its dungeon link."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT name FROM dungeons WHERE link = ?", (dungeon_link,))
    dungeon = cursor.fetchone()

    return dungeon["name"]

def get_wings_by_link(dungeon_link):
    """Get the wings of a dungeon by its dungeon link."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT dw.id, dw.name, dw.description FROM dungeons d, dungeon_wings dw WHERE d.link = ? AND d.id = dw.dungeon_id ORDER BY dw.ordr", (dungeon_link,))
    wings = cursor.fetchall()

    for i, wing in enumerate(wings):
        wings[i] = {"id": wing["id"], "name": wing["name"], "description": wing["description"]}

    return wings

def get_bosses_by_wing_id(wing_id):
    """Get the bosses of a wing by its wing id."""
    db_connection = db.get_db()
    cursor = db_connection.execute("SELECT name, link FROM bosses WHERE wing_id = ? ORDER BY ordr", (wing_id,))
    bosses = cursor.fetchall()

    return bosses
