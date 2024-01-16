from flask import Flask, jsonify, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/get_file_content')
def get_file_content():
    with open('example.txt', 'r') as file:
        content = file.read()
    return jsonify({'content': content})

if __name__ == '__main__':
    app.run(debug=True)
