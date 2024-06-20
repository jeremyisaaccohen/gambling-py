import random
from flask import Flask, jsonify, request, render_template

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

# Route for placing a bet
@app.route('/bet', methods=['POST'])
def place_bet():
    amount = request.form.get('amount')
    number = request.form.get('number')

    # Convert amount and number to integers
    amount = int(amount)
    number = int(number)

    # Simulate dice roll
    dice_roll = random.randint(1, 6)
    if number == dice_roll:
        result = 'win'
        winnings = amount * 5
    else:
        result = 'lose'
        winnings = 0

    return jsonify({'result': result, 'winnings': winnings, 'dice_roll': dice_roll})

if __name__ == '__main__':
    app.run(debug=True)
