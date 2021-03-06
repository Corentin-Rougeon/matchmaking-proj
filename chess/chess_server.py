from flask import Flask, request, abort

app = Flask(__name__)

@app.route('/webhook', methods=['POST'])
def webhook():
    if request.method == 'POST':
        print(request.get_json())
        return 'success', 200
    else:
        abort(400)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=8000, debug=True)