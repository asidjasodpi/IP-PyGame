def load_score():
    try:
        with open("score.txt", "r") as file:
            return int(file.read())
    except (FileNotFoundError, ValueError):
        # Если файла нет или он пустой, вернём 0
        return 0

def save_score(score):
    with open("score.txt", "w") as file:
        file.write(str(score))