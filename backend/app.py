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

@app.route('/diaries/<int:diary_id>', methods = ['PUT'])
def update_diary(diary_id):
    data = request.json
    diary = diaries.get(diary_id)

    # 만일 수정할 다이어리가 없다면, Diary Not Found 에러 반환, 응답 코드 404
    if diary is None:
        return jsonify({'error': 'Diary Not Found'}), 404
    
    # diary 변수 업데이트
    if 'title' in data:
        diary['title'] = data['title']
    if 'content' in data:
        diary['content'] = data['content']

    # diaries 딕셔너리 전역변수를 업데이트
    diaries['diary_id'] = diary
    # json 형식으로 업데이트 된 diary 반환, 응답코드 200(기본 값)
    return jsonify(diary)


@app.route('/diaries/<int:diary_id>', methods = ['DELETE'])
def delete_diary(diary_id):
    diary = diaries.get(diary_id)

    # 삭제할 다이어리가 없을 때, 404
    if diary is None:
        return jsonify({'error': 'Diary Not Found'}), 404
    
    # 다이어리 제거
    del diaries[diary_id]

    return jsonify(diary), 200