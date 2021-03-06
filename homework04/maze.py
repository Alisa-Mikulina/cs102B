from copy import deepcopy
from random import choice, randint
from typing import List, Optional, Tuple, Union


def create_grid(rows: int = 15, cols: int = 15) -> List[List[Union[str, int]]]:
    return [["■"] * cols for _ in range(rows)]


def remove_wall(
    grid: List[List[Union[str, int]]], coord: Tuple[int, int]
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param coord:
    :return:
    """

    if grid[coord[0]][coord[1]] != " ":
        grid[coord[0]][coord[1]] = " "
    elif coord[1] + 1 < len(grid[0]) - 1:
        grid[coord[0]][coord[1] + 1] = " "
    elif coord[0] - 1 > 1:
        grid[coord[0] - 1][coord[1]] = " "
    return grid


def bin_tree_maze(
    rows: int = 15, cols: int = 15, random_exit: bool = True
) -> List[List[Union[str, int]]]:
    """

    :param rows:
    :param cols:
    :param random_exit:
    :return:
    """

    grid = create_grid(rows, cols)
    empty_cells = []
    for x, row in enumerate(grid):
        for y, _ in enumerate(row):
            if x % 2 == 1 and y % 2 == 1:
                grid[x][y] = " "
                empty_cells.append((x, y))

    # 1. выбрать любую клетку
    # 2. выбрать направление: наверх или направо.
    # Если в выбранном направлении следующая клетка лежит за границами поля,
    # выбрать второе возможное направление
    # 3. перейти в следующую клетку, сносим между клетками стену
    # 4. повторять 2-3 до тех пор, пока не будут пройдены все клетки

    # генерация входа и выхода

    random_action = [-1, 1]
    for row_cor in range(1, rows - 1, 2):
        for col_cor in range(1, cols - 1, 2):
            action = choice(random_action)
            if action == 1:
                if row_cor == 1:
                    if col_cor + 1 == cols - 1:
                        continue
                    remove_wall(grid, (row_cor, col_cor + 1))
                elif col_cor + 1 < cols - 1:
                    remove_wall(grid, (row_cor, col_cor + 1))
                elif col_cor - 1 <= cols - 1:
                    remove_wall(grid, (row_cor - 1, col_cor))
            else:
                if row_cor == 1:
                    if col_cor + 1 == cols - 1:
                        continue
                    remove_wall(grid, (row_cor, col_cor + 1))
                elif row_cor + 1 <= rows - 1:
                    remove_wall(grid, (row_cor - 1, col_cor))

    if random_exit:
        x_in, x_out = randint(0, rows - 1), randint(0, rows - 1)
        y_in = randint(0, cols - 1) if x_in in (0, rows - 1) else choice((0, cols - 1))
        y_out = randint(0, cols - 1) if x_out in (0, rows - 1) else choice((0, cols - 1))
    else:
        x_in, y_in = 0, cols - 2
        x_out, y_out = rows - 1, 1

    grid[x_in][y_in], grid[x_out][y_out] = "X", "X"

    return grid


def get_exits(grid: List[List[Union[str, int]]]) -> List[Tuple[int, int]]:
    """

    :param grid:
    :return:
    """

    ans = []
    rows = len(grid) - 1
    columns = len(grid[0]) - 1

    for i in range(columns):
        if grid[0][i] == "X":
            ans.append((0, i))
    for i in range(rows):
        if grid[i][0] == "X":
            ans.append((i, 0))

    if len(ans) != 2:
        for i in range(columns):
            if grid[rows][i] == "X":
                ans.append((rows, i))
        for i in range(rows):
            if grid[i][columns] == "X":
                ans.append((i, columns))
    if len(ans) > 1:
        if ans[0][1] > ans[1][1]:
            ans[0], ans[1] = ans[1], ans[0]
        if ans[0][0] > ans[1][0]:
            ans[0], ans[1] = ans[1], ans[0]

    return ans


def make_step(grid: List[List[Union[str, int]]], k: int) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param k:
    :return:
    """

    moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    to_visit = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == k:
                to_visit.append((i, j, k + 1))
    while to_visit != []:
        i, j = to_visit[0][0], to_visit[0][1]
        for x, y in moves:
            if 0 <= i + x < len(grid) and 0 <= j + y < len(grid[0]):
                if grid[i + x][j + y] == 0:
                    grid[i + x][j + y] = to_visit[0][2]
        to_visit.pop(0)
    return grid


def shortest_path(
    grid: List[List[Union[str, int]]], exit_coord: Tuple[int, int]
) -> Optional[Union[Tuple[int, int], List[Tuple[int, int]]]]:
    """

    :param grid:
    :param exit_coord:
    :return:
    """
    x = exit_coord[0]
    y = exit_coord[1]
    k = grid[x][y]
    moves = [[0, 1], [0, -1], [1, 0], [-1, 0]]
    way = []
    way.append((x, y))
    while k != 1:
        for a, b in moves:
            if 0 <= x + a < len(grid) and 0 <= y + b < len(grid[0]):
                temp = grid[x + a][y + b]
                if isinstance(temp, int):
                    if temp < int(k):
                        x, y = x + a, y + b
                        way.append((x, y))
                        k = grid[x][y]

    for i in range(len(grid) - 1):
        for j in range(len(grid[0])):
            if grid[i][j] != "■":
                grid[i][j] = " "

    return way


def encircled_exit(grid: List[List[Union[str, int]]], coord: Tuple[int, int]) -> bool:
    """

    :param grid:
    :param coord:
    :return:
    """

    ans = False

    if (
        coord == (0, 0)
        or coord == (len(grid) - 1, len(grid[0]) - 1)
        or coord == (len(grid) - 1, 0)
        or coord == (0, len(grid[0]) - 1)
    ):
        ans = True
    elif coord[0] == 0:
        if grid[1][coord[1]] != " ":
            ans = True

    elif coord[1] == 0:
        if grid[coord[0]][1] != " ":
            ans = True

    elif coord[0] == len(grid) - 1:
        if grid[len(grid) - 2][coord[1]] != " ":
            ans = True

    elif coord[1] == len(grid[0]) - 1:
        if grid[coord[0]][len(grid[0]) - 2] != " ":
            ans = True
    return ans


def solve_maze(grid):
    """

    :param grid:
    :return:
    """

    exits = get_exits(grid)
    if len(exits) < 2:
        return grid, exits[0]
    else:
        for exit in exits:
            if encircled_exit(grid, exit):
                return None, None
    enter = exits[0]
    exit = exits[1]
    if exit[1] - enter[1] == 1 and exit[0] - enter[0] == 0:
        return grid, exits[::-1]
    elif exit[1] - enter[1] == 0 and exit[0] - enter[0] == 1:
        return grid, exits[::-1]
    elif exit[0] - enter[0] == 0 and exit[1] - enter[1] == 1:
        return grid, exits[::-1]
    elif exit[0] - enter[0] == 1 and exit[1] - enter[1] == 0:
        return grid, exits[::-1]

    grid[exits[0][0]][exits[0][1]] = 1
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == " ":
                grid[i][j] = 0
            elif grid[i][j] == "X":
                grid[i][j] = 0

    k = 1
    while grid[exits[1][0]][exits[1][1]] == 0:
        grid = make_step(grid, k)
        k += 1

    path = shortest_path(grid, exits[1])

    return grid, path


def add_path_to_grid(
    grid: List[List[Union[str, int]]],
    path: Optional[Union[Tuple[int, int], List[Tuple[int, int]]]],
) -> List[List[Union[str, int]]]:
    """

    :param grid:
    :param path:
    :return:
    """

    if path:
        for i, row in enumerate(grid):
            for j, _ in enumerate(row):
                if (i, j) in path:
                    grid[i][j] = "X"
    return grid
