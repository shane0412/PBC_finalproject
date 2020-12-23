# Connect Four
from tkinter import *
from tkinter import messagebox
import sys

# GUI介面 
class ConnectFour:
    def __init__(self, parent):
        self.labels = [] 
        self.count = 0 # 計算輪到誰 
        self.win_status = 0 # 當遊戲進行時為0，分出勝負時為1
        self.empty_image = PhotoImage(file = "picture/empty_try.gif")  # 未放入棋子的圖片
        self.yellow_image = PhotoImage(file = "picture/yellow_try.gif")  # 放入黃色棋子的圖片
        self.red_image = PhotoImage(file = "picture/red_try.gif")  # 放入紅色棋子的圖片
        # 格子長寬皆為100
        self.height = 100
        self.width = 100
        # 放入42格
        for i in range(42):
            self.labels.append(Label(parent,
                                     image = self.empty_image,
                                     bg = "blue",
                                     width = self.width,
                                     height = self.height))
        
        piece_index = 0  # 將每個格子標號
        for c in range(7):  # 從左到右編號 
            for r in range(6,0,-1): # 由下往上編號，因此step = -1
                self.labels[piece_index].grid(row = r, column = c)
                self.labels[piece_index].bind("<Button-1>", lambda event, coords = (r,c): self.column_click(event, coords))
                piece_index += 1
        self.button = Button(parent,text='Restart', width=10, command=self.Restart)
        self.button1 = Button(parent,text='Help', width=10, command=self.Help)
        self.label2 = Label(parent,text="Yellow's Turn", fg='#FEC200')
        self.button.grid(column=0, row=7)
        self.button1.grid(column=1, row=7)
        self.label2.grid(column=2, row=7)
    def Restart(self):
        MsgBox = messagebox.askquestion(title='Restart game?', message='Are you sure to restart?')
        if MsgBox == 'yes':
            for i in range(0,42):
                game.labels[i].grid_forget()
            game.__init__(root)
            yellow_win.__init__(root, "Winner is Yellow!")
            red_win.__init__(root, "Winner is Red!")
    def Help(self):
        self.help = Toplevel(root)
        self.help.title('Game Rule')
        self.help.geometry('350x100+450+250')
        labels=Label(self.help,
                     text ='遊戲規則\n1.玩家雙方輪流放入一枚棋子(以滑鼠點擊想放入之位子)\n2.棋盤為豎立的，故棋子會落至底部或其他棋子上。\n3.當任一方的棋子以縱、橫、斜任一方向連成四枚一線時，\n遊戲結束，連線一方獲勝。\n4.棋盤滿棋且無任一方連成4子，則以平手結束棋局')
        labels.pack()
    
    # 在同一個column中點擊都可以放入棋子
    def column_click(self, event, coords):
        print("Turn", game.count + 1, "request to column", coords[1])
        # 遊戲進行中都可以繼續點擊
        if game.win_status == 0:
            columns[coords[1]].drop_piece(coords[1])
            
    #update an individual piece
    def redraw(self, c_ord, r_ord, piece_state): 

        self.c_ord = c_ord
        self.r_ord = r_ord
        self.piece_state = piece_state

        piece_index = r_ord + 6 * c_ord #recalculate unique piece identifier from 0 to 42 by row and column

        if self.piece_state == 1:
            self.labels[piece_index].configure(image = self.yellow_image)
            self.label2.configure(text="Red's Turn", fg='red')
        elif self.piece_state == -1:
            self.labels[piece_index].configure(image = self.red_image)
            self.label2.configure(text="Yellow's Turn", fg='#FEC200')
        #print("Drawing to column", self.c_ord, "and row", self.r_ord)
        
    #check all possible positions for a win
    def judge(self):
        for i in range(len(columns)):
            print(columns[i].column)

        # 判斷行
        self.yellow_vertical = [1, 1, 1, 1]
        self.red_vertical = [-1, -1, -1, -1]
        
        for i in range(len(columns)):
            if any(self.yellow_vertical == columns[i].column[j:j+4] for j in range(3)):
                game.win_status = 1
                yellow_win.display_win_message()
            if any(self.red_vertical == columns[i].column[j:j+4] for j in range(3)): 
                game.win_status = 1
                red_win.display_win_message()

        # 判斷列
        for i in range(4): #only needs to check the first 4 columns
            for j in range(6): #check all 6 rows of each column

                subtotal = columns[i].column[j] + columns[i+1].column[j] + columns[i+2].column[j] + columns[i+3].column[j]
                if subtotal == 4:
                    game.win_status = 1
                    yellow_win.display_win_message()
                if subtotal == -4:
                    game.win_status = 1
                    red_win.display_win_message()

        
        for i in range(4): #check the first 4 columns
            # 判斷右上到左下
            for j in range(3):
                subtotal = columns[i].column[j] + columns[i+1].column[j+1] + columns[i+2].column[j+2] + columns[i+3].column[j+3]
                if subtotal == 4:
                    game.win_status = 1
                    yellow_win.display_win_message()
                if subtotal == -4:
                    game.win_status = 1
                    red_win.display_win_message()
                    
            # 判斷左上到右下
            for j in range(3, 6):
                subtotal = columns[i].column[j] + columns[i+1].column[j-1] + columns[i+2].column[j-2] + columns[i+3].column[j-3]
                if subtotal == 4:
                    game.win_status = 1
                    yellow_win.display_win_message()       
                if subtotal == -4:
                    game.win_status = 1
                    red_win.display_win_message()

    
        board_full = 1
        for i in range(7):
            for j in range(6):
                board_full *= columns[i].column[j]
        # 棋盤滿了則為平手
        if board_full != 0:
            tie_win.display_win_message()


"""
贏了輸出的訊息
"""
class Win_message(Toplevel):
    def __init__(self, root, team):
        self.root = root
        self.team = team
       
    def display_win_message(self):
        self.win = Toplevel(root)
        self.win.title('Restart?')
        self.win.geometry('250x100+500+250')
        close_btn = Button(self.win, text='Exit', command = self.close_win)
        restart_btn = Button(self.win, text='Restart', command = self.start_win)
        close_btn.place(x = 150, y = 50)
        restart_btn.place(relx = 0.25, y = 50)
        img = PhotoImage(file='picture/celebrate_icon_20.gif')
        lbl = Label(self.win, text = self.team)
        lb2 = Label(self.win, image = img)
        lbl.place(x = 85, y =10)
        lb2.place(x = 60, y = 10)
        self.win.mainloop()
    def start_win(self):
        self.win.quit()
        self.win.destroy()
        for i in range(0,42):
            game.labels[i].grid_forget()
        game.__init__(root)
        yellow_win.__init__(root, "Winner is Yellow!")
        red_win.__init__(root, "Winner is Red!")
        for i in range(7):
            columns[i].__init__()
    def close_win(self):
        root.destroy()
"""
Manages individual columns 0-6
"""
class Memory:
    def __init__(self):
        #sets default state of empty
        self.column = [0 for i in range(6)] #Six pieces, from bottom to top

    def drop_piece(self, c_ord):

        self.c_ord = c_ord
        
        for i in range(len(self.column)):
            if self.column[i] == 0: #check if slot is empty
                if game.count % 2 == 0: #either make slot blue (1) or red (-1)              
                    self.column[i] = 1
                else:
                    self.column[i] = -1

                self.r_ord = i
                self.piece_state = self.column[i]
                #print("Column state:", self.column) #debug
            
                game.count += 1
                #print("Turn number:", game.count)

                game.redraw(self.c_ord, self.r_ord, self.piece_state) #draws colored piece at given coordinates
                game.judge()
                
                break
            elif self.column[5] != 0:
                print("column full")
                break

        
"""
Main routine
"""
if __name__ == "__main__":
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    root.geometry("728x650+250+0")
    root.title("Let's Play Connect Four")
    game = ConnectFour(root)
    yellow_win = Win_message(root, 'Winner is Yellow!')
    red_win = Win_message(root, 'Winner is Red!')
    tie_win = Win_message(root, 'It is a tie!')
    columns = []
    for i in range(7):
        columns.append(Memory())
    root.mainloop()
