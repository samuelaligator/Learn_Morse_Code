import random
import json
import asyncio
import toga
from toga.style import Pack
from toga.style.pack import COLUMN, ROW


class LearnMorse(toga.App):

    def startup(self):
        self.morse_code = {
            'A': '.-', 'B': '-...', 'C': '-.-.', 'D': '-..', 'E': '.', 'F': '..-.', 'G': '--.', 'H': '....',
            'I': '..', 'J': '.---', 'K': '-.-', 'L': '.-..', 'M': '--', 'N': '-.', 'O': '---', 'P': '.--.',
            'Q': '--.-', 'R': '.-.', 'S': '...', 'T': '-', 'U': '..-', 'V': '...-', 'W': '.--', 'X': '-..-',
            'Y': '-.--', 'Z': '--..',

            '0': '-----', '1': '.----', '2': '..---', '3': '...--', '4': '....-', '5': '.....',
            '6': '-....', '7': '--...', '8': '---..', '9': '----.',

            '.': '.-.-.-', ',': '--..--', '?': '..--..', '/': '-..-.', '(': '-.--.',
            ')': '-.--.-', ':': '---...', ';': '-.-.-.', '=': '-...-', '+': '.-.-.', '-': '-....-'
        }
        self.encode_selected_letter = random.choice(list(self.morse_code.keys()))
        self.decode_selected_letter = random.choice(list(self.morse_code.keys()))
        self.combination = []
        self.encode_counter = 0
        self.decode_counter = 0
        self.encode_best_series = 0
        self.decode_best_series = 0
        self.decode_see_again = False

        self.load_series_data()

        toga.Font.register("morse", "resources/morse.ttf")

        self.main_box = toga.Box(style=Pack(direction=COLUMN, padding=5, alignment="center"))
        self.header = toga.Box(style=Pack(direction=ROW, padding_top=5))
        self.div = toga.Box()
        self.canvas = toga.Canvas(style=Pack(flex=1, width=300, height=110, padding_top=20))

        self.button_style = Pack(height=50, padding_left=5, padding_right=5, width=100, background_color="white", color="black")
        self.button_active_style = Pack(height=50, padding_left=5, padding_right=5, width=100)
        self.series_style = Pack(font_size=15, font_weight="bold", padding_left=5, padding_right=5, height=50, color="#ff6961", background_color="white")
        self.series_active_style = Pack(font_size=15, font_weight="bold", padding_left=5, padding_right=5, height=50, color="#ff6961")


        self.mode1 = toga.Button("ENCODE", on_press=self.encode, style=self.button_style)
        self.series = toga.Button(str(self.encode_counter), on_press=self.show_stats, style=self.series_style)
        self.mode2 = toga.Button("DECODE", on_press=self.decode, style=self.button_style)
        logo = toga.Image("resources/LearnMorse.png")
        self.view_logo = toga.ImageView(logo, style=Pack(width=300))

        self.header.add(self.mode1, self.series, self.mode2)
        self.main_box.add(self.header, self.div, self.view_logo)

        self.main_window = toga.MainWindow(title="Learn Morse Code")
        self.main_window.content = self.main_box
        self.main_window.show()

    def encode(self, widget):
        self.switch_mode("encode")
        self.mode1_template("black", "serif")

    def show_stats(self, widget):
        self.switch_mode("stats")
        self.mode2_template()

    def decode(self, widget):
        self.switch_mode("decode")
        self.mode3_template()

    def switch_mode(self, selection):
        button1 = self.button_style
        button2 = self.series_style
        button3 = self.button_style

        if selection == "encode":
            button1 = self.button_active_style
            number = str(self.encode_counter)
        elif selection == "stats":
            button2 = self.series_active_style
            number = ""
        else:
            button3 = self.button_active_style
            number = str(self.decode_counter)

        self.header.remove(self.mode1, self.mode2, self.series)
        self.mode1 = toga.Button("ENCODE", on_press=self.encode, style=button1)
        self.series = toga.Button(number, on_press=self.show_stats, style=button2)
        self.mode2 = toga.Button("DECODE", on_press=self.decode, style=button3)

        self.header.add(self.mode1, self.series, self.mode2)

        self.main_box.remove(self.div, self.view_logo)

    def mode1_template(self, letter_color, letter_family, letter_weight="bold"):

        self.main_box.remove(self.div, self.canvas)

        self.div = toga.Box(style=Pack(direction=COLUMN, alignment="center", padding_top="10"))
        section = toga.Box(style=Pack(direction=ROW))

        self.letter = toga.Label(self.encode_selected_letter, style=Pack(font_size=75, font_family=letter_family, font_weight=letter_weight, text_align="center", color=letter_color))

        button_style = Pack(font_size=60, font_family="morse", width=140, height=110, padding_left=5, padding_right=5)
        dot_button = toga.Button("E", on_press=self.dot, style=button_style)
        line_button = toga.Button("T", on_press=self.line, style=button_style)

        section.add(dot_button, line_button)
        self.div.add(self.letter, section)
        self.main_box.add(self.div)

    def dot(self, widget):
        self.combination.append(".")
        self.check_combination()

    def line(self, widget):
        self.combination.append("-")
        self.check_combination()

    def check_combination(self):
        for i, value in enumerate(self.combination):
            if value != self.morse_code[self.encode_selected_letter][i]:
                self.lost_combination()
                break

        if ''.join(self.combination) == self.morse_code[self.encode_selected_letter]:
            self.successful_combination()

    def successful_combination(self):
        self.encode_selected_letter = random.choice(list(self.morse_code.keys()))
        self.combination = []
        self.encode_counter += 1

        self.switch_mode("encode")
        self.mode1_template("black", "serif")

        if self.encode_counter > self.encode_best_series:
            self.encode_best_series = self.encode_counter
            self.save_series_data()


    def lost_combination(self):
        self.combination = []
        self.encode_counter = 0

        self.switch_mode("encode")
        self.mode1_template("#ff6961", "morse", "normal")

    def mode2_template(self):
        self.main_box.remove(self.div, self.canvas)

        self.div = toga.Box(style=Pack(direction=COLUMN, padding_top="10"))

        title_style = Pack(font_size=23, font_weight="bold", padding_left=15, text_align="center")
        text_style = Pack(font_size=18, padding_left=30, text_align="center")

        encode = toga.Label("Encode", style=title_style)
        encode_series = toga.Label(f"Current series : {str(self.encode_counter)}", style=text_style)
        encode_best_series = toga.Label(f"Best series : {str(self.encode_best_series)}", style=text_style)

        empty_space = toga.Label("")

        decode = toga.Label("Decode", style=title_style)
        decode_series = toga.Label(f"Current series : {str(self.decode_counter)}", style=text_style)
        decode_best_series = toga.Label(f"Best series : {str(self.decode_best_series)}", style=text_style)

        self.div.add(encode, encode_series, encode_best_series, empty_space, decode, decode_series, decode_best_series)
        self.main_box.add(self.div)

    def load_series_data(self, filename="best_series.json"):
        file_path = self.app.paths.data / filename
        try:
            with open(file_path, 'r') as file:
                data = json.load(file)
            self.encode_best_series = data["encode"]
            self.decode_best_series = data["decode"]
        except FileNotFoundError:
            print("file not found")

    def save_series_data(self, filename="best_series.json"):
        best_series = {
            "encode": self.encode_best_series,
            "decode": self.decode_best_series
        }
        file_path = self.app.paths.data / filename

        # Create the directory if it doesn't exist
        file_path.parent.mkdir(parents=True, exist_ok=True)

        with open(file_path, 'w') as file:
            json.dump(best_series, file)

    def mode3_template(self):
        self.main_box.remove(self.div)

        self.loop.create_task(self.flashing())

        self.div = toga.Box(style=Pack(direction=COLUMN, padding_top="20", alignment="center"))

        self.input = toga.TextInput(placeholder="Type a letter", on_confirm=self.check_letter, style=Pack(width=180))
        button_see_again = toga.Button("See the code again", on_press=self.see_again, style=Pack(width=180, padding_top=10))

        self.div.add(self.input, button_see_again)

        self.main_box.add(self.canvas, self.div)

    async def flashing(self):
        self.decode_see_again = False
        for character in self.morse_code[self.decode_selected_letter]:
            self.draw_circle("black")
            await asyncio.sleep(0.2)

            self.draw_circle("#ff6961")
            if character == ".":
                await asyncio.sleep(0.2)
            else:
                await asyncio.sleep(0.6)

        self.draw_circle("black")
        self.decode_see_again = True

    def draw_circle(self, color):
        with self.canvas.Fill(color=color) as circle:
            circle.arc(x=150, y=55, radius=55)

    def see_again(self, widget):
        if self.decode_see_again == True:
            self.loop.create_task(self.flashing())

    def check_letter(self, widget):
        if self.input.value == self.decode_selected_letter or self.input.value == self.decode_selected_letter.lower():
            self.successful_letter()
        else:
            self.lost_letter()
        print(self.input.value)

    def successful_letter(self):
        self.decode_selected_letter = random.choice(list(self.morse_code.keys()))
        self.decode_counter += 1

        self.switch_mode("decode")
        self.mode3_template()

        if self.decode_counter > self.decode_best_series:
            self.decode_best_series = self.decode_counter
            self.save_series_data()


    def lost_letter(self):
        self.decode_counter = 0

        self.switch_mode("decode")
        self.lost_letter_template()

    def lost_letter_template(self):
        self.main_box.remove(self.div, self.canvas)

        self.div = toga.Box(style=Pack(direction=COLUMN, padding_top="20", alignment="center"))

        letter = toga.Label(self.decode_selected_letter, style=Pack(font_size=60, font_family="serif", font_weight="bold", text_align="center", color="#ff6961"))
        morse = toga.Label(self.decode_selected_letter, style=Pack(font_size=60, font_family="morse", text_align="center", color="#ff6961"))
        button_next = toga.Button("Next", on_press=self.decode, style=self.button_active_style)

        self.div.add(letter, morse, button_next)
        self.main_box.add(self.div)
        self.decode_selected_letter = random.choice(list(self.morse_code.keys()))


def main():
    return LearnMorse()
