import random

def play_game():
    choices = ['rock', 'paper', 'scissors']

    player_score = 0
    computer_score = 0
    max_score = 4  # Maximum points allowed

    while player_score < max_score and computer_score < max_score:
        print(f"\nPlayer Score: {player_score} | Computer Score: {computer_score}")
        player = input("\nRock, Paper, or Scissors? (type 'quit' to stop): ").lower()

        if player == 'quit':
            print("Thanks for playing! Goodbye!")
            break
        
        if player not in choices:
            print("Invalid choice. Please choose rock, paper, or scissors.")
            continue

        # Computer choice
        computer = random.choice(choices)
        print(f"Computer chose: {computer}")

        # Determine the outcome
        if player == computer:
            print("It's a draw!")
        elif (player == "rock" and computer == "scissors") or \
             (player == "paper" and computer == "rock") or \
             (player == "scissors" and computer == "paper"):
            print("You win this round!")
            player_score += 1
        else:
            print("You lose this round!")
            computer_score += 1

        # Check if someone reached the maximum score
        if player_score == max_score:
            print("\nCongratulations! You won the game!")
            break
        elif computer_score == max_score:
            print("\nSorry! The computer won the game!")
            break

if __name__ == "__main__":
    play_game()

