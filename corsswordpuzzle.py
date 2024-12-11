import random

class Crossword:
    def __init__(self, size):
        self.size = size
        self.grid = [['-' for _ in range(size)] for _ in range(size)]
        self.words = []

    def add_word(self, word):
        self.words.append(word.upper())

    def generate_grid(self):
        for word in self.words:
            if not self.place_word(word):
                print(f"Could not place the word: {word}")

    def place_word(self, word):
        attempts = 100
        word_length = len(word)
        for _ in range(attempts):
            row = random.randint(0, self.size - 1)
            col = random.randint(0, self.size - 1)
            direction = random.choice([(0, 1), (1, 0)])

            if self.can_place_word(word, row, col, direction):
                self.do_place_word(word, row, col, direction)
                return True
        return False

    def can_place_word(self, word, row, col, direction):
        for i in range(len(word)):
            r, c = row + i * direction[0], col + i * direction[1]
            if r >= self.size or c >= self.size or (self.grid[r][c] != '-' and self.grid[r][c] != word[i]):
                return False
        return True

    def do_place_word(self, word, row, col, direction):
        for i in range(len(word)):
            r, c = row + i * direction[0], col + i * direction[1]
            self.grid[r][c] = word[i]

    def display_grid(self):
        for row in self.grid:
            print(' '.join(row))

    def solve(self, word):
        word = word.upper()
        for row in self.grid:
            if word in ''.join(row):
                return True

        for col in range(self.size):
            column = ''.join(self.grid[row][col] for row in range(self.size))
            if word in column:
                return True

        return False

if __name__ == "__main__":
    crossword = Crossword(10)

    crossword.add_word("APPLE")
    crossword.add_word("banana")
    crossword.add_word("grape")
    crossword.add_word("orange")

    crossword.generate_grid()

    print("Crossword Puzzle:")
    crossword.display_grid()

    print("\nSolve: Searching for 'apple'")
    print("Found" if crossword.solve("apple") else "Not Found")

    print("\nSolve: Searching for 'pear'")
    print("Found" if crossword.solve("pear") else "Not Found")
