from flask import Flask, request

app = Flask(__name__)

@app.route('/')
def home():
    return 'Hello, World!'

@app.route('/null_pointer')
def null_pointer():
    try:
        # Simulating a potential Null Pointer vulnerability
        value = request.args.get('value')
        result = len(value)  # This can lead to a TypeError if 'value' is None
        return f'Result: {result}'
    except TypeError as e:
        return f'Error: {e}'
    except Exception as e:
        return f'An error occurred: {e}'

if __name__ == '__main__':
    app.run(debug=True)
