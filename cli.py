from openai_client import OpenAIClient
def main():
    client = OpenAIClient()
    while True:
        print("\nPlease choose your action.")
        print("1) Ask a general question.")
        print("2) Get coding help.")
        print("3) Quit")
        choice = input("Your choice: ")

        if choice == "3":
            print("Exiting program. Have a productive day!")
            break

        elif choice == "1":
            question = input("Enter your question.")
            answer = client.get_a_direct_answer(question)
            print(f"\n Answer: {answer}")

        elif choice == "2":
            question = input("Enter your question.")
            hint = client.get_a_hint(question)
            print(f"\n Hint: {hint}")

            while True:
                print("\nPlease choose your action.")
                print("1) Get another hint.")
                print("2) Get a guiding question.")
                print("3) Show the direct solution.")
                print("4) End this question.")

                alt_choice = input("Your choice: ")
                if alt_choice == "1":
                    hint = client.get_a_hint(question)
                    print(f"\n Answer: {hint}")

                elif alt_choice == "2":
                    guiding_question = client.get_a_question(question)
                    print(f"\n Question: {guiding_question}")

                elif alt_choice == "3":
                    solution = client.get_a_solution(question)
                    print(f"\n Solution: {solution}")
                    break
                elif alt_choice == "4":
                    break
                else:
                    print("Invalid choice. Please try again.")

        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()