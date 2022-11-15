
"""
    Name: Caspar Grevelhörster
    Date: 22 11 2020
    Assignment name: Snake
"""

from ipy_lib3 import SnakeUserInterface


class Coordinate:
    def __init__(self, list_of_x_and_y):
        self.x = int(list_of_x_and_y[0])
        self.y = int(list_of_x_and_y[1])
        self.x_and_y = [self.x, self.y]


class CoordinateRow:
    def __init__(self, row):
        self.row = row

    def add_element(self, element, index=-1):
        self.row.insert(index, element)

    def delete_last_element(self):
        self.row.pop()

    def len(self):
        return len(self.row)


class SnakeEngine:
    def __init__(self, ui):
        self.direction = INITIAL_DIRECTION
        self.body_parts_list = CoordinateRow([Coordinate(INITIAL_HEAD), Coordinate(INITIAL_BODY)])
        self.wall_parts_list = CoordinateRow([])
        self.food_position = None
        self.ui = ui

    def next_head_state(self, current_head_x_and_y):
        current_x, current_y = current_head_x_and_y[0], current_head_x_and_y[1]
        moved_x, moved_y = current_x, current_y

        if self.direction == "r":
            moved_x = current_x + 1
        if self.direction == "l":
            moved_x = current_x - 1
        if self.direction == "d":
            moved_y = current_y + 1
        if self.direction == "u":
            moved_y = current_y - 1

        moved_x = moved_x % WINDOW_LENGTH
        moved_y = moved_y % WINDOW_HEIGHT

        new_head_coordinate = Coordinate([moved_x, moved_y])

        for body_part in self.body_parts_list.row:
            if body_part.x_and_y == new_head_coordinate.x_and_y:
                self.snake_death()
        for wall_part in self.wall_parts_list.row:
            if wall_part.x_and_y == new_head_coordinate.x_and_y:
                self.snake_death()

        return new_head_coordinate

    def next_snake_state(self):
        if self.food_position is None:
            self.place_food()
        new_head_position = self.next_head_state(self.body_parts_list.row[0].x_and_y)
        self.body_parts_list.add_element(new_head_position, 0)

        if new_head_position.x_and_y == self.food_position.x_and_y:
            self.place_food()
        else:
            self.body_parts_list.delete_last_element()

    def place_food(self):
        food_x = self.ui.random(WINDOW_LENGTH)
        food_y = self.ui.random(WINDOW_HEIGHT)
        self.food_position = Coordinate([food_x, food_y])
        for coordinate in self.body_parts_list.row:
            if self.food_position.x_and_y == coordinate.x_and_y:
                self.place_food()
        for coordinate in self.wall_parts_list.row:
            if self.food_position.x_and_y == coordinate.x_and_y:
                self.place_food()

    def snake_death(self):
        self.ui.clear()
        self.ui.clear_text()
        self.ui.print_(f"Snake dead at length {self.body_parts_list.len()} :(\nTo restart, press 0.")

        self.direction = "r"
        self.body_parts_list = CoordinateRow([Coordinate(INITIAL_HEAD), Coordinate(INITIAL_BODY)])
        self.wall_parts_list = CoordinateRow([])
        self.food_position = None

        while True:
            if self.ui.get_event().data == "0":
                self.ui.clear_text()
                main()


FPS = 10
WINDOW_LENGTH = 32
WINDOW_HEIGHT = 24
INITIAL_BODY = [0, 0]
INITIAL_HEAD = [1, 0]
INITIAL_DIRECTION = "r"

FOOD_COLOR = 1
BODY_COLOR = 2
WALL_COLOR = 3

snake = SnakeEngine(SnakeUserInterface(WINDOW_LENGTH, WINDOW_HEIGHT))


def main():
    snake.ui.print_(
        "You don't want to play with levels? Press 0\nWhich level do you want to play? Press a number from 1 to 4"
    )
    while True:
        key_input = snake.ui.get_event()
        if key_input.name == "number":
            level_number = int(key_input.data)
            if level_number in [1, 2, 3, 4]:
                create_level(level_number)
                snake.ui.clear_text()
                break
            elif level_number == 0:
                snake.ui.clear_text()
                break

    snake.ui.set_animation_speed(FPS)
    while True:
        process_event(snake.ui.get_event())


def create_level(desired_level):
    required_file_name = f"SnakeInput{desired_level}.txt"
    with open(required_file_name) as file:
        all_lines = [x.strip() for x in file.readlines()]

    second_line_arguments = all_lines[1].split("=")
    head_part_coordinate = list(map(int, all_lines[0].split(" ")))
    body_part_coordinate = list(map(int, second_line_arguments[0].split(" ")))
    first_wall_coordinate = list(map(int, second_line_arguments[-1].split(" ")))

    snake.direction = second_line_arguments[1].lower()
    snake.body_parts_list = CoordinateRow([Coordinate(head_part_coordinate), Coordinate(body_part_coordinate)])

    snake.wall_parts_list.add_element(Coordinate(first_wall_coordinate))
    for i in range(2, len(all_lines)):
        snake.wall_parts_list.add_element(Coordinate(list(map(int, all_lines[i].split(" ")))))


def draw_screen():
    for snake_part in snake.body_parts_list.row:
        snake.ui.place(snake_part.x, snake_part.y, BODY_COLOR)
    for wall_part in snake.wall_parts_list.row:
        snake.ui.place(wall_part.x, wall_part.y, WALL_COLOR)
    if snake.food_position is not None:
        snake.ui.place(snake.food_position.x, snake.food_position.y, FOOD_COLOR)


def process_event(event):
    if event.name == "alarm":
        snake.ui.clear()
        snake.next_snake_state()
        draw_screen()
        snake.ui.show()
    if event.name == "arrow":
        snake.direction = event.data


if __name__ == "__main__":
    main()
