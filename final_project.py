# Connect Four
from tkinter import *
import time
import sys


# 製作遊戲大小
class LoadingBar:
    def __init__(self, num_images):
        self.num_images = num_images
        self.length = num_images * 21 #frame count of each GIF image
        self.bar = ["-"] * self.length

    def increment_bar(self):
        for i in range(len(self.bar)):
            if self.bar[i] == "-":
                self.bar[i] = "|"
                print ('[%s]' % ''.join(map(str, self.bar)), "Loading")
                break


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
        elif self.piece_state == -1:
            self.labels[piece_index].configure(image = self.red_image)
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
                yellow_win.display_win_message()
            if any(self.red_vertical == columns[i].column[j:j+4] for j in range(3)): 
                red_win.display_win_message()

        # 判斷列
        for i in range(4): #only needs to check the first 4 columns
            for j in range(6): #check all 6 rows of each column

                subtotal = columns[i].column[j] + columns[i+1].column[j] + columns[i+2].column[j] + columns[i+3].column[j]
                if subtotal == 4: 
                    yellow_win.display_win_message()
                if subtotal == -4:
                    red_win.display_win_message()

        
        for i in range(4): #check the first 4 columns
            # 判斷右上到左下
            for j in range(3):
                subtotal = columns[i].column[j] + columns[i+1].column[j+1] + columns[i+2].column[j+2] + columns[i+3].column[j+3]
                if subtotal == 4: 
                    yellow_win.display_win_message()
                if subtotal == -4:
                    red_win.display_win_message()
                    
            # 判斷左上到右下
            for j in range(3, 6):
                subtotal = columns[i].column[j] + columns[i+1].column[j-1] + columns[i+2].column[j-2] + columns[i+3].column[j-3]
                if subtotal == 4:
                    yellow_win.display_win_message()       
                if subtotal == -4:
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
class Win_message:
    def __init__(self, root, team):
        
        self.root = root
        self.team = team
        self.frame_status = 0
        self.total_frame_num = 21 #length of GIF anim in frames
        self.frame_delay = 30 #in ms
        #grid contraction variables
        self.grid_total_frame_num = 9 #controls duration of contraction
        self.grid_multiplier = 3 #controls speed of contraction
        #button slide variables
        self.current_height = -0.1 #also the starting height
        self.final_height = 0.32 #actual stopping height will be greater and a multiple of increment_height
        self.increment_height = 0.02 #as a proportion of the window space
        
    #load animation frames. This is an individual method because it does not need to be called on 'Play Again', whereas everything else in __init__() needs to be reset.
    def load_frames(self):
        
        self.frames = []    
        #loads each frame to the list self.frames
        for i in range(self.total_frame_num):
            
            self.frames.append(PhotoImage(file = self.team, format = "gif -index " + str(i)))
            loading.increment_bar()

    #create the two buttons just once
    def place_buttons(self):
        
        game.win_status = 1 #game has been won, prevents slots from being clicked
        self.button_again = Button(text = "Play Again",
                                   command = self.again,
                                   height = 4,
                                   width = 20)
        self.button_again.place(relx = 0.25, rely = self.current_height)

        self.button_quit = Button(text = "Quit",
                                  command = self.quit_game,
                                  height = 4,
                                  width = 20)
        self.button_quit.place(relx = 0.55, rely = self.current_height)
        
        self.animate_buttons() #begin animation of buttons

    #animate the two buttons
    def animate_buttons(self):
        #drop the play again / quit buttons down
        if self.current_height < self.final_height:
            self.button_again.place(rely = self.current_height)
            self.button_quit.place(rely = self.current_height)
            self.current_height += self.increment_height
            
            self.root.after(self.frame_delay, self.animate_buttons)

    #animate the main win banner   
    def win_animation(self):
        
        self.winlabel = Label(background = "white", image = self.frames[self.frame_status])#creates label from first frame
        self.winlabel.place(relx = 0.5, rely = 1, anchor = S)
        
        for i in range(42):
            game.labels[i].lift() #pulls banner below the pieces
        
        if self.frame_status < self.total_frame_num:
            self.frame_status += 1 #cycles to next frame
            
        self.winlabel.configure(image = self.frames[self.frame_status - 1]) #refreshes frame
        #print("Displaying frame", self.frame_status)

        if self.frame_status < self.grid_total_frame_num:            
            for i in range(42):
                game.labels[i].configure(height = 100 - self.frame_status * self.grid_multiplier) #contracts grid at the same time as animated banner
        
        if self.frame_status < self.total_frame_num:
            self.root.after(self.frame_delay, self.win_animation) #keeps updating the image every 20ms
        else:
            self.place_buttons() #triggers button fall AFTER animation is complete to avoid a bug

    #initiates animations. Allows them to be split into their own methods.
    def display_win_message(self):
        self.win_animation()
        
    def again(self):
        #restart board and memory
        for i in range(0,42):
            game.labels[i].grid_forget()
        game.__init__(root)
        yellow_win.__init__(root, "yellow")
        red_win.__init__(root, "red")
        for i in range(7):
            columns[i].__init__()
                
    def quit_game(self): #Contains both methods because one does not work in the IDE?
        root.destroy()
        sys.exit()         


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
    root.geometry("728x624")
    root.title("Let's Play Connect Four")
    loading = LoadingBar(3)
    game = ConnectFour(root)
    yellow_win = Win_message(root, 'picture/bluewin.gif')
    red_win = Win_message(root, 'picture/redwin.gif')
    tie_win = Win_message(root, 'picture/tiewin.gif')
    yellow_win.load_frames()
    red_win.load_frames()
    tie_win.load_frames()
    columns = []
    
    for i in range(7):
        columns.append(Memory())
    root.mainloop()
 