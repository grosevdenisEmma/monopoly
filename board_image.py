from PIL import Image, ImageDraw, ImageFont
import requests
from io import BytesIO
from monopoly.board import Board

BOARD_SIZE = 1280
CELL_SIZE = 128
PLAYER_COLORS = [
    "#FF4500", "#1E90FF", "#228B22", "#FFD700", "#9400D3", "#00CED1", "#8B0000", "#FF69B4"
]

def get_avatar_image(avatar_url, size=64):
    """Загрузить аватарку игрока (Telegram)"""
    try:
        response = requests.get(avatar_url)
        img = Image.open(BytesIO(response.content)).convert("RGBA")
        img = img.resize((size, size), Image.ANTIALIAS)
        return img
    except Exception:
        # Заглушка если не удалось загрузить
        img = Image.new("RGBA", (size, size), "#CCCCCC")
        return img

def draw_board(game, font_path="arial.ttf"):
    """
    Сгенерировать изображение поля с фишками, домами, отелями, собственностью.
    game: объект Game
    font_path: путь к TTF-шрифту
    """
    board = Board()
    img = Image.new("RGBA", (BOARD_SIZE, BOARD_SIZE), "#ffffff")
    draw = ImageDraw.Draw(img)

    # 1. Нарисовать клетки
    for cell in board.all_cells():
        x, y = cell["x"], cell["y"]
        cell_id = cell["id"]
        prop = board.get_property(cell_id)
        color = "#dddddd"
        if prop and prop.get("color"):
            color = prop.get("color")
            color = Board().properties[cell_id].get("color", "#dddddd")
            # Преобразуем в HEX если нужно
            color_map = {
                "brown": "#8B4513", "light_blue": "#ADD8E6", "pink": "#FF69B4",
                "orange": "#FFA500", "red": "#FF0000", "yellow": "#FFFF00",
                "green": "#008000", "dark_blue": "#00008B", "railroad": "#222222",
                "utility": "#AAAAAA"
            }
            color = color_map.get(color, color)
        draw.rectangle([x, y, x + CELL_SIZE, y + CELL_SIZE], fill=color, outline="#222222", width=3)

        # Имя клетки
        try:
            font = ImageFont.truetype(font_path, 18)
        except Exception:
            font = ImageFont.load_default()
        draw.text((x + 8, y + 8), cell["name"], fill="#111111", font=font)

    # 2. Нарисовать собственность (метка владельца, дома/отели)
    for prop in game.properties:
        if prop.owner_id is not None:
            owner_idx = [p.user_id for p in game.players].index(prop.owner_id)
            px, py = board.get_coords(prop.id)
            # Метка владельца
            draw.ellipse([px + CELL_SIZE - 30, py + 10, px + CELL_SIZE - 10, py + 30],
                         fill=PLAYER_COLORS[owner_idx % len(PLAYER_COLORS)], outline="#222222")
            # Дома/отели
            if prop.type == "street":
                # Дома
                for h in range(prop.house_count):
                    draw.rectangle([px + 10 + h*22, py + CELL_SIZE - 30, px + 30 + h*22, py + CELL_SIZE - 10],
                                   fill="#006600", outline="#222222")
                # Отель
                if prop.hotel:
                    draw.rectangle([px + 10, py + CELL_SIZE - 50, px + 50, py + CELL_SIZE - 10],
                                   fill="#D2691E", outline="#222222")

    # 3. Нарисовать фишки игроков (аватарка или круг)
    for idx, player in enumerate(game.players):
        px, py = board.get_coords(player.position)
        avatar_img = get_avatar_image(player.avatar_url, size=56)
        img.paste(avatar_img, (px + CELL_SIZE//2 - 28, py + CELL_SIZE//2 - 28), avatar_img)
        # Обводка фишки
        draw.ellipse([px + CELL_SIZE//2 - 30, py + CELL_SIZE//2 - 30,
                      px + CELL_SIZE//2 + 30, py + CELL_SIZE//2 + 30],
                     outline=PLAYER_COLORS[idx % len(PLAYER_COLORS)], width=4)

    # 4. Нарисовать баланс игроков снизу
    try:
        font = ImageFont.truetype(font_path, 24)
    except Exception:
        font = ImageFont.load_default()
    y_panel = BOARD_SIZE - 60
    for idx, player in enumerate(game.players):
        text = f"@{player.username}: {player.balance}₽"
        draw.text((20 + idx*220, y_panel), text,
                  fill=PLAYER_COLORS[idx % len(PLAYER_COLORS)], font=font)

    # 5. Нарисовать очередь/ход
    cp = game.get_current_player()
    if cp:
        draw.text((BOARD_SIZE//2 - 160, BOARD_SIZE - 30),
                  f"Ход игрока: @{cp.username}", fill="#222222", font=font)

    return img

def save_board_image(img, path):
    img.save(path, "PNG")

def get_board_image_bytes(img):
    """Вернуть картинку в байтах для отправки через Telegram API"""
    bio = BytesIO()
    img.save(bio, format="PNG")
    bio.seek(0)
    return bio