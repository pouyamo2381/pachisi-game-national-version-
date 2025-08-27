import json

def save_game(filename, game_settings, current_player, dice_value,
              can_roll_again, pieces_at_home_count, all_pieces):
    save_data = {
        "schema_version": 1,
        "game_settings": game_settings,
        "current_player": current_player,
        "dice_value": dice_value,
        "can_roll_again": can_roll_again,
        "pieces_at_home_count": pieces_at_home_count,
        "pieces": []
    }

    for p in all_pieces:
        save_data["pieces"].append({
            "player_id": p.player_id,
            "piece_id": p.piece_id,
            "logical_pos": list(p.logical_pos) if p.logical_pos is not None else None,
            "in_base": p.in_base,
            "on_path": p.on_path,
            "in_final_path": p.in_final_path,
            "is_home": p.is_home,
            "steps_on_main_path": p.steps_on_main_path,
            "steps_on_final_path": p.steps_on_final_path,
        })

    with open(filename, "w") as f:
        json.dump(save_data, f, indent=4)
    print(f"Game saved to {filename}")


def load_game(filename):
    with open(filename, "r") as f:
        save_data = json.load(f)

    # فقط دادهٔ خام را برگردان؛ ساخت آبجکت‌ها را بگذار به فایل اصلی
    return (
        save_data["game_settings"],
        save_data["current_player"],
        save_data["dice_value"],
        save_data["can_roll_again"],
        save_data["pieces_at_home_count"],
        save_data["pieces"],  # لیست دیکشنری‌های مهره‌ها
        save_data.get("schema_version", 1)
    )
