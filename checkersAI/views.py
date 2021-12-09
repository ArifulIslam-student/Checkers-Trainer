from django.shortcuts import render
#from .forms import FormUserstable
from .models import Userstable
from django.contrib import messages
from copy import deepcopy 
from django.http import JsonResponse


#AI Code Functions
RED = "red"
WHITE = "wht"
ROWS, COLS = 8, 8
WIDTH = 800
SQUARE_SIZE = WIDTH//COLS
red_left = white_left = 12
red_kings = white_kings = 0

class Board:
    def __init__(self):
        self.board = []
        self.red_left = self.white_left = 12
        self.red_kings = self.white_kings = 0
        self.create_board()
    
    def draw_squares(self, win):
        #win.fill(BLACK)
        for row in range(ROWS):
            for col in range(row % 2, COLS, 2):
                #pygame.draw.rect(win, RED, (row*SQUARE_SIZE, col *SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
                print("I work broski")

    def evaluate(self):
        return self.white_left - self.red_left + (self.white_kings * 0.5 - self.red_kings * 0.5)

    def get_all_pieces(self, color):
        pieces = []
        for row in self.board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

    def move(self, piece, row, col):
        self.board[piece.row][piece.col], self.board[row][col] = self.board[row][col], self.board[piece.row][piece.col]
        piece.move(row, col)

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                self.white_kings += 1
            else:
                self.red_kings += 1 

    def get_piece(self, row, col):
        return self.board[row][col]

    def create_board(self):
        for row in range(ROWS):
            self.board.append([])
            for col in range(COLS):
                if col % 2 == ((row +  1) % 2):
                    if row < 3:
                        self.board[row].append(Piece(row, col, WHITE))
                    elif row > 4:
                        self.board[row].append(Piece(row, col, RED))
                    else:
                        self.board[row].append(0)
                else:
                    self.board[row].append(0)
        
    def draw(self, win):
        self.draw_squares(win)
        for row in range(ROWS):
            for col in range(COLS):
                piece = self.board[row][col]
                if piece != 0:
                    piece.draw(win)

    def remove(self, pieces):
        for piece in pieces:
            self.board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    self.red_left -= 1
                else:
                    self.white_left -= 1
    
    def winner(self):
        if self.red_left <= 0:
            return WHITE
        elif self.white_left <= 0:
            return RED
        
        return None 
    
    def get_valid_moves(self, piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(self._traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(self._traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(self._traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(self._traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

    def _traverse_left(self, start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = self.board[r][left]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r, left)] = last + skipped
                else:
                    moves[(r, left)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

    def _traverse_right(self, start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = self.board[r][right]
            if current == 0:
                if skipped and not last:
                    break
                elif skipped:
                    moves[(r,right)] = last + skipped
                else:
                    moves[(r, right)] = last
                
                if last:
                    if step == -1:
                        row = max(r-3, 0)
                    else:
                        row = min(r+3, ROWS)
                    moves.update(self._traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(self._traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

class Piece:
    PADDING = 15
    OUTLINE = 2

    def __init__(self, row, col, color):
        self.row = row
        self.col = col
        self.color = color
        self.king = False
        self.x = 0
        self.y = 0
        self.calc_pos()

    def calc_pos(self):
        self.x = SQUARE_SIZE * self.col + SQUARE_SIZE // 2
        self.y = SQUARE_SIZE * self.row + SQUARE_SIZE // 2

    def make_king(self):
        self.king = True

    def move(self, row, col):
        self.row = row
        self.col = col
        self.calc_pos()

    def __repr__(self):
        return str(self.color)

class Game:
    def __init__(self):
        self.board = Board()
    def get_board(self):
        return self.board

def getJavascriptVariable(request):
    board = request.GET.get('board', None)
    game = Game()
    difficulty = int(request.GET.get('difficulty', None))
    difficulty = difficulty + 1
    new_board =  [
    [' X ', 'wht', ' X ', 'wht', ' X ', 'wht', ' X ', 'wht'],
    ['wht', ' X ', 'wht', ' X ', 'wht', ' X ', 'wht', ' X '],
    [' X ', 'wht', ' X ', 'red', ' X ', 'wht', ' X ', 'wht'],
    [' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X '],
    [' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X ', ' X '],
    ['red', ' X ', 'red', ' X ', 'red', ' X ', 'red', ' X '],
    [' X ', 'red', ' X ', 'white', ' X ', 'red', ' X ', 'red'],
    ['red', ' X ', 'red', ' X ', 'red', ' X ', 'red', ' X ']
  ]

    value, new_board = minimax(game.get_board(), difficulty, WHITE)
    response = {
        'board': new_board
    }
    return JsonResponse(response)

def minimax(position, depth, max_player): #remove all "game"
    if depth == 0:
        return position
    
    if max_player:
        maxEval = float('-inf')
        best_move = None
        for move in get_all_moves(position, WHITE):
            evaluation = minimax(move, depth-1, False)[0]
            maxEval = max(maxEval, evaluation)
            if maxEval == evaluation:
                best_move = move
        
        return maxEval, best_move
    else:
        minEval = float('inf')
        best_move = None
        for move in get_all_moves(position, RED):
            evaluation = minimax(move, depth-1, True)[0]
            minEval = min(minEval, evaluation)
            if minEval == evaluation:
                best_move = move
        
        return minEval, best_move

def simulate_move(piece, move, board, skip): #not sure if needed
    board.move(piece, move[0], move[1])
    if skip:
        board.remove(skip)

    return board

def get_all_moves(board, color):
    moves = []
    print(board.get_all_pieces(color))
    for piece in board.get_all_pieces(color):
        valid_moves = board.get_valid_moves(piece)
        for move, skip in valid_moves.items():
            #draw_moves(board, piece)
            temp_board = deepcopy(board) 
            temp_piece = temp_board.get_piece(piece.row, piece.col)
            new_board = simulate_move(temp_piece, move, temp_board, skip)
            moves.append(new_board)
    
    return moves


#def draw_moves(game, board, piece):
    #valid_moves = get_valid_moves(piece)
    #board.draw(game.win)
    #pygame.draw.circle(game.win, (0,255,0), (piece.x, piece.y), 50, 5) #remove for django
    #game.draw_valid_moves(valid_moves.keys()) #draws moves in real time 
    #pygame.display.update() #remove for django
    #pygame.time.delay(100)


#Ai Code Ending


def Login(request):
    users = Userstable.objects.all()
    if request.method == "POST":
        getuserids = request.POST.get('userid')
        getuserpasswords = request.POST.get('userpassword')
        for login in users:
            if getuserids == login.userid and getuserpasswords == login.userpassword:
                return render(request, 'homepage.html', {'user': users, 'getuserid': getuserids, 'getuserpassword': getuserpasswords}) #homepage path 

        return render(request, 'signin.html', {'user': users, 'getuserid': getuserids, 'getuserpassword': getuserpasswords})

    else:
        return render(request, 'signin.html', {'user': users})


def Home(request): #doesn't work rn
    users = Userstable.objects.all()
    
    return render(request, 'homepage.html', {'user': users})


def InsertUser(request):
    if request.method == "POST": #ties to signin.html's submit button 
        if request.POST.get('userid') and request.POST.get('userpassword') and request.POST.get('aidifficulty'):
            saverecord = Userstable()
            saverecord.userid = request.POST.get('userid')
            saverecord.userpassword = request.POST.get('userpassword')
            saverecord.aidifficulty = request.POST.get('aidifficulty')
            saverecord.save()
            messages.success(request, 'Record saved')
            return render(request, 'signup.html')
    else:
        messages.success(request, 'Record saved')
        return render(request, 'signup.html')
