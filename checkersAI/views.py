from django.shortcuts import render
#from .forms import FormUserstable
from .models import Userstable
from django.contrib import messages
from copy import deepcopy 

#AI Code Functions
RED = "red"
WHITE = "wht"
ROWS, COLS = 8, 8
red_left = white_left = 12
red_kings = white_kings = 0
board = []




def minimax(position, depth, max_player): #remove all "game"
    if depth == 0 or position.winner() != None:
        return position.evaluate(), position
    
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

def move(piece, row, col):
        board[piece.row][piece.col], board[row][col] = board[row][col], board[piece.row][piece.col]
        piece.move(row, col)
        
        global white_kings, red_kings

        if row == ROWS - 1 or row == 0:
            piece.make_king()
            if piece.color == WHITE:
                white_kings += 1
            else:
                red_kings += 1 

def remove(pieces):

        global red_left, white_left

        for piece in pieces:
            board[piece.row][piece.col] = 0
            if piece != 0:
                if piece.color == RED:
                    red_left -= 1
                else:
                    white_left -= 1

def simulate_move(piece, move, board, skip): #not sure if needed
    move(piece, move[0], move[1])
    if skip:
        remove(skip)

    return board

def get_all_pieces(board, color):
        pieces = []
        for row in board:
            for piece in row:
                if piece != 0 and piece.color == color:
                    pieces.append(piece)
        return pieces

def get_valid_moves(piece):
        moves = {}
        left = piece.col - 1
        right = piece.col + 1
        row = piece.row

        if piece.color == RED or piece.king:
            moves.update(_traverse_left(row -1, max(row-3, -1), -1, piece.color, left))
            moves.update(_traverse_right(row -1, max(row-3, -1), -1, piece.color, right))
        if piece.color == WHITE or piece.king:
            moves.update(_traverse_left(row +1, min(row+3, ROWS), 1, piece.color, left))
            moves.update(_traverse_right(row +1, min(row+3, ROWS), 1, piece.color, right))
    
        return moves

def _traverse_left( start, stop, step, color, left, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if left < 0:
                break
            
            current = board[r][left]
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
                    moves.update(_traverse_left(r+step, row, step, color, left-1,skipped=last))
                    moves.update(_traverse_right(r+step, row, step, color, left+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            left -= 1
        
        return moves

def _traverse_right( start, stop, step, color, right, skipped=[]):
        moves = {}
        last = []
        for r in range(start, stop, step):
            if right >= COLS:
                break
            
            current = board[r][right]
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
                    moves.update(_traverse_left(r+step, row, step, color, right-1,skipped=last))
                    moves.update(_traverse_right(r+step, row, step, color, right+1,skipped=last))
                break
            elif current.color == color:
                break
            else:
                last = [current]

            right += 1
        
        return moves

def get_all_moves(board, color):
    moves = []

    for piece in get_all_pieces(board,color):
        valid_moves = get_valid_moves(piece)
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
