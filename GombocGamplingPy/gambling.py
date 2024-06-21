import random
from flask import Flask, jsonify, request, send_from_directory
import sqlalchemy

from GombocGamplingPy.model import Session, Bet

app = Flask(__name__, static_folder='static')

@app.route('/')
def serve():
    return send_from_directory(app.static_folder, 'index.html')

# Route for placing a bet
@app.route('/bet', methods=['POST'])
def place_bet():
    session = Session()
    try:

        balance: int = get_latest_balance(session=session)
        data = request.get_json()
        amount = int(data.get('amount'))
        number = int(data.get('number'))
        print("here")

        # Simulate dice roll
        dice_roll = random.randint(1, 6)
        print(f" balance before: {balance}")
        if number == dice_roll:
            result = 'Win'
            outcome = amount * 5
            balance += amount * 5
        else:
            result = 'Lose'
            outcome = -amount
            balance -= amount

        print(f"balance after :{balance}")
        bet = Bet(amount=amount, number=number, dice_roll=dice_roll, outcome=outcome, balance=balance)
        print(f"placing bet with balance {balance}")
        save_bet(bet, session)
    except Exception as e:
        session.rollback()
        return jsonify('Error: ', str(e))
    finally:
        session.close()
    return jsonify({'balance': balance, 'result': result, 'outcome': outcome, 'dice_roll': dice_roll, 'guess': number})

def save_bet(bet: Bet, session:Session):
    # Save bet to database
    print("saving bet", bet)
    session.add(bet)
    session.commit()
    print(f"Saved bet: {bet}")  # Debug statement
    session.close()

def get_latest_balance(session):
    last_bet = session.query(Bet).order_by(Bet.id.desc()).first()
    return last_bet.balance if last_bet else 1000  # Default initial balance

# Route to get the current balance
@app.route('/balance', methods=['GET'])
def get_current_balance():
    session = Session()
    try:
        balance = get_latest_balance(session)
        print("balance: ", balance)
    finally:
        session.close()
    return jsonify({'balance': balance})

# Route for getting bet history
# Route for getting bet history
@app.route('/history', methods=['GET'])
def get_history():
    session = Session()
    try:
        bets = session.query(Bet).all()
        bet_list = [
            {'id': bet.id, 'balance': bet.balance, 'amount': bet.amount, 'number': bet.number, 'dice_roll': bet.dice_roll, 'outcome': bet.outcome}
            for bet in bets
        ]
        print(f"Retrieved bets: {bet_list}")  # Debug statement
    except Exception as e:
        print(f"Error retrieving bets: {e}")  # Debug statement
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
    return jsonify(bet_list)


# Route for withdrawing balance and resetting the game
@app.route('/withdraw', methods=['POST'])
def withdraw():
    session = Session()
    try:
        balance = 1000
        bet = Bet(amount=0, number=0, dice_roll=0, outcome=0, balance=balance)
        save_bet(bet, session)
    except Exception as e:
        session.rollback()
        return jsonify('Error: ', str(e)), 500
    finally:
        session.close()
    return jsonify({'balance': balance})

# Serve React static files
@app.route('/<path:path>')
def serve_static_files(path):
    return send_from_directory(app.static_folder, path)

if __name__ == '__main__':
    app.run(debug=True)
