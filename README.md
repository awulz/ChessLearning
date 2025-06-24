# Chess Learning Platform

A comprehensive chess learning application built with Python and Pygame, designed to help users learn and practice chess through an interactive graphical interface.

## 🎯 Project Overview

This chess learning platform provides a fully functional chess game with a modern graphical interface, complete move validation, and educational features. The application is designed to be both a learning tool for chess beginners and a practice environment for more experienced players.

## ✨ Features

### Core Gameplay
- **Complete Chess Rules Implementation**: All standard chess rules including special moves
- **Move Validation**: Real-time validation of all chess moves
- **Castling Support**: Both kingside and queenside castling with proper validation
- **Check Detection**: Automatic detection of check and checkmate situations
- **Turn-based Gameplay**: Proper alternating turns between white and black players

### User Interface
- **Modern Graphical Interface**: Clean, intuitive design using Pygame
- **Visual Move Indicators**: Highlighted squares for selected pieces and valid moves
- **Board Coordinates**: Clear rank and file labels for easy position identification
- **Piece Visualization**: High-quality chess piece graphics for both white and black pieces

### Educational Features
- **Move Preview**: Visual indication of possible moves for selected pieces
- **Castling Preview**: Special highlighting for castling moves when king is selected
- **Error Feedback**: Clear messages for invalid moves and rule violations
- **Game State Tracking**: Comprehensive tracking of game state and move history

## 🛠️ Technical Architecture

### Project Structure
```
ChessLearning-6/
├── ChessMain.py          # Main application driver and UI logic
├── ChessEngine.py        # Game state management and core chess logic
├── images/               # Chess piece graphics
│   ├── wP.png, wR.png, wN.png, wB.png, wK.png, wQ.png  # White pieces
│   └── bp.png, bR.png, bN.png, bB.png, bK.png, bQ.png  # Black pieces
└── README.md            # This file
```

### Key Components

#### ChessMain.py
- **Main Game Loop**: Handles user input, game state updates, and rendering
- **Event Handling**: Mouse click detection and piece movement
- **Graphics Rendering**: Board drawing, piece placement, and visual effects
- **Move Validation**: Integration with chess engine for move verification

#### ChessEngine.py
- **Game State Management**: Board representation and game state tracking
- **Move Logic**: Implementation of all chess piece movement rules
- **Special Moves**: Castling, en passant, and pawn promotion logic
- **Check Detection**: Pin and check analysis algorithms

## 🚀 Installation

### Prerequisites
- Python 3.7 or higher
- Pygame library

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd ChessLearning-6
   ```

2. **Install dependencies**
   ```bash
   pip install pygame
   ```

3. **Run the application**
   ```bash
   python ChessMain.py
   ```

## 🎮 How to Play

### Basic Controls
- **Select a piece**: Click on any chess piece to select it
- **Make a move**: Click on a valid destination square to move the selected piece
- **Deselect**: Click on the same square again to deselect a piece
- **Quit**: Close the window to exit the game

### Game Rules
- **Turn Order**: White moves first, then players alternate
- **Valid Moves**: Only legal chess moves are allowed
- **Check**: The game automatically detects when a king is in check
- **Castling**: Available when king and rook haven't moved and no pieces are between them

### Visual Indicators
- **Blue Square**: Currently selected piece
- **Yellow Square**: Valid castling moves (when king is selected)
- **Board Coordinates**: Numbers (1-8) on the left, letters (a-h) on the bottom

## 🔧 Development Status

### ✅ Completed Features
- Complete chess game implementation
- Move validation for all pieces
- Castling mechanics
- Check detection
- Graphical user interface
- Turn-based gameplay

### 🚧 In Development
- **Backend Integration**: Django backend for user management and game history
- **Multiplayer Support**: Online gameplay capabilities
- **Game Analysis**: Move analysis and suggestions
- **Learning Modules**: Tutorial and training features

## 🎯 Future Roadmap

### Phase 1: Backend Development (Planned)
- **Django Backend**: User authentication and profile management
- **Database Integration**: Game history and statistics storage
- **API Development**: RESTful API for frontend-backend communication

### Phase 2: Enhanced Features (Planned)
- **User Accounts**: Registration, login, and profile management
- **Game History**: Save and replay previous games
- **Statistics Tracking**: Win/loss ratios, move analysis
- **Difficulty Levels**: AI opponent with adjustable difficulty

### Phase 3: Advanced Features (Planned)
- **Online Multiplayer**: Real-time online chess games
- **Tournament System**: Organize and participate in tournaments
- **Learning Paths**: Structured learning modules for different skill levels
- **Mobile Support**: Cross-platform compatibility

## 🤝 Contributing

We welcome contributions to improve the chess learning platform! Here's how you can help:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Commit your changes**: `git commit -m 'Add amazing feature'`
4. **Push to the branch**: `git push origin feature/amazing-feature`
5. **Open a Pull Request**

### Development Guidelines
- Follow Python PEP 8 style guidelines
- Add comments for complex logic
- Test your changes thoroughly
- Update documentation as needed

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Chess Piece Graphics**: High-quality chess piece images for the game interface
- **Pygame Community**: For the excellent game development framework
- **Chess Community**: For inspiration and feedback on chess rule implementations

## 📞 Support

If you encounter any issues or have questions about the project:

1. **Check the Issues**: Look for existing issues in the GitHub repository
2. **Create a New Issue**: Report bugs or request new features
3. **Contact the Team**: Reach out to the development team

---

**Note**: This project is currently in active development. The Django backend integration is planned for future releases and will significantly enhance the platform's capabilities with user management, game history, and online features. 