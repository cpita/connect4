import React from 'react'

export default function Cell(props){

    const renderToken = () => {
        if(props.value === 1){
            return (
                <div className='red' style={getTokenStyles()}></div>
            )
        }else if(props.value === -1){
            return (
                <div className='black' style={getTokenStyles()}></div>
            )
        }
    }

    const getTokenStyles = () => {
        if(props.gameState === 'RUNNING' || props.isWinningCell) return {
            opacity: '1'
        }
        return {
            opacity: '0.5'
        }
    }

    const getCellStyles = () => {
        return {
            pointerEvents: props.gameState === 'RUNNING' && props.allowedEvents ? 'auto': 'none',
        }
    }

    return (
        <div className='Cell' onClick={() => props.handleClick(props.column)} style={getCellStyles()}>
            {renderToken()}
        </div>
    )
}