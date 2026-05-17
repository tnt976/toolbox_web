from flask import Flask, render_template, request, jsonify
import difflib
import os

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/compare', methods=['POST'])
def compare():
    data = request.get_json()
    text1 = data.get('text1', '')
    text2 = data.get('text2', '')
    
    diff = difflib.SequenceMatcher(None, text1, text2)
    
    changes = []
    for tag, i1, i2, j1, j2 in diff.get_opcodes():
        changes.append({
            'type': tag,
            'text1_start': i1,
            'text1_end': i2,
            'text2_start': j1,
            'text2_end': j2,
            'text1_content': text1[i1:i2],
            'text2_content': text2[j1:j2]
        })
    
    return jsonify({
        'text1': text1,
        'text2': text2,
        'similarity': diff.ratio(),
        'changes': changes
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
