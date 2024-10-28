from flask import Flask, jsonify, request
import pymysql
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'basic_sql',
    'port': 3308
}
db_con = pymysql.connect(**db_config)
cursor = db_con.cursor()


@app.route('/', methods=['GET'])
def index():
    try:
        # cursor.execute('SELECT * FROM items')
        # items = cursor.fetchall()
        cursor.execute('SELECT id, name FROM items')
        items = [{'id': id, 'name': name} for id, name in cursor.fetchall()]
        return jsonify(items)
    except Exception as e:
        return jsonify({'message': str(e)})


@app.route('/items', methods=['POST'])
def insert():
    try:
        data = request.get_json()
        name = data.get('name')
        cursor.execute('INSERT INTO items (name) VALUES (%s)', (name,))
        db_con.commit()
        return jsonify({'massege': 'Insert Successfully'})
    except Exception as e:
        return jsonify({'message': str(e)})


@app.route('/items/<int:Id>', methods=['PUT'])
def update(Id):
    try:
        data = request.get_json()
        name = data.get('name')
        cursor.execute('UPDATE items SET name = (%s)  WHERE id = (%s)',
                       (name, Id))
        db_con.commit()
        return jsonify({'massege': 'Update Successfully'})
    except Exception as e:
        return jsonify({'message': str(e)})


@app.route('/items/<int:Id>', methods=['DELETE'])
def delete(Id):
    try:
        cursor.execute('DELETE FROM items WHERE id = (%s)', (Id))
        db_con.commit()
        return jsonify({'massege': 'Delete Successfully'})
    except Exception as e:
        return jsonify({'message': str(e)})


if __name__ == '__main__':
    app.run(debug=True)  # run the app in debug mode
