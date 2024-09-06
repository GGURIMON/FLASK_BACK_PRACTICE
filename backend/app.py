from flask import Flask, jsonify, request

app = Flask(__name__)

diaries = {}
next_id = 1

@app.route('/diaries', methods = ['GET'])
def get_diaries():
   return jsonify(list(diaries.values()))

@app.route('/diaries', methods = ['POST'])
def create_diary():
    global next_id
    data = request.json

    if 'title' not in data or 'content' not in data:
        return jsonify({'error': 'Title and Content are required'}), 400
   
    diary = {
        'id': next_id,
        'title': data['title'],
        'content': data['content']
    }
    diaries[next_id] = diary
    next_id += 1
    return jsonify(diary), 201