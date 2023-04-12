import time
import ctypes

ATTACK_DELAY_SEC = 1.325  # 1.325 seconds between attacks
ATTACKS_PER_TRY = 3  # 3 attacks per try
X_OFFSET = 75  # 75 pixels to the right
DIRECTIONS = [-1] * 3 + [1] * 6 + [-1] * 3  # 3 left, 6 right, 3 left
TOTAL_TIME = "1h30"  # will run for 1 hour 30 minutes


def convert_time_str_to_seconds(time_str: str) -> int:
    time_str = time_str.lower().replace(" ", "")
    hour_idx = time_str.find("h")
    min_idx = time_str.find("m")
    if hour_idx == -1 and min_idx == -1:
        raise ValueError(
            "Invalid time string: Use 'h' or 'm' to indicate hours or minutes"
        )
    elif hour_idx == -1:
        minutes = int(time_str[:min_idx])
        return minutes * 60
    elif min_idx == -1:
        hours = int(time_str[:hour_idx])
        return hours * 3600
    else:
        hours = int(time_str[:hour_idx])
        minutes = int(time_str[hour_idx + 1 : min_idx])
        return hours * 3600 + minutes * 60


def attack() -> None:
    for direction in DIRECTIONS:
        ctypes.windll.user32.mouse_event(0x0001, X_OFFSET * direction, 0, 0, 0)
        ctypes.windll.user32.mouse_event(0x0002, 0, 0, 0, 0)
        ctypes.windll.user32.mouse_event(0x0004, 0, 0, 0, 0)
        time.sleep(ATTACK_DELAY_SEC)


def run(total_seconds: int) -> None:
    start_time = time.perf_counter()
    while time.perf_counter() - start_time < total_seconds:
        for _ in range(ATTACKS_PER_TRY):
            attack()


def main() -> None:
    total_seconds = convert_time_str_to_seconds(TOTAL_TIME)
    for i in range(5, 0, -1):
        print(f"Starting in {i} seconds...")
        time.sleep(1)
    run(total_seconds)


if __name__ == "__main__":
    main()
