import numpy as np

class chessboard(object):
    def __init__(self):
        # 初始化棋盤
        self.board = np.zeros((6,7), dtype=np.int)
    
    def reset(self):
        # 重置棋盤
        self.board = np.zeros((6,7), dtype=np.int)
        
        
    def checkBoradIsFull(self)->bool:
        # 判斷棋盤是否已滿
        return sum(sum(self.board==0)) == 0
     
    def checkRowIsFull(self, column:int)->int:
        """   
        判斷棋盤該列是否已滿，已滿返回-1，未滿返回棋子所落位置的行標
        Args: 
            column: 由界面傳回的玩家選擇落子的入口列下標
        Return:
            index: 返回棋子所落位置的行標，若該列已無位置則返回-1
        """
        
        index = -1
        row = self.board.shape[0]-1
        for i in range(row, 0, -1):
            if self.board[i, column] == 0:
                index = i
                break
        
        return index
            
    
    def place_piece(self, column: int, player: int)->int:
        """   
        放置棋子
        Args: 
            column: 由界面傳回的玩家選擇落子的入口列下標
            player: 由界面傳回的玩家. 1: 玩家1 2: 玩家2
        Return:
            index: 返回棋子所落位置的行標，若該列已無位置則返回-1
        """
        
        index = self.checkRowIsFull(column)
        
        # 該列已沒有位置放置棋子
        if index == -1:
            return -1
        else:
            self.board[index, column] = player
        
        # 返回該棋子所在行下標
        return index
    
    def showBoard(self):
        # 打印棋盤
        print(self.board)
        print("\n")

    def judge(self, row:int ,column:int,player: int) -> bool:
        # 判斷輸贏
        if self.judgeRow(row, column, player) == True:
            return True
        if self.judgeColumn(row, column, player) == True:
            return True
        if self.judgeUpperLeftRight(row, column, player) == True:
            return True
        if self.judgeUpperRightLeft(row, column, player) == True:
            return True
        return False

    def judgeRow(self, row: int, column: int, player: int) -> bool:
        #判断行
        count = 0#連子個數
        flag1 = flag2 = 0#左右判斷
        for i in range(1,4):
            if column-i >= 0 and self.board[row][column-i] == player and flag1 == 0:#向左判斷
                count += 1
            else:
                flag1 = 1
            if column+i < len(self.board[0]) and self.board[row][column+i] == player and flag2 == 0:#向右判斷
                count += 1
            else:
                flag2 = 1;
        if count >= 3:
            return True
        return False

    def judgeColumn(self, row: int, column:int, player: int) -> bool:
        #判斷列
        count = 0
        flag1 = flag2 = 0#上下判斷
        for i in range(1,4):
            if row - i >= 0 and self.board[row-i][column] == player and flag1 == 0:#向上判斷
                count += 1
            else:
                flag1 = 1
            if row + i < len(self.board) and self.board[row + i][column] == player and flag2 == 0:#向下判斷
                count += 1
            else:
                flag2 = 1;
        if count >= 3:
            return True
        return False

    def judgeUpperLeftRight(self, row: int, column: int, player: int) -> bool:
        #判斷左上到右下
        count = 0
        flag1 = flag2 = 0  # 上下判斷
        for i in range(1, 4):
            if row - i >= 0 and column - i >= 0 and self.board[row - i][column - i] == player and flag1 == 0:  # 左上判斷
                count += 1
            else:
                flag1 = 1
            if row + i < len(self.board) and column + i < len(self.board[0]) and self.board[row + i][column + i] == player and flag2 == 0:  # 右下判斷
                count += 1
            else:
                flag2 = 1;
        if count >= 3:
            return True
        return False

    def judgeUpperRightLeft(self, row: int, column: int, player: int) -> bool:
        #判斷右上到左下
        count = 0
        flag1 = flag2 = 0  # 上下判断
        for i in range(1, 4):
            if row - i >= 0 and column + i < len(self.board[0]) and self.board[row - i][column + i] == player and flag1 == 0:  # 左上判斷
                count += 1
            else:
                flag1 = 1
            if row + i < len(self.board) and column - i >= 0 and self.board[row + i][column - i] == player and flag2 == 0:  # 右下判斷
                count += 1
            else:
                flag2 = 1;
        if count >= 3:
            return True
        return False



if __name__ == '__main__':
    board = chessboard()

    game = 1
    player = 0
    while game == 1:
        if board.checkBoradIsFull():
            print("\n\n該棋盤已經落滿棋子，游戲結束")
            break
        print("player {} is placing chess...".format(player+1))
        
        # 玩家落子
        while True:
            column = int(input())
            row = board.place_piece(column, player+1)#棋子坐标
            if row == -1:
                print("該列已沒有位置放置棋子！！！")
            else:
                break
        print("player {} have placed chess.\n".format(player+1))
        
        # 打印棋盤
        board.showBoard()

        # 判斷有無玩家勝利
        if (board.judge(row, column, player+1)) == True:#勝利
            print("Congratulations, player {} wins!\n".format(player+1))
            print("Start over?")
            print("1.Start over")#重新開始
            print("2.Turn off")#結束遊戲
            game = int(input())
            board.reset()
        player = 1-player#更換玩家
        
