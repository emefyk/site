from flask import Flask, request, redirect, url_for, jsonify
import sqlite3

app = Flask(__name__, static_folder='.', static_url_path='')

# Initialiser la base de données
def init_db():
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            message TEXT NOT NULL,
            date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()

init_db()

@app.route('/')
def index():
    return redirect(url_for('static', filename='index.html'))

@app.route('/save', methods=['POST'])
def save():
    name = request.form.get('name', '').strip()
    message = request.form.get('message', '').strip()

    if not name or not message:
        return jsonify(error="Nom et message requis"), 400

    # Insérer dans SQLite3
    conn = sqlite3.connect('app.db')
    cur = conn.cursor()
    cur.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
    conn.commit()
    conn.close()

    return jsonify(success=True, message="Message enregistré !"), 201

@app.route('/messages', methods=['GET'])
def get_messages():
    """Récupérer tous les messages"""
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cur.execute("SELECT id, name, message, date FROM messages ORDER BY date DESC")
    rows = cur.fetchall()
    conn.close()
    
    return jsonify([dict(row) for row in rows])

if __name__ == '__main__':
    app.run(debug=True)