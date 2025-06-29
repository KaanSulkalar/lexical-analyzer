import re

class Token:
    def __init__(self, token_type, value):
        self.token_type = token_type
        self.value = value

    def __str__(self):
        return f"<{self.token_type},{self.value}>"

symbol_table = []

class Lexer:
    def __init__(self, file_path):
        with open(file_path, 'r') as f:
            self.text = f.read()
        self.position = 0
        self.length = len(self.text)

    def skip_whitespace(self):
        while self.position < self.length and self.text[self.position].isspace():
            self.position += 1

    def next_token(self):
        self.skip_whitespace()
        if self.position >= self.length:
            return None

        if self.text.startswith('&&', self.position):
            self.position += 2
            return Token("LOGICAL_AND", "nothing")
        elif self.text.startswith('&', self.position):
            self.position += 1
            return Token("BITWISE_AND", "nothing")
        elif self.text.startswith('||', self.position):
            self.position += 2
            return Token("LOGICAL_OR", "nothing")
        elif self.text.startswith("|", self.position):
            self.position += 1
            return Token("BITWISE_OR", "nothing")

        created_pattern = r'[+-]?\d+\.\d+|[+-]?\d+|[A-Za-z_][A-Za-z0-9_]*'
        is_match = re.match(created_pattern, self.text[self.position:])
        if is_match:
            lexeme = is_match.group(0)
            self.position += len(lexeme)
            if re.fullmatch(r'[+-]?\d+\.\d+', lexeme):
                return Token("FLOAT", float(lexeme))
            elif re.fullmatch(r'[+-]?\d+', lexeme):
                return Token("INTEGER", int(lexeme))
            elif re.fullmatch(r'[A-Za-z_][A-Za-z0-9_]*', lexeme):
                if lexeme not in symbol_table:
                    symbol_table.append(lexeme)
                return Token("ID", symbol_table.index(lexeme))
        else:
            start = self.position
            while self.position < self.length and not self.text[self.position].isspace():
                self.position += 1
            return Token("ERROR", f'"{self.text[start:self.position]}"')

def main():
    filename = input("Enter input file name: ")
    lexer = Lexer(filename)

    while True:
        print("\nMenu:\n1. Call lex()\n2. Show symbol table\n3. Exit")
        choice = input("Enter your choice: ")
        if choice == '1':
            token = lexer.next_token()
            if token:
                print(token)
            else:
                print("End of input reached.")
        elif choice == '2':
            if not symbol_table:
                print("Symbol Table is empty.")
            else:
                print("Symbol Table:")
                for i, sym in enumerate(symbol_table):
                    print(f"{i}: {sym}")
        elif choice == '3':
            print("Exiting...")
            break
        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main()
