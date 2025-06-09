import os
import random
import sys
import time

if len(sys.argv) < 2:
    print("Usage: python interactive_client.py <player_id>")
    sys.exit(1)

player_id = int(sys.argv[1])

min_bid = 100
max_bid = 9999
num_rounds = 5

# Questions and correct answers
questions = [
    {
        "question": "What type of problems are quantum algorithms particularly suited to solve?",
        "choices": ["A. Database Search", "B. Web Development", "C. Optimisation Problems", "D. Image Processing"],
        "answer": "C"
    },
    {
        "question": "What is the fundamental unit of information in quantum computing?",
        "choices": ["A. Bit", "B. Transistor", "C. Qubit", "D. Byte"],
        "answer": "C"
    },
    {
        "question": "What quantum computing concept allows multiple states to exist simultaneously?",
        "choices": ["A. Teleportation", "B. Entanglement", "C. Decoherence", "D. Superposition"],
        "answer": "D"
    },
    {
        "question": "What is the term for the phenomenon where quantum bits are correlated, even when separated by large distances?",
        "choices": ["A. Entanglement", "B. Tunneling", "C. Superposition", "D. Uncertainty"],
        "answer": "A"
    },
    {
        "question": "What is the main cryptographic advantage of quantum computing?",
        "choices": ["A. Generating Keys", "B. Breaking Classical Encryption Schemes Like RSA", "C. Faster Hashing", "D. Safer Email"],
        "answer": "B"
    }
]

def ask_question(q):
    print("\n" + q["question"])
    for choice in q["choices"]:
        print(choice)
    answer = input("Your answer (A/B/C/D): ").strip().upper()
    print("\n")
    return answer

def get_bonus(user_answer, correct_answer):
    if user_answer == correct_answer:
        return 1
    elif user_answer == "":
        return 0
    else:
        return -1

# Create directory if not exists
os.makedirs("Player-Data", exist_ok=True)

# Output file path
file_path = f"Player-Data/Input-P{player_id}-0"

# Initialize file with round 0
with open(file_path, "w") as f:
    f.write(f"0\n")

last_bid = min_bid - 1

for i in range(num_rounds):
    # Update first line with current round number
    if os.path.exists(file_path):
        with open(file_path, "r") as f:
            lines = f.readlines()
        lines = lines[1:]  # Remove first line
    else:
        lines = []

    # Get bid input
    if i == 0:
        while True:
            bid_input = input(f"Enter your bid for round {i+1} (between {last_bid + 1} and {max_bid}): ").strip()
            if not bid_input.isdigit():
                print("Invalid input. Please enter a non-empty number.")
                continue
            bid = int(bid_input)
            if bid < (last_bid + 1) or bid > max_bid:
                print(f"Invalid bid. Please enter a value between {last_bid + 1} and {max_bid}.")
                continue
            break
        last_bid = bid
    else:
        bid_input = input(f"Enter your bid for round {i+1} (between {last_bid + 1} and {max_bid}, or leave blank to skip): ").strip()
        if bid_input == "":
            bid = last_bid
        else:
            bid = int(bid_input)
            while bid < (last_bid + 1) or bid > max_bid:
                print(f"Invalid bid. Please enter a value between {last_bid + 1} and {max_bid}.")
                bid_input = input(f"Enter your bid for round {i+1} (between {last_bid + 1} and {max_bid}, or leave blank to skip): ").strip()
                if bid_input == "":
                    bid = last_bid
                    break
                bid = int(bid_input)
        last_bid = bid

    # Ask the question after the bid
    user_answer = ask_question(questions[i])
    bonus = get_bonus(user_answer, questions[i]["answer"])
    
    with open(file_path, "w") as f:
        f.write(f"{i + 1}\n")  # Write updated round number
        f.writelines(lines)    # Write the rest of the content
    # Append bid and bonus to file
        f.write(f"{bid}\n")
        f.write(f"{bonus}\n")
            
    log_file_path = f"wise_output{player_id}.log"

    while True:
        if os.path.exists(log_file_path):
            with open(log_file_path, "r") as log_file:
                lines = log_file.readlines()
                if len(lines) >= 4:
                    log_value = int(lines[0].strip())
                    if -1 * log_value == (i + 1):
                        round_no = log_value
                        bid_ranking = lines[2].strip()
                        bonus_amount = lines[3].strip()

                        print(f"Round No: {-1 * log_value}")
                        print(f"Bid Ranking : {bid_ranking}")
                        print(f"Bonus Amount: {bonus_amount}")
                        print(f"")                        
                        break
                    try:
                        log_value = int(round_no)
                        if -1 * log_value == (i + 1):
                            break
                    except ValueError:
                        print(f"Warning: Could not parse int from first line: '{round_no}'")
    time.sleep(1)  # Check every 1 second

print(f"Input received for bidder {player_id}. Please wait for the auction results.\n\n")
