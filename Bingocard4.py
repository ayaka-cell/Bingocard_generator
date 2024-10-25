import tkinter as tk
import random
import hashlib

class BingoCard:
    def __init__(self):
        self.card = self.generate_card()
        self.selected_numbers = set()
        self.checksum = self.generate_checksum()

    def generate_card(self):
        card = []
        ranges = [
            range(1, 16),
            range(16, 31),
            range(31, 46),
            range(46, 61),
            range(61, 76)
        ]
        
        for i in range(5):
            column_numbers = random.sample(ranges[i], 5 if i != 2 else 4)
            card.append(column_numbers)
        
        card[2].insert(2, 'FREE')  # 中央のフリースポット
        return card

    # パターン被りチェックサム(sha256)
    def generate_checksum(self):
        card_str = ''.join(str(num) for col in self.card for num in col if num != 'FREE')
        return hashlib.sha256(card_str.encode()).hexdigest()

    def select_number(self, number):
        if number in self.selected_numbers:
            self.selected_numbers.remove(number)
        else:
            self.selected_numbers.add(number)

    # ビンゴチェック
    def check_bingo(self):
        for row in range(5):
            if all(num in self.selected_numbers or num == 'FREE' for num in [self.card[col][row] for col in range(5)]):
                return True
        
        for col in range(5):
            if all(num in self.selected_numbers or num == 'FREE' for num in self.card[col]):
                return True

        if all(self.card[i][i] in self.selected_numbers or self.card[i][i] == 'FREE' for i in range(5)):
            return True
        
        if all(self.card[i][4 - i] in self.selected_numbers or self.card[i][4 - i] == 'FREE' for i in range(5)):
            return True
        
        return False

    # リーチチェック
    def check_reach(self):
        reach_count = 0
        
        for row in range(5):
            if sum(num in self.selected_numbers for num in [self.card[col][row] for col in range(5)]) >= 4:
                reach_count += 1
        
        for col in range(5):
            if sum(num in self.selected_numbers for num in self.card[col]) >= 4:
                reach_count += 1

        if sum(self.card[i][i] in self.selected_numbers for i in range(5)) >= 4:
            reach_count += 1
        
        if sum(self.card[i][4 - i] in self.selected_numbers for i in range(5)) >= 4:
            reach_count += 1
        
        return reach_count > 0




class BingoApp:
    def __init__(self, master):
        self.master = master
        master.title("Bingo Card")
        master.config(bg='lightpink')

        self.bingo_card = BingoCard()

        self.buttons = []
        self.create_buttons()

        self.result_label = tk.Label(master, text="", bg='lightpink')
        self.result_label.grid(row=6, columnspan=5)

        self.next_card_button = tk.Button(master, text="次のカード", command=self.next_card)
        self.next_card_button.grid(row=7, columnspan=5)

    def create_buttons(self):
        for row in range(5):
            button_row = []
            for col in range(5):
                number = self.bingo_card.card[col][row]
                button = tk.Button(self.master, text=str(number), width=5, height=2)
                button.config(command=lambda num=number, btn=button: self.on_button_click(num, btn))
                button.grid(row=row, column=col)
                button_row.append(button)
            self.buttons.append(button_row)

    def on_button_click(self, number, button):
        self.bingo_card.select_number(number)
        button.config(bg='gray')
        self.check_result()

    def check_result(self):
        if self.bingo_card.check_bingo():
            self.result_label.config(text="Bingo!")
        elif self.bingo_card.check_reach():
            self.result_label.config(text="リーチ！")
        else:
            self.result_label.config(text="")

    def next_card(self):
        self.bingo_card = BingoCard()  # 新しいビンゴカードを生成
        self.bingo_card.selected_numbers = set()  # 選択された番号のリセット
        self.result_label.config(text="")  # 結果ラベルのリセット
        self.update_buttons()  # ボタンの表示を更新

    def update_buttons(self):
        for row in range(5):
            for col in range(5):
                number = self.bingo_card.card[col][row]
                self.buttons[row][col].config(text=str(number), bg='SystemButtonFace')  # ボタンのテキストと色をリセット
                # ボタンがクリックされたときのコールバックを再設定
                self.buttons[row][col].config(command=lambda num=number, btn=self.buttons[row][col]: self.on_button_click(num, btn))

if __name__ == "__main__":
    root = tk.Tk()
    app = BingoApp(root)
    root.mainloop()
