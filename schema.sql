DROP TABLE IF EXISTS posts;
CREATE TABLE posts (
	id INTEGER PRIMARY KEY,
	title TEXT NOT NULL,
	link TEXT NOT NULL,
	content TEXT NOT NULL,
	preview_content TEXT NOT NULL,
	created_datetime TEXT NOT NULL
);

DROP TABLE IF EXISTS dungeons;
CREATE TABLE dungeons (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	name TEXT NOT NULL,
	link TEXT NOT NULL,
	description TEXT NOT NULL,
	updated_datetime TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP)
);

DROP TABLE IF EXISTS dungeon_wings;
CREATE TABLE dungeon_wings (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	dungeon_id INTEGER NOT NULL,
	ordr INTEGER NOT NULL,
	name TEXT NOT NULL,
	description TEXT NOT NULL,
	FOREIGN KEY (dungeon_id) REFERENCES dungeons(id)
);

DROP TABLE IF EXISTS bosses;
CREATE TABLE bosses (
	id INTEGER PRIMARY KEY AUTOINCREMENT,
	dungeon_id INTEGER NOT NULL,
	wing_id INTEGER,
	ordr INTEGER NOT NULL,
	name TEXT NOT NULL,
	link TEXT NOT NULL,
	description TEXT NOT NULL,
	difficulties TEXT NOT NULL,
	overview TEXT,
	strategy TEXT,
	updated_datetime TEXT NOT NULL DEFAULT (CURRENT_TIMESTAMP),
	FOREIGN KEY (dungeon_id) REFERENCES dungeons(id),
	FOREIGN KEY (wing_id) REFERENCES dungeon_wings(id)
);

DROP TRIGGER IF EXISTS after_update_dungeon;
CREATE TRIGGER after_update_dungeon AFTER UPDATE OF name, link, description ON dungeons
BEGIN
	UPDATE dungeons
	SET updated_datetime = CURRENT_TIMESTAMP
	WHERE id = NEW.id;
END;

DROP TRIGGER IF EXISTS after_insert_dungeon_wing;
CREATE TRIGGER after_insert_dungeon_wing AFTER INSERT ON dungeon_wings
BEGIN
	UPDATE dungeons
	SET updated_datetime = CURRENT_TIMESTAMP
	WHERE id = NEW.dungeon_id;
END;

DROP TRIGGER IF EXISTS after_update_dungeon_wing;
CREATE TRIGGER after_update_dungeon_wing AFTER UPDATE ON dungeon_wings
BEGIN
	UPDATE dungeons
	SET updated_datetime = CURRENT_TIMESTAMP
	WHERE id = NEW.dungeon_id;
END;

DROP TRIGGER IF EXISTS after_insert_boss;
CREATE TRIGGER after_insert_boss AFTER INSERT ON bosses
BEGIN
	UPDATE dungeons
	SET updated_datetime = CURRENT_TIMESTAMP
	WHERE id = NEW.dungeon_id;
END;

DROP TRIGGER IF EXISTS after_update_boss;
CREATE TRIGGER after_update_boss AFTER UPDATE OF ordr, name, link, description, difficulties, overview, strategy ON bosses
BEGIN
	UPDATE bosses
	SET updated_datetime = CURRENT_TIMESTAMP
	WHERE id = NEW.id;
	UPDATE dungeons
	SET updated_datetime = CURRENT_TIMESTAMP
	WHERE id = NEW.dungeon_id;
END;
