import React from 'react';
import './App.css';
import Board from './Components/Board'
import Control from './Components/Control'

export default class App extends React.Component {

  constructor(props){
    super(props)
    this.state = {
      board: this.initBoard(),
      turn: 1,
      gameState: 'RUNNING',
      winningCells: [],
      algorithm: 'mcts',
      aiPlayer: -1,
      difficulty: 1,
      isAiThinking: false
    }

    this.resetState = this.resetState.bind(this)
  }

  initBoard(){
    const board = []
    for(let i = 0; i < 6; i++){
      board.push([])
      for(let j = 0; j < 7; j++){
        board[i].push(0)
      }
    }
    return board
  }

  resetState(){
    this.setState(() => ({
      board: this.initBoard(),
      turn: 1,
      gameState: 'RUNNING',
      winningCells: []
    }))
  }

  getMessage(){
    if(this.state.gameState === 'STOPPED'){
      if(this.state.winningCells.length === 0) return 'Tie'
      if(this.state.board[this.state.winningCells[0][0]][this.state.winningCells[0][1]] === this.state.aiPlayer) return 'I win'
      return 'You win'
    }
    if(this.state.turn === this.state.aiPlayer) return 'I am thinking...'
    return 'Your turn, human'
  }

  render(){
    return (
      <div className='container'>
        <Board algorithm={this.state.algorithm} difficulty={this.state.difficulty} aiPlayer={this.state.aiPlayer} winningCells={this.state.winningCells} gameState={this.state.gameState} turn={this.state.turn} board={this.state.board} updateState={(board, gameState, winningCells) => this.setState(state => ({board: board, turn: state.turn * (-1), gameState: gameState, winningCells: winningCells}))}/>
        <Control message={this.getMessage()} gameState={this.state.gameState} algorithm={this.state.algorithm} difficulty={this.state.difficulty} aiPlayer={this.state.aiPlayer} handleReset={this.resetState} handlePlayer={aiPlayer => this.setState(() => ({aiPlayer: aiPlayer}))} handleAlgorithm={algorithm => this.setState(() => ({algorithm: algorithm}))} handleDifficulty={difficulty => this.setState(() => ({difficulty: difficulty}))}/>
      </div>
    )
  }
}