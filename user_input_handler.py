class UserInput:

    def ask_for_free_text(statement: str) -> str:
        return input(statement + "\n")

    def ask_for_integer(statement: str, min: int, max: int) -> int:
        while True:
            try:        
                data = int(input(f"{statement}\nPossible answers are between {min} and {max}.\n"))
                if not min <= data <= max:
                    print("Please input a whole number.")
            except ValueError:
                print("Please input a whole number.")
            else:
                break
        return data

    def ask_for_boolean(statement: str) -> bool:
        while True:
            try:        
                data = input(f"{statement}\nPossible answers:\n  yes\n  no\n")
                if data != "yes" and data != "no":
                    print(f"Please answer either 'yes' or 'no'.")
                    continue
            except ValueError:
                print("Please input a whole number.")
            else:
                break
        return data == "yes"

    def ask_to_select(statement: str, options: list[str], return_index: bool=False) -> str:
        statement = f"{statement}\nPossible answers:\n"
        for i, option in enumerate(options, start=1):
            statement += f"  {i}. {option}\n"
        while True:
            try:        
                index = int(input(statement))
                if index > len(options) + 1:
                    print(f"There is no answer option for the number {index}.")
                    continue
            except ValueError:
                print("Please input the number of your answer.")
            else:
                break
        return index - 1 if return_index else options[index - 1] 