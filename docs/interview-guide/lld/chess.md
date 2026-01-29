---
sidebar_position: 6
title: "Design Chess Game"
description: >-
  Complete LLD for chess game. Piece hierarchy, move validation,
  game state management, and check/checkmate detection.
keywords:
  - chess design
  - LLD chess
  - game design
  - object oriented chess
difficulty: Advanced
estimated_time: 40 minutes
prerequisites:
  - SOLID Principles
companies: [Amazon, Google, Microsoft]
---

# Design a Chess Game

Chess is a classic OOP design problem. It tests inheritance, polymorphism, and state management.

---

## Requirements

- Two-player game
- Standard chess rules
- All piece movements
- Check, checkmate, stalemate detection
- Move validation
- Game history

---

## Class Diagram

```
┌─────────────────┐       ┌─────────────────┐
│      Game       │       │     Board       │
├─────────────────┤       ├─────────────────┤
│ - board         │──────▶│ - squares[8][8] │
│ - players[2]    │       │ - pieces        │
│ - currentTurn   │       ├─────────────────┤
│ - status        │       │ + getPiece()    │
├─────────────────┤       │ + movePiece()   │
│ + move()        │       │ + isCheck()     │
│ + getStatus()   │       └─────────────────┘
└─────────────────┘
         │
         ▼
┌─────────────────┐       ┌─────────────────┐
│     Player      │       │     Piece       │ (Abstract)
├─────────────────┤       ├─────────────────┤
│ - color         │       │ - color         │
│ - name          │       │ - position      │
└─────────────────┘       ├─────────────────┤
                          │ + getValidMoves()│
                          │ + canMove()     │
                          └────────┬────────┘
                                   │
        ┌──────────┬───────────────┼───────────────┬──────────┐
        ▼          ▼               ▼               ▼          ▼
    ┌──────┐  ┌──────┐        ┌──────┐        ┌──────┐  ┌──────┐
    │ King │  │Queen │        │Bishop│        │Knight│  │ Pawn │
    └──────┘  └──────┘        └──────┘        └──────┘  └──────┘
```

---

## Implementation

### Enums and Helpers

```python
from enum import Enum
from abc import ABC, abstractmethod

class Color(Enum):
    WHITE = "white"
    BLACK = "black"

class GameStatus(Enum):
    ACTIVE = "active"
    WHITE_WIN = "white_win"
    BLACK_WIN = "black_win"
    STALEMATE = "stalemate"
    RESIGNED = "resigned"

class Position:
    def __init__(self, row: int, col: int):
        self.row = row
        self.col = col
    
    def is_valid(self):
        return 0 <= self.row < 8 and 0 <= self.col < 8
    
    def __eq__(self, other):
        return self.row == other.row and self.col == other.col
    
    def __hash__(self):
        return hash((self.row, self.col))
```

### Piece Base Class

```python
class Piece(ABC):
    def __init__(self, color: Color, position: Position):
        self.color = color
        self.position = position
        self.has_moved = False
    
    @abstractmethod
    def get_valid_moves(self, board) -> list:
        pass
    
    def can_move(self, board, end: Position) -> bool:
        return end in self.get_valid_moves(board)
    
    def _is_valid_destination(self, board, pos: Position) -> bool:
        if not pos.is_valid():
            return False
        piece = board.get_piece(pos)
        return piece is None or piece.color != self.color
```

### Piece Implementations

```python
class King(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1,-1),(-1,0),(-1,1),(0,-1),(0,1),(1,-1),(1,0),(1,1)]
        
        for dr, dc in directions:
            pos = Position(self.position.row + dr, self.position.col + dc)
            if self._is_valid_destination(board, pos):
                moves.append(pos)
        
        # Castling logic would go here
        return moves

class Queen(Piece):
    def get_valid_moves(self, board):
        moves = []
        # Combine rook and bishop moves
        directions = [(-1,0),(1,0),(0,-1),(0,1),(-1,-1),(-1,1),(1,-1),(1,1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                pos = Position(self.position.row + dr*i, self.position.col + dc*i)
                if not pos.is_valid():
                    break
                piece = board.get_piece(pos)
                if piece is None:
                    moves.append(pos)
                elif piece.color != self.color:
                    moves.append(pos)
                    break
                else:
                    break
        return moves

class Rook(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1,0),(1,0),(0,-1),(0,1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                pos = Position(self.position.row + dr*i, self.position.col + dc*i)
                if not pos.is_valid():
                    break
                piece = board.get_piece(pos)
                if piece is None:
                    moves.append(pos)
                elif piece.color != self.color:
                    moves.append(pos)
                    break
                else:
                    break
        return moves

class Bishop(Piece):
    def get_valid_moves(self, board):
        moves = []
        directions = [(-1,-1),(-1,1),(1,-1),(1,1)]
        
        for dr, dc in directions:
            for i in range(1, 8):
                pos = Position(self.position.row + dr*i, self.position.col + dc*i)
                if not pos.is_valid():
                    break
                piece = board.get_piece(pos)
                if piece is None:
                    moves.append(pos)
                elif piece.color != self.color:
                    moves.append(pos)
                    break
                else:
                    break
        return moves

class Knight(Piece):
    def get_valid_moves(self, board):
        moves = []
        jumps = [(-2,-1),(-2,1),(-1,-2),(-1,2),(1,-2),(1,2),(2,-1),(2,1)]
        
        for dr, dc in jumps:
            pos = Position(self.position.row + dr, self.position.col + dc)
            if self._is_valid_destination(board, pos):
                moves.append(pos)
        return moves

class Pawn(Piece):
    def get_valid_moves(self, board):
        moves = []
        direction = -1 if self.color == Color.WHITE else 1
        
        # Forward move
        front = Position(self.position.row + direction, self.position.col)
        if front.is_valid() and board.get_piece(front) is None:
            moves.append(front)
            
            # Double move from starting position
            if not self.has_moved:
                double = Position(self.position.row + 2*direction, self.position.col)
                if board.get_piece(double) is None:
                    moves.append(double)
        
        # Captures
        for dc in [-1, 1]:
            capture = Position(self.position.row + direction, self.position.col + dc)
            if capture.is_valid():
                piece = board.get_piece(capture)
                if piece and piece.color != self.color:
                    moves.append(capture)
        
        # En passant would go here
        return moves
```

### Board

```python
class Board:
    def __init__(self):
        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self._setup_pieces()
    
    def _setup_pieces(self):
        # Place pawns
        for col in range(8):
            self.squares[1][col] = Pawn(Color.BLACK, Position(1, col))
            self.squares[6][col] = Pawn(Color.WHITE, Position(6, col))
        
        # Place other pieces
        piece_order = [Rook, Knight, Bishop, Queen, King, Bishop, Knight, Rook]
        for col, piece_class in enumerate(piece_order):
            self.squares[0][col] = piece_class(Color.BLACK, Position(0, col))
            self.squares[7][col] = piece_class(Color.WHITE, Position(7, col))
    
    def get_piece(self, pos: Position):
        if pos.is_valid():
            return self.squares[pos.row][pos.col]
        return None
    
    def move_piece(self, start: Position, end: Position):
        piece = self.get_piece(start)
        if piece:
            self.squares[end.row][end.col] = piece
            self.squares[start.row][start.col] = None
            piece.position = end
            piece.has_moved = True
    
    def is_check(self, color: Color) -> bool:
        king_pos = self._find_king(color)
        opponent = Color.BLACK if color == Color.WHITE else Color.WHITE
        
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if piece and piece.color == opponent:
                    if king_pos in piece.get_valid_moves(self):
                        return True
        return False
    
    def _find_king(self, color: Color) -> Position:
        for row in range(8):
            for col in range(8):
                piece = self.squares[row][col]
                if isinstance(piece, King) and piece.color == color:
                    return piece.position
        return None
```

### Game

```python
class Game:
    def __init__(self, player1: str, player2: str):
        self.board = Board()
        self.players = [
            Player(player1, Color.WHITE),
            Player(player2, Color.BLACK)
        ]
        self.current_turn = 0
        self.status = GameStatus.ACTIVE
        self.move_history = []
    
    def move(self, start: Position, end: Position) -> bool:
        if self.status != GameStatus.ACTIVE:
            return False
        
        piece = self.board.get_piece(start)
        current_color = self.players[self.current_turn].color
        
        if not piece or piece.color != current_color:
            return False
        
        if not piece.can_move(self.board, end):
            return False
        
        # Make move
        captured = self.board.get_piece(end)
        self.board.move_piece(start, end)
        
        # Check if move puts own king in check
        if self.board.is_check(current_color):
            # Undo move
            self.board.move_piece(end, start)
            if captured:
                self.board.squares[end.row][end.col] = captured
            return False
        
        self.move_history.append((start, end, captured))
        self._check_game_status()
        self.current_turn = 1 - self.current_turn
        
        return True
    
    def _check_game_status(self):
        opponent_color = self.players[1 - self.current_turn].color
        
        if self._is_checkmate(opponent_color):
            self.status = (GameStatus.WHITE_WIN 
                          if opponent_color == Color.BLACK 
                          else GameStatus.BLACK_WIN)
        elif self._is_stalemate(opponent_color):
            self.status = GameStatus.STALEMATE
    
    def _is_checkmate(self, color: Color) -> bool:
        if not self.board.is_check(color):
            return False
        return not self._has_valid_moves(color)
    
    def _is_stalemate(self, color: Color) -> bool:
        if self.board.is_check(color):
            return False
        return not self._has_valid_moves(color)
    
    def _has_valid_moves(self, color: Color) -> bool:
        for row in range(8):
            for col in range(8):
                piece = self.board.squares[row][col]
                if piece and piece.color == color:
                    if piece.get_valid_moves(self.board):
                        return True
        return False

class Player:
    def __init__(self, name: str, color: Color):
        self.name = name
        self.color = color
```

---

## Key Design Decisions

| Decision | Choice | Why |
|----------|--------|-----|
| Piece hierarchy | Abstract base class | Polymorphic move validation |
| Move validation | Per piece | Each piece has unique rules |
| Board representation | 2D array | Simple access, intuitive |
| Game state | Enum | Clear status tracking |

---

## Extensions

1. **Castling:** Track king/rook moved status
2. **En passant:** Track last move for pawn captures
3. **Pawn promotion:** Detect and handle
4. **Move notation:** Standard algebraic notation
5. **Undo/redo:** Command pattern
