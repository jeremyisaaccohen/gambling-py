import random
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

BALANCE = 1000

@app.route('/')
def home():
    return render_template('index.html', balance=BALANCE)

# Route for placing a bet
@app.route('/bet', methods=['POST'])
def place_bet():
    global BALANCE
    data = request.get_json()
    amount = int(data.get('amount'))
    number = int(data.get('number'))

    # Simulate dice roll
    dice_roll = random.randint(1, 6)
    if number == dice_roll:
        result = 'win'
        winnings = amount * 5
        BALANCE += winnings
        return jsonify({'balance': BALANCE, 'result': result, 'winnings': winnings, 'dice_roll': dice_roll})
    else:
        result = 'lose'
        BALANCE -= amount
        return jsonify({'balance': BALANCE, 'result': result, 'losings': amount, 'dice_roll': dice_roll})

if __name__ == '__main__':
    app.run(debug=True)
