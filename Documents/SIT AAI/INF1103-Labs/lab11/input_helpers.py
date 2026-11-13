def get_positive_float(prompt: str) -> float:
    # Keeps asking until the user enters a number greater than zero
    while True:
        try:
            value = float(input(prompt))
            if value <= 0:
                print("Please enter a number greater than zero.")
                continue
            return value
        except ValueError:
            print("Please enter a valid number, e.g. 12.50")
