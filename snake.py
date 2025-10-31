import curses
import random

WINDOW_HEIGHT = 20
WINDOW_WIDTH = 40


def main(stdscr):
    curses.curs_set(0)
    stdscr.nodelay(True)
    stdscr.timeout(100)

    sh, sw = stdscr.getmaxyx()
    w = curses.newwin(WINDOW_HEIGHT, WINDOW_WIDTH, (sh - WINDOW_HEIGHT)//2, (sw - WINDOW_WIDTH)//2)
    w.keypad(True)
    w.border()

    snake = [
        (WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2 + 1),
        (WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2),
        (WINDOW_HEIGHT // 2, WINDOW_WIDTH // 2 - 1),
    ]
    direction = curses.KEY_RIGHT

    food = None
    while food is None or food in snake:
        food = (
            random.randint(1, WINDOW_HEIGHT - 2),
            random.randint(1, WINDOW_WIDTH - 2),
        )
    w.addch(food[0], food[1], "O")

    while True:
        next_key = w.getch()
        if next_key in [curses.KEY_UP, curses.KEY_DOWN, curses.KEY_LEFT, curses.KEY_RIGHT]:
            opposite = {curses.KEY_UP: curses.KEY_DOWN, curses.KEY_DOWN: curses.KEY_UP,
                        curses.KEY_LEFT: curses.KEY_RIGHT, curses.KEY_RIGHT: curses.KEY_LEFT}
            if next_key != opposite[direction]:
                direction = next_key
        elif next_key == ord('q'):
            break

        head_y, head_x = snake[0]
        if direction == curses.KEY_UP:
            head_y -= 1
        elif direction == curses.KEY_DOWN:
            head_y += 1
        elif direction == curses.KEY_LEFT:
            head_x -= 1
        elif direction == curses.KEY_RIGHT:
            head_x += 1

        if (
            head_y in [0, WINDOW_HEIGHT - 1]
            or head_x in [0, WINDOW_WIDTH - 1]
            or (head_y, head_x) in snake
        ):
            break

        snake.insert(0, (head_y, head_x))

        if (head_y, head_x) == food:
            while food in snake:
                food = (
                    random.randint(1, WINDOW_HEIGHT - 2),
                    random.randint(1, WINDOW_WIDTH - 2),
                )
            w.addch(food[0], food[1], "O")
        else:
            tail_y, tail_x = snake.pop()
            w.addch(tail_y, tail_x, " ")

        w.addch(head_y, head_x, "#")

    msg = f"Game Over! Score: {len(snake) - 3}"
    w.nodelay(False)
    w.addstr(WINDOW_HEIGHT // 2, (WINDOW_WIDTH - len(msg)) // 2, msg)
    w.getch()


if __name__ == "__main__":
    curses.wrapper(main)
