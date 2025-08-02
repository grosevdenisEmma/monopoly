# Размер поля — 1280x1280
# Размер одной клетки ~128 (поле 10 клеток на сторону)

BOARD_SIZE = 1280
CELL_SIZE = 128  # размер клетки

def generate_board_cells():
    """
    Координаты по часовой стрелке начиная с GO (правый нижний угол).
    """
    names = [
        "GO", "Mediterranean Avenue", "Community Chest", "Baltic Avenue", "Income Tax", "Reading Railroad",
        "Oriental Avenue", "Chance", "Vermont Avenue", "Connecticut Avenue", "Jail",
        "St. Charles Place", "Electric Company", "States Avenue", "Virginia Avenue", "Pennsylvania Railroad",
        "St. James Place", "Community Chest", "Tennessee Avenue", "New York Avenue", "Free Parking",
        "Kentucky Avenue", "Chance", "Indiana Avenue", "Illinois Avenue", "B&O Railroad",
        "Atlantic Avenue", "Ventnor Avenue", "Water Works", "Marvin Gardens", "Go To Jail",
        "Pacific Avenue", "North Carolina Avenue", "Community Chest", "Pennsylvania Avenue", "Short Line",
        "Chance", "Park Place", "Luxury Tax", "Boardwalk"
    ]

    coords = []

    # Нижняя сторона (0..10)
    for i in range(11):
        x = BOARD_SIZE - CELL_SIZE * (i + 1)
        y = BOARD_SIZE - CELL_SIZE
        coords.append((x, y))
    # Левая сторона (11..20)
    for i in range(1, 10):
        x = 0
        y = BOARD_SIZE - CELL_SIZE * (i + 1)
        coords.append((x, y))
    # Верхняя сторона (21..30)
    for i in range(1, 11):
        x = CELL_SIZE * i
        y = 0
        coords.append((x, y))
    # Правая сторона (31..39)
    for i in range(1, 10):
        x = BOARD_SIZE - CELL_SIZE
        y = CELL_SIZE * i
        coords.append((x, y))

    board_cells = []
    for i, name in enumerate(names):
        if i < 40:
            x, y = coords[i]
            board_cells.append({
                "id": i,
                "name": name,
                "x": x,
                "y": y
            })
    return board_cells