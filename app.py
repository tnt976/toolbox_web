from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/demo')
def demo():
    return render_template('demo.html')

@app.route('/api/greet', methods=['POST'])
def greet():
    data = request.get_json()
    name = data.get('name', 'Guest')
    message = f'Hello, {name}! Welcome to our Flask Web App!'
    return jsonify({'message': message, 'name': name})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
