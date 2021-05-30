from core.board import Board
from core.rule import Rule


class Project:

    def __init__(self, name, board, colors):
        self.name = name
        self.board = board
        self.colors = colors

    @staticmethod
    def open(path):

        if not path.endswith(".life"):
            raise Exception("Bad file format")

        with open(path, "r") as file:

            name = file.readline()[:-1]

            width, height = map(lambda string: int(string), file.readline().split())

            bs = file.readline()[:-1]
            rule = Rule.from_bs_notation(bs)

            live_color, dead_color = file.readline().split()

            board = Board(width, height, rule)

            for i in range(height):
                row = file.readline()[:-1]
                for j in range(width):
                    board[j, i] = row[j] == '1'

            return Project(name, board, {"life": live_color, "dead": dead_color})

    @staticmethod
    def save(project, path):

        if not path.endswith(".life"):
            path += ".life"

        with open(path, 'w') as file:

            file.write(project.name + '\n')
            file.write(f"{project.board.width} {project.board.height}\n")
            file.write(project.board.rule.bs_notation + '\n')

            live_color, dead_color = project.colors["life"], project.colors["dead"]
            file.write(f"{live_color} {dead_color}\n")

            for row in project.board.view:
                file.write("".join(map(lambda item: '1' if item else '0', row)) + '\n')

            file.close()

    @staticmethod
    def export(path):
        pass
