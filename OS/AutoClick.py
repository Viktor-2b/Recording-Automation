import pyautogui
import time

# 中心点位置
center_x, center_y = 2100, 400  # 你可以根据屏幕分辨率调整这个值

# 点击间隔时间（秒）
click_interval = 0.5

# 移动周期时间（秒）
move_cycle_time = 5

# 计算每次移动的时间和距离
move_time = move_cycle_time / 4
move_distance = 100  # 假设每次移动100像素


def click_position(x, y):
    pyautogui.rightClick(x, y)
    print(f"Right clicked at ({x}, {y})")


def main():
    start_time = time.time()

    while True:
        elapsed_time = time.time() - start_time

        # 上方向
        if elapsed_time % move_cycle_time < move_time:
            click_position(center_x, center_y - move_distance)

        # 右方向
        elif elapsed_time % move_cycle_time < 2 * move_time:
            click_position(center_x + move_distance, center_y)

        # 下方向
        elif elapsed_time % move_cycle_time < 3 * move_time:
            click_position(center_x, center_y + move_distance)

        # 左方向
        else:
            click_position(center_x - move_distance, center_y)

        # 每隔 click_interval 进行一次点击
        time.sleep(click_interval)


if __name__ == "__main__":
    main()
