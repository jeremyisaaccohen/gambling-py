import random
from flask import Flask, jsonify, request, send_from_directory, Response

from GombocGamplingPy.model import Session, Bet

app = Flask(__name__, static_folder='static')


@app.route('/')
def serve() -> Response:
    return send_from_directory(app.static_folder, 'index.html')


def roll_dice(balance: int, guess: int) -> int:
    """
    Rolls a die, either fairly or rigged based on the balance.

    Args:
        balance (int): The current balance of the player.
        guess (int): The player's guess for the dice roll.

    Returns:
        int: The result of the dice roll.
    """
    fair_roll = random.randint(1, 6)
    if balance < 5000:
        return fair_roll
    # If we're wrong, don't reroll.
    if guess != fair_roll:
        return fair_roll
    # Now we know we got it right, calculate reroll odds.
    if balance < 10000:
        reroll_chance = 3  # 30%
    else:
        reroll_chance = 5  # 50%
    reroll = random.randint(1, 10)
    if reroll <= reroll_chance:
        print(f"{reroll_chance * 10}% chance hit, we're rerolling!")
        return random.randint(1, 6)

    return fair_roll


@app.route('/bet', methods=['POST'])
def place_bet() ->tuple[Response, int] | Response:
    """
    Places a bet, rolls a potentially rigged die, updates the balance, and saves the bet.

    Returns:
        json: A JSON response containing the updated balance, result, outcome, dice roll, and guess.
    """
    session = Session()
    try:
        balance: int = get_latest_balance(session=session)
        data = request.get_json()
        amount = int(data.get('amount'))
        if amount > balance:
            return jsonify(
                {'error': 'Cannot place bet, insufficient balance remaining. Please give us more money!'}), 400
        number = int(data.get('number'))

        # Roll the potentially rigged die
        dice_roll = roll_dice(balance, guess=number)
        if number == dice_roll:
            result = 'Win'
            outcome = amount * 5
            balance += amount * 5
        else:
            result = 'Lose'
            outcome = -amount
            balance -= amount

        bet = Bet(amount=amount, number=number, dice_roll=dice_roll, outcome=outcome, balance=balance, result=result)
        save_bet(bet, session)
        if balance == 0:
            balance = 1000
            bet = Bet(amount=0, number=0, dice_roll=0, outcome=0, balance=balance, result='You ran out of cash! Reset!')
            save_bet(bet, session)
    except Exception as e:
        session.rollback()
        return jsonify('Error: ', str(e))
    finally:
        session.close()
    return jsonify({'balance': balance, 'result': result, 'outcome': outcome, 'dice_roll': dice_roll, 'guess': number})


def save_bet(bet: Bet, session: Session) -> None:
    """
    Saves a bet to the database.

    Args:
        bet (Bet): The bet to save.
        session (Session): The database session.
    """
    session.add(bet)
    session.commit()
    print(f"Saved bet: {bet}")
    session.close()


def get_latest_balance(session: Session) -> int:
    """
    Retrieves the latest balance from the database.

    Args:
        session (Session): The database session.

    Returns:
        int: The latest balance, or the default initial balance if none is found.
    """
    last_bet = session.query(Bet).order_by(Bet.id.desc()).first()
    return last_bet.balance if last_bet else 1000  # Default initial balance


@app.route('/balance', methods=['GET'])
def get_current_balance() -> Response:
    """
    Retrieves the current balance of the player.

    Returns:
        json: A JSON response containing the current balance.
    """
    session = Session()
    try:
        balance = get_latest_balance(session)
    finally:
        session.close()
    return jsonify({'balance': balance})


# Route for getting bet history
@app.route('/history', methods=['GET'])
def get_history() -> tuple[Response, int] | Response:
    """
    Retrieves the bet history.

    Returns:
        json: A JSON response containing the bet history.
    """
    session = Session()
    try:
        bets = session.query(Bet).all()
        bet_list = [
            {'id': bet.id, 'balance': bet.balance, 'amount': bet.amount, 'number': bet.number,
             'dice_roll': bet.dice_roll, 'outcome': bet.outcome, 'result': bet.result}
            for bet in bets
        ]
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        session.close()
    return jsonify(bet_list)


@app.route('/withdraw', methods=['POST'])
def withdraw():
    """
    Resets the balance to 1000 and saves a withdraw action in the bet history.

    Returns:
        json: A JSON response containing the updated balance.
    """
    session = Session()
    try:
        balance = 1000
        bet = Bet(amount=0, number=0, dice_roll=0, outcome=0, balance=balance, result='Withdrawn')
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
    """
    Serves static files.

    Args:
        path (str): The path of the static file.

    Returns:
        response: The static file response.
    """
    return send_from_directory(app.static_folder, path)


if __name__ == '__main__':
    app.run(debug=True)
