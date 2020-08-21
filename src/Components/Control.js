import React from 'react'

export default class Control extends React.Component {

    constructor(props){
        super(props)
        this.handlePlayer = this.handlePlayer.bind(this)
        this.handleAlgorithm = this.handleAlgorithm.bind(this)
        this.handleDifficulty = this.handleDifficulty.bind(this)
    }

    handlePlayer(e){
        this.props.handlePlayer(parseInt(e.target.value))
    }

    handleAlgorithm(e){
        this.props.handleAlgorithm(e.target.value)
    }

    handleDifficulty(e){
        this.props.handleDifficulty(parseInt(e.target.value))
    }
    
    render(){
        return(
            <div className='Control'>
                <div>
                    AI plays as: 
                    <select value={this.props.aiPlayer} onChange={this.handlePlayer}>
                        <option value={1}>Player 1</option>
                        <option value={-1}>Player 2</option>
                    </select>
                </div>
                <div>
                    Algorithm:
                    <select value={this.props.algorithm} onChange={this.handleAlgorithm}>
                        <option value='mcts'>Monte Carlo Tree Search</option>
                        <option value='ab'>Minimax with A&B Prunning</option>
                    </select>
                </div>
                <div>
                    Difficulty:
                    <input type='range' min={1} max={5} value={this.props.difficulty} onChange={this.handleDifficulty}/>
                </div>
                <button onClick={this.props.handleReset}>Restart</button>
                <h1>{this.props.message}</h1>
            </div>
        )
    }
}