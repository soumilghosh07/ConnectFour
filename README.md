# ConnectFour
# Four Connect Game with Game Tree Player

This project implements the Four Connect game, allowing users to play against an AI opponent powered by the Game Tree Player, which utilizes the MiniMax algorithm with Alpha-Beta pruning. The game provides an interactive and challenging experience for players to test their strategic thinking skills.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Installation](#installation)
- [How to Use](#how-to-use)
- [File Structure](#file-structure)
- [Test Cases](#test-cases)

## Introduction

The game of Four Connect, also known as Connect Four, is a classic two-player connection game in which the players take turns dropping colored discs into a grid. The objective of the game is to be the first to form a horizontal, vertical, or diagonal line of four discs of one's own color.

The Game Tree Player is an AI opponent that evaluates possible moves using the MiniMax algorithm with Alpha-Beta pruning, allowing it to make intelligent decisions to maximize its chances of winning.

## Features

- **Interactive Gameplay**: Players can enjoy a user-friendly interface that allows them to interact with the game easily.
- **AI Opponent**: The Game Tree Player provides a challenging opponent that utilizes advanced algorithms to make strategic moves.
- **MiniMax Algorithm**: The AI opponent employs the MiniMax algorithm with Alpha-Beta pruning to search through the game tree and select the best possible move.
- **Graphical Display**: The game board is displayed graphically, providing a visual representation of the current game state.

## Installation

To run the Four Connect game with the Game Tree Player, follow these steps:

1. Ensure you have Python 3 installed on your system.
2. Download or clone the repository to your local machine.
3. Navigate to the project directory in your terminal.
4. Run the `FourConnect.py` file using Python to start the game.

## How to Use

1. Launch the game by running the `FourConnect.py` file.
2. Follow the on-screen instructions to select the game mode (human vs. AI) and begin playing.
3. Drop your colored discs into the grid and try to connect four of them in a row horizontally, vertically, or diagonally before your opponent does.
4. If playing against the AI, observe its moves and plan your strategy accordingly to outsmart it and win the game.

## File Structure

The project directory contains the following files:

- `FourConnect.py`: Implementation of the Four Connect game.
- `testcase.csv`: Test cases for evaluating the Game Tree Player's performance.

## Test Cases

The `testcase.csv` file contains predefined game states for evaluating the performance of the Game Tree Player. These test cases simulate various scenarios to assess the AI opponent's ability to make optimal moves and win the game.


