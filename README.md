# 2 Truths 1 Lie Game

A fun, interactive trivia game built using Generative AI and Streamlit that challenges players to distinguish truth from fiction. The game presents three statements where two are true and one is false, pushing players to use their knowledge and intuition to spot the lie.

## Features

The game incorporates several engaging elements to create an entertaining learning experience:

- Each round presents three carefully crafted statements
- Real-time feedback when players make their selection
- Detailed explanations for all statements after each guess
- Concurrent fact generation for smooth gameplay
- Celebratory animations for correct answers

## Technical Implementation

The application uses a sophisticated architecture combining several Python technologies:

- Streamlit for the interactive web interface
- LangChain for structured prompt management
- GPT-4 for generating creative and educational content
- Concurrent futures for managing asynchronous operations

## Setup and Installation

1. Clone the repository and navigate to the project directory:
```bash
git clone <repository-url>
cd TwoTruthsOneLie
```

2. Install the required dependencies:
```bash
pip install -r requirements.txt
```

3. Set up your environment variables:
```bash
export OPENAI_API_KEY='your-api-key'
```

4. Launch the application:
```bash
streamlit run two_truths_one_lie.py
```

## How to Play

1. Read the three statements presented on screen
2. Click on the statement you believe is false
3. The game will reveal whether your choice was correct
4. Read the explanations to learn more about each statement
5. Click "Skip / Next Question" to move to the next round

## Contributing

We welcome contributions to improve the game! Some areas for potential enhancement:

- Additional topic categories
- Difficulty levels
- Score tracking
- Multiplayer functionality
- Custom prompt templates

Feel free to submit pull requests or open issues for any bugs or feature suggestions.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
