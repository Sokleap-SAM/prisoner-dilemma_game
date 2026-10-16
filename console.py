import getpass
import os
import sys


class Console:
    """Reads what the user types and prints headings and tables."""

    def clear(self):
        """Clear the screen: 'cls' on Windows, 'clear' on Mac/Linux."""
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")

    def read_text(self, prompt, hidden=False):
        """Read one line of text. With hidden=True, the typing is not shown."""
        # getpass only works with a real keyboard. When the input comes from a
        # file (for example in automated tests), use normal input() instead.
        if hidden and sys.stdin.isatty():
            return getpass.getpass(prompt)
        return input(prompt)

    def ask_number(self, prompt, lowest, highest):
        """Keep asking until the user types a number from lowest to highest, or 0.

        Returns the number. 0 means "go back".
        """
        hint = f"Please type a number from {lowest} to {highest}, or 0 to go back."
        while True:
            text = input(prompt).strip()
            if text == "0":
                return 0
            if text == "":
                print(f"  Nothing was entered. {hint}")
                continue
            try:
                number = int(text)
            except ValueError:
                print(f"  '{text}' is not a whole number. {hint}")
                continue
            if lowest <= number <= highest:
                return number
            print(f"  {number} is out of range. {hint}")

    def ask_menu(self, title, options, back_text):
        """Show the options as a numbered list, plus "0. <back_text>".

        Returns the number the user picked. 0 means "go back".
        """
        print(f"\n{title}")
        for number, option in enumerate(options, start=1):
            print(f"  {number}. {option}")
        print(f"  0. {back_text}")
        return self.ask_number("Your choice: ", 1, len(options))

    def ask_yes_no(self, prompt):
        """Keep asking until the user types y or n. Returns True for yes."""
        while True:
            answer = input(prompt).strip().lower()
            if answer in ("y", "yes"):
                return True
            if answer in ("n", "no"):
                return False
            print("  Invalid answer. Please type y (yes) or n (no).")

    def print_heading(self, text, line_character="="):
        line = line_character * 70
        print()
        print(line)
        print(text.center(70))
        print(line)

    def print_table(self, headers, rows, footer=None):
        """Print a table with borders. Each row is a list with one value per column.
        The optional footer is an extra row printed below a line, e.g. totals."""
        all_rows = [headers] + rows
        if footer:
            all_rows.append(footer)

        # Each column is as wide as the longest value in it.
        widths = []
        for column in range(len(headers)):
            longest = 0
            for row in all_rows:
                longest = max(longest, len(str(row[column])))
            widths.append(longest)

        border = "+"
        for width in widths:
            border += "-" * (width + 2) + "+"

        print(border)
        print(self.make_row(headers, widths))
        print(border)
        for row in rows:
            print(self.make_row(row, widths))
        if footer:
            print(border)
            print(self.make_row(footer, widths))
        print(border)

    def make_row(self, row, widths):
        """Turn one row into text like '|  C  |  3  |', centring each value."""
        text = "|"
        for value, width in zip(row, widths):
            text += " " + str(value).center(width) + " |"
        return text
