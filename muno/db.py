import sqlite3

import click
from flask import current_app, g

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row
    return g.db

def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

def init_db():
    db = get_db()
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

def delete_row(table, row):
    db = get_db()
    conn = sqlite3.connect('test_db.db')
    cur = conn.cursor()
    cur.execute('DELETE FROM {table} WHERE id = "{row}";')
    conn.commit()
    print(cur.fetchall())

def exist_speaker(username):
    conn = sqlite3.connect('instance/muno.sqlite')
    cur = conn.cursor()
    cur.execute('SELECT content COUNT(content) FROM sentence WHERE name = {username}')
    print(cur)
    return True

def get_sentence(username):
    print(username)
    conn = sqlite3.connect('instance/muno.sqlite')
    cur = conn.cursor()
    if(username is None) :
        print("username is none")
        cur.execute('SELECT content FROM sentence;')
    if(username is not None):
        print("username is not none")
        cur.execute('SELECT content FROM sentence WHERE speaker = :name;',{"name":username,})
    list = []
    for row in cur:
        list.append(str(row)[2:-3])
    cur.close()
    conn.close()
    return list
