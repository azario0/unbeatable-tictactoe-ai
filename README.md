# 🎯 Unbeatable Tic-Tac-Toe AI

[![Python](https://img.shields.io/badge/Python-3.7+-blue.svg)](https://python.org)
[![Flask](https://img.shields.io/badge/Flask-2.0+-green.svg)](https://flask.palletsprojects.com/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> A sophisticated Tic-Tac-Toe game featuring an unbeatable AI powered by the Minimax algorithm with Alpha-Beta pruning, complete with a sleek web interface.

## ✨ Features

### 🤖 **Intelligent AI Engine**
- **Unbeatable AI** using Minimax algorithm with Alpha-Beta pruning
- **Lightning-fast decisions** with memoization caching
- **Adaptive gameplay** supporting dynamic player symbols
- **Performance analytics** with built-in simulation modes

### 🎮 **Modern Web Interface**
- **Intuitive gameplay** with responsive click-to-play mechanics  
- **Symbol selection** - choose to play as X (first) or O (second)
- **Real-time updates** with seamless AI integration
- **Visual feedback** and game status indicators
- **Clean, modern design** optimized for all devices

### 🏗️ **Robust Architecture**
- **Microservices design** with separate API and client applications
- **RESTful API** for easy integration and extensibility
- **Cross-origin support** with Flask-CORS
- **Comprehensive error handling** and input validation

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/azario0/unbeatable-tictactoe-ai.git
   cd unbeatable-tictactoe-ai
   ```

2. **Set up virtual environment**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Application

The application consists of two components that need to run simultaneously:

#### 1. Start the AI API Server
```bash
cd api_server
python app.py api
```
🌐 **API Server**: http://127.0.0.1:5000

#### 2. Start the Web Client
```bash
# In a new terminal
cd client_app  
python client_app.py
```
🎮 **Game Interface**: http://127.0.0.1:5001

## 🎯 How to Play

1. **Access the game** at http://127.0.0.1:5001
2. **Choose your symbol**: 
   - Select **X** to make the first move
   - Select **O** to let the AI go first  
3. **Make your moves** by clicking on empty cells
4. **Watch the AI respond** with optimal counter-moves
5. **Try to beat the unbeatable!** (Spoiler: you can't, but you can tie!)

## 📁 Project Structure

```
unbeatable-tictactoe-ai/
├── 📁 api_server/
│   └── 🐍 app.py              # AI engine & Flask API
├── 📁 client_app/
│   ├── 🐍 client_app.py       # Web application server
│   ├── 📁 static/
│   │   └── 🎨 style.css       # Game styling
│   └── 📁 templates/
│       ├── 🏠 start.html      # Symbol selection page
│       └── 🎮 game.html       # Game board interface
├── 📋 requirements.txt        # Python dependencies
├── 📖 README.md              # Project documentation
└── ⚖️  LICENSE               # MIT License
```

## 🔧 API Reference

### `POST /predict_move`

Get the AI's optimal next move.

**Request Body:**
```json
{
  "board": [" ", "X", " ", "O", "X", " ", " ", " ", "O"],
  "ai_symbol": "O",
  "opponent_symbol": "X"
}
```

**Response:**
```json
{
  "board": ["O", "X", " ", "O", "X", " ", " ", " ", "O"],
  "ai_move_index": 0,
  "status": "success", 
  "message": "AI (O) moved to position 0.",
  "game_over": false,
  "winner": null
}
```

## 🎮 Additional Game Modes

The AI engine supports additional interaction modes:

### Interactive Terminal Play
```bash
cd api_server
python app.py interactive
```

### AI Performance Simulation  
```bash
cd api_server
python app.py simulate
```
*Runs AI vs random player simulations with performance analytics*

## 🛠️ Tech Stack

- **Backend**: Python, Flask, Flask-CORS
- **Frontend**: HTML5, CSS3, JavaScript
- **AI Algorithm**: Minimax with Alpha-Beta pruning
- **HTTP Client**: Requests library
- **Analytics**: Matplotlib, NumPy (for simulations)

## 🤝 Contributing

Contributions are welcome! Here are some ways you can help:

- 🐛 Report bugs and issues
- 💡 Suggest new features or improvements  
- 🔧 Submit pull requests
- 📖 Improve documentation
- ⭐ Star the repository if you find it useful!

### Development Setup

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and test thoroughly
4. Commit your changes: `git commit -m 'Add some feature'`
5. Push to the branch: `git push origin feature-name`
6. Submit a pull request

## 🚀 Future Roadmap

- [ ] **Enhanced UI/UX** with animations and sound effects
- [ ] **Multiplayer support** for human vs human games
- [ ] **Difficulty levels** with adjustable AI intelligence
- [ ] **Mobile app** versions for iOS and Android
- [ ] **WebSocket integration** for real-time gameplay
- [ ] **Tournament mode** with leaderboards
- [ ] **Cloud deployment** on major platforms

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**azario0**
- GitHub: [@azario0](https://github.com/azario0)

## 🙏 Acknowledgments

- Thanks to the creators of the Minimax algorithm
- Inspired by classic game theory and AI research
- Built with modern web technologies and best practices

---

<div align="center">

**⭐ Star this repository if you found it helpful!**

[Report Bug](https://github.com/azario0/unbeatable-tictactoe-ai/issues) · [Request Feature](https://github.com/azario0/unbeatable-tictactoe-ai/issues) · [Contribute](https://github.com/azario0/unbeatable-tictactoe-ai/pulls)

</div>