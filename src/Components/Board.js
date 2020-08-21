import React from 'react'
import Cell from './Cell'
import Axios from 'axios'

export default class Board extends React.Component {

    constructor(props){
        super(props)
        this.play = this.play.bind(this)
    }

    componentDidUpdate(){
        if(this.props.turn === this.props.aiPlayer && this.props.gameState === 'RUNNING'){
            this.fetchAIMove()
        }
      }
    
    play(column){
        const board = this.props.board
        let i = board.length - 1;
        while(i >= 0){
          if(board[i][column] === 0) break
          i --
        }
        if(i === -1) return
        board[i][column] = this.props.turn
        if(this.isBoardTerminal(board)){
            const winningCells = this.getWinningCells(board)
            if(winningCells.length === 0){
                this.props.updateState(board, 'STOPPED', [])
            } else{
                this.props.updateState(board, 'STOPPED', winningCells)
            }
        }else {
            this.props.updateState(board, 'RUNNING', [])
        }
    }

    getWinningCells(board){
        /*
        Returns array of cells with the winning move
        If there's a tie or the game hasn't finished, returns empty array
        */
        for(let i = 0; i < 6; i++){
            for(let j = 0; j < 4; j++){
                if(Math.abs(board[i][j] + board[i][j + 1] + board[i][j + 2] + board[i][j + 3]) === 4){
                    return [[i, j], [i, j + 1], [i, j + 2], [i, j + 3]]
                }
            }
        }

        for(let i = 0; i < 3; i++){
            for(let j = 0; j < 7; j++){
                if(Math.abs(board[i][j] + board[i + 1][j] + board[i + 2][j] + board[i + 3][j]) === 4){
                    return [[i, j], [i + 1, j], [i + 2, j], [i + 3, j]]
                }
            }
        }

        for(let i = 0; i < 3; i++){
            for(let j = 0; j < 4; j++){
                if(Math.abs(board[i][j] + board[i + 1][j + 1] + board[i + 2][j + 2] + board[i + 3][j + 3]) === 4){
                    return [[i, j], [i + 1, j + 1], [i + 2, j + 2], [i + 3, j + 3]]
                }
            }
        }

        for(let i = 0; i < 3; i++){
            for(let j = 3; j < 7; j++){
                if(Math.abs(board[i][j] + board[i + 1][j - 1] + board[i + 2][j - 2] + board[i + 3][j - 3]) === 4){
                    return [[i, j], [i + 1, j - 1], [i + 2, j - 2], [i + 3, j - 3]]
                }
            }
        }

        return []
    }

    isBoardTerminal(board){
        if(this.getWinningCells(board).length > 0) return true
        for(let i = 0; i < board.length; i++){
            for(let j = 0; j < board[i].length; j++){
                if(board[i][j] === 0) return false
            }
        }
        return true
    }

    fetchAIMove(){
        let board = ''
        for(let i = 0; i < this.props.board.length; i++){
          board += this.props.board[i].join(',') + ','
        }
        const host = 'https://connect4-carlos.herokuapp.com/'
        const url = `${host}?board=${board}&algorithm=${this.props.algorithm}&difficulty=${this.props.difficulty}`
        Axios.get(url)
        .then(response => {
          return response.data
        })
        .then(data => {
          this.play(data.action)
        }).catch(err => {
            console.log(err)
        })
      }
    
    renderBoard(){
        const board = Array(6)
        for(let i = 0; i < this.props.board.length; i++){
            board[i] = Array(7)
            for(let j = 0; j < this.props.board[i].length; j++){
                board[i][j] = (
                    <Cell allowedEvents={this.props.turn !== this.props.aiPlayer} isWinningCell={this.props.winningCells.map(arr => JSON.stringify(arr)).includes(JSON.stringify([i, j]))} gameState={this.props.gameState} value={this.props.board[i][j]} row={i} column={j} handleClick={this.play}/>
                )
            }
        }
        return board
    }
    
    render(){
        return (
            <div className="Board">
                {this.renderBoard()}
            </div>
        )
    }
}