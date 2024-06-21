### Assumptions


### Todo
If the user's balance reaches 0, the game should reset to the initial state.
##### Extra rules
- If the user's balance is greater or equal to 5000, the dice roll should be rigged with the following logic:
    - If the dice roll matches the user bet (before claiming the user win), there is a 30% chance that the server will repeat the roll (a single time) and use the second roll as the final result.
- If the user's balance is greater or equal to 10000, the dice roll should be rigged with the following logic:
    - If the dice roll matches the user bet (before claiming the user win), there is a 50% chance that the server will repeat the roll (a single time) and use the second roll as the final result.

##### Extra features
- If the user's balance is greater or equal to 20000 and the user try to press `withdraw` button, the button should move away from the mouse cursor.