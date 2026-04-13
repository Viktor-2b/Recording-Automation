import pyautogui
import time
import sys


def auto_press_right():
    print("--- 自动按右键脚本 ---")
    print("功能：每隔 X 秒自动按下键盘的【右方向键】")
    print("退出方法：按 Ctrl+C 强制停止，或者将鼠标快速移动到屏幕四个角之一触发安全保护。\n")

    try:
        # 1. 间隔时间
        interval = float(1)

        # 2. 启动倒计时，给用户准备时间
        print("\n脚本将在 5 秒后开始运行...")
        print("请立刻切换到你需要操作的窗口！")
        for i in range(5, 0, -1):
            print(f"{i}...", end=" ", flush=True)
            time.sleep(1)
        print("\n\n>>> 开始运行！(按 Ctrl+C 停止) <<<")

        # 3. 循环按键
        count = 0
        while True:
            # 模拟按右键
            pyautogui.press('right')

            count += 1
            # 打印状态（在同一行刷新，保持整洁）
            sys.stdout.write(f"\r已按右键次数: {count} | 上次按键时间: {time.strftime('%H:%M:%S')}")
            sys.stdout.flush()

            # 等待
            time.sleep(interval)

    except KeyboardInterrupt:
        print("\n\n[已停止] 用户按下了 Ctrl+C，脚本结束。")
    except ValueError:
        print("\n[错误] 请输入有效的数字！")
    except pyautogui.FailSafeException:
        print("\n[紧急停止] 触发了 PyAutoGUI 的安全故障保护（鼠标移到了角落）。")


if __name__ == "__main__":
    auto_press_right()