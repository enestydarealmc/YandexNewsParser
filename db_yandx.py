def create_table(conn):
    try:
        if conn:
            conn.autocommit = True
            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS stories(
                    story_id INT NOT NULL PRIMARY KEY,
                    story_name TEXT,
                    appearance TIMESTAMP,
                    request_time TIMESTAMP,
                    url TEXT)"""
                )
                print("[INFO] create table successfully")

            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS instories(
                    story_id INT,
                    media_name TEXT,
                    published TIMESTAMP,
                    headline TEXT PRIMARY KEY,
                    request_time TIMESTAMP,
                    author TEXT,
                    page_url TEXT,
                    FOREIGN KEY (story_id) REFERENCES stories (story_id))"""
                )
                print("[INFO] create table successfully")

            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS tm_sites(
                    id INT,
                    name TEXT,
                    url TEXT)"""
                )
                print("[INFO] create table successfully")

            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS mentions(
                    story_id INT,
                    object TEXT,
                    media_name TEXT,
                    page_url TEXT,
                    headline TEXT,
                    FOREIGN KEY (story_id) REFERENCES stories (story_id),
                    FOREIGN KEY (headline) REFERENCES instories (headline))"""
                )
                print("[INFO] create table successfully")

            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS story_dynamics(
                    request_time TIMESTAMP,
                    story_id INT,
                    position INT,
                    interest INT,
                    weight INT,
                    views FLOAT,
                    FOREIGN KEY (story_id) REFERENCES stories (story_id))"""
                )
                print("[INFO] create table successfully")

            with conn.cursor() as cursor:
                cursor.execute(
                    """CREATE TABLE IF NOT EXISTS media_dynamics(
                    request_time TIMESTAMP,
                    story_id INT,
                    media_name TEXT,
                    headline TEXT,
                    position INT,
                    FOREIGN KEY (story_id) REFERENCES stories (story_id),
                    FOREIGN KEY (headline) REFERENCES instories (headline))"""
                )
                print("[INFO] create table successfully")

    except Exception as _ex:
        print("[INFO] Error while working with PostgreSQL:\n", _ex)
