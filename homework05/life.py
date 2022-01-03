import pathlib
import random
import typing as tp
from copy import deepcopy

import pygame
from pygame.locals import *

Cell = tp.Tuple[int, int]
Cells = tp.List[int]
Grid = tp.List[Cells]


class GameOfLife:
    def __init__(
        self,
        size: tp.Tuple[int, int],
        randomize: bool = True,
        max_generations: tp.Optional[float] = float("inf"),
    ) -> None:
        # Размер клеточного поля
        self.rows, self.cols = size
        # Предыдущее поколение клеток
        self.prev_generation = self.create_grid()
        # Текущее поколение клеток
        self.curr_generation = self.create_grid(randomize=randomize)
        # Максимальное число поколений
        self.max_generations = max_generations
        # Текущее число поколений
        self.generations = 1

    def create_grid(self, randomize: bool = False) -> Grid:
        """
        Создание списка клеток.
        Клетка считается живой, если ее значение равно 1, в противном случае клетка
        считается мертвой, то есть, ее значение равно 0.
        Parameters
        ----------
        randomize : bool
            Если значение истина, то создается матрица, где каждая клетка может
            быть равновероятно живой или мертвой, иначе все клетки создаются мертвыми.
        Returns
        ----------
        out : Grid
            Матрица клеток размером `cell_height` х `cell_width`.
        """
        if not randomize:
            Grid = [[0 for i in range(self.cols)] for p in range(self.rows)]
            return Grid
        Grid = [[random.choice([0, 1]) for i in range(self.cols)] for p in range(self.rows)]
        return Grid

    def get_neighbours(self, cell: Cell) -> Cells:
        """
        Вернуть список соседних клеток для клетки `cell`.
        Соседними считаются клетки по горизонтали, вертикали и диагоналям,
        то есть, во всех направлениях.
        Parameters
        ----------
        cell : Cell
            Клетка, для которой необходимо получить список соседей. Клетка
            представлена кортежем, содержащим ее координаты на игровом поле.
        Returns
        ----------
        out : Cells
            Список соседних клеток.
        """
        row, col = cell
        cells = []
        if col > 0:
            cells.append(self.curr_generation[row][col - 1])
            if row > 0:
                cells.append(self.curr_generation[row - 1][col - 1])
            if row < (self.rows - 1):
                cells.append(self.curr_generation[row + 1][col - 1])
        if col < (self.cols - 1):
            cells.append(self.curr_generation[row][col + 1])
            if row > 0:
                cells.append(self.curr_generation[row - 1][col + 1])
            if row < (self.rows - 1):
                cells.append(self.curr_generation[row + 1][col + 1])
        if row > 0:
            cells.append(self.curr_generation[row - 1][col])
        if row < (self.rows - 1):
            cells.append(self.curr_generation[row + 1][col])
        return cells

    def get_next_generation(self) -> Grid:
        """
        Получить следующее поколение клеток.
        Returns
        ----------
        out : Grid
            Новое поколение клеток.
        """
        grid = deepcopy(self.curr_generation)
        alive = []
        dead = []
        for i in range(self.rows):
            for j in range(self.cols):
                summ = sum(self.get_neighbours((i, j)))
                if summ == 3 and self.curr_generation[i][j] == 0:
                    alive.append([i, j])
                elif summ < 2 or summ > 3:
                    dead.append([i, j])

        for pair in alive:
            grid[pair[0]][pair[1]] = 1
        for pair in dead:
            grid[pair[0]][pair[1]] = 0
        return grid

    def step(self) -> None:
        """
        Выполнить один шаг игры.
        """
        self.prev_generation = deepcopy(self.curr_generation)
        self.curr_generation = self.get_next_generation()
        self.generations += 1

    @property
    def is_max_generations_exceeded(self) -> bool:
        """
        Не превысило ли текущее число поколений максимально допустимое.
        """
        if self.max_generations:
            if self.generations < self.max_generations:
                return False
            return True

    @property
    def is_changing(self) -> bool:
        """
        Изменилось ли состояние клеток с предыдущего шага.
        """
        if self.curr_generation == self.prev_generation:
            return False
        return True

    @staticmethod
    def from_file(filename) -> "GameOfLife":
        """
        Прочитать состояние клеток из указанного файла. 
        """
        with open(filename, "r") as f:
            line = f.readlines()
            game = GameOfLife((len(line), len(line[0].strip())), False)
            for i in range(len(line)):
                line[i].strip()
                for j in range(len(line[0].strip())):
                    game.curr_generation[i][j] = int(line[i][j])
        return game

    def save(self, filename) -> None:
        """
        Сохранить текущее состояние клеток в указанный файл. 
        """
        with open(filename, "w") as f:
            for row in self.curr_generation:
                f.write("".join([str(chr) for chr in row]) + "\n")
        return
