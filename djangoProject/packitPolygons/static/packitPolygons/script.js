let boardMatrix = null;
let moveMatrix = null;
let cellsClicked = 0;
let turn = 1;
let possibleMoves = null;
let cellBaseColor = '#bab1b5';
let aiStarts = false;
let aiMode = false;
let confirmMoveButton = null;

function startAiMode(doesAIStart) {
    // console.log(doesAIStart);
    let popUp = document.getElementById("ai-popup");
    popUp.classList.remove("open");
    aiStarts = doesAIStart;
    aiMode = true;
    generateGrid();
    // if (aiStarts) {
    //     confirmMoveButton._disabled = true;
    // }
}

function changeToNormalMode() {
    // aiStarts = null;
    aiMode = false;
    generateGrid();
    // confirmMoveButton._disabled = true;

}

function openAiPopUp() {
    let popUp = document.getElementById("ai-popup");
    popUp.classList.add("open");
}

function onClickCell(row, col, cell) {
    if(cell._disabled) return;
    if(!moveMatrix) {
        moveMatrix = getBoardMatrix();
    }
    if(boardMatrix[row][col]) {
        alert('Cell already clicked');
        return;
    }
    if(moveMatrix[row][col]) {
        unclickCell(row, col);
        moveMatrix[row][col] = 0;
        cellsClicked--;
        return;
    }
    cellsClicked ++;

    if (cellsClicked > turn + 1) {
        alert(`You can click at most ${turn+1} cells`);
        cellsClicked--;
        return;
    }

    // console.log(`Row: ${row}, col: ${col}`);
    moveMatrix[row][col] = turn;
    // console.log(moveMatrix);
    // console.log('Move matrix: ')
    // console.log(JSON.stringify(moveMatrix))
    cell.style.backgroundColor = getColorForTurn(turn);
    cell.innerHTML = turn;
}

function updateCellsAfterMove(board) {
    let updated = false;
    for (let i=0; i < boardMatrix.length; i++) {
        for (let j = 0; j<boardMatrix[i].length; j++) {
            if (boardMatrix[i][j]) {
                let cellID = `${i};${j}`;
                let cell = document.getElementById(cellID);
                if (cell.innerHTML === '') {
                    cell.innerHTML = turn;
                    cell.style.backgroundColor = getColorForTurn(turn);
                    updated = true;
                }
            }
        }
    }
    return updated;
}

function unclickCell(i, j) {
    let cellID = `${i};${j}`;
    let cell = document.getElementById(cellID);
    if (boardMatrix[i][j]) {
        cell.innerHTML = boardMatrix[i][j];
        cell.style.backgroundColor = getColorForTurn(boardMatrix[i][j]);
    } else {
        cell.innerHTML = '';
        cell.style.backgroundColor = cellBaseColor;
    }
}

function disableClicks() {
    let cellClass = getGameMode() + '-cell';
    // console.log(cellClass);
    let cells = document.getElementsByClassName(cellClass);
    // console.log(cells[0]);
    Array.from(cells).forEach(cell => {
        // cell.removeEventListener('click', onClickCell);
        cell._disabled = true;
    })
}

function revertMove() {
    for(let i=0; i < moveMatrix.length; i++) {
        for(let j = 0; j<moveMatrix[i].length; j++) {
            if (moveMatrix[i][j] === turn) {
                unclickCell(i, j);
            }
        }
    }
    moveMatrix = getBoardMatrix();
    cellsClicked = 0;
}

function confirmMove() {
    if (confirmMoveButton._disabled) return;
    confirmMoveButton._disabled = true;
    const startTime = Date.now();

    console.log('Board matrix:', boardMatrix)
    // console.log('Possible moves')
    // console.log(possibleMoves);
    // console.log('Current move')
    // console.log(JSON.stringify(moveMatrix))
    // console.log('Move is valid:')
    // console.log(possibleMoves.includes(JSON.stringify(moveMatrix)))
    let moveMatrixJSON = JSON.stringify(moveMatrix);
    if (!possibleMoves.includes(moveMatrixJSON)) {
        alert('Not a valid move')
        revertMove();
        return;
    }
    turn ++;
    const response = fetch( '/confirm_move/', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body : JSON.stringify({
            board : boardMatrix,
            move : moveMatrix,
            turn : turn,
            game_mode : getGameMode(),
            ai_starts : aiStarts,
            ai_mode : aiMode
        })
        }
    )
    .then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
    })
    .then(data => {
        console.log("Move confirmed:", data);
        possibleMoves = data.moves;
        boardMatrix = data.board;
        // console.log(data.board)
        // console.log('Current board', boardMatrix);
        if(updateCellsAfterMove()) {
            turn++;

        }
        if(possibleMoves.length > 0) {
            moveMatrix = getBoardMatrix();
            cellsClicked = 0;
            if (!aiMode) {
                let winnerHeader = document.getElementById('winner-header');
                winnerHeader.innerHTML = `Players ${(turn + 1) % 2 + 1} turn`;
            }
            let turnSpan = document.getElementById('turn-span');
            if (turnSpan) {
                turnSpan.innerHTML = String(turn);
            }
        } else {
            // alert('Game finished');
            let winnerHeader = document.getElementById('winner-header');
            winnerHeader.innerHTML = `Player ${turn % 2 + 1} wins!`;
            if (aiMode) {
                if ((aiStarts && ((turn+1) % 2 === 1)) || (!aiStarts && ((turn+1) % 2 === 0)))  {
                    winnerHeader.innerHTML = `AI wins!`;
                } else {
                    winnerHeader.innerHTML = `Player wins!`;
                }
            }

            disableClicks();

        }
        const endTime = Date.now();
        console.log(`Elapsed time: ${endTime - startTime} ms`);
        confirmMoveButton._disabled = false;

    })
    .catch(error => {
        console.error("There was an error:", error);
    });
}

function startGame() {
    const startTime = Date.now();

    const response = fetch( '/start_game/', {
        method: 'POST',
        headers: {
        'Content-Type': 'application/json'
        },
        body : JSON.stringify({
            board_size : getBoardDimension(),
            game_mode : getGameMode(),
            ai_starts : aiStarts,
            ai_mode : aiMode
        }),
        }
    )
    .then(response => {
    if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
    })
    .then(data => {
        console.log("Game started:", data);
        possibleMoves = data.moves;
        boardMatrix = data.board;
        if(updateCellsAfterMove()) {
            turn++;
            let turnSpan = document.getElementById('turn-span');
            if (turnSpan) {
                turnSpan.innerHTML = String(turn);
            }
        }
        if (!aiMode) {
                let winnerHeader = document.getElementById('winner-header');
                winnerHeader.innerHTML = `Players ${(turn + 1) % 2 + 1} turn`;
            }
        confirmMoveButton._disabled = false;
        const endTime = Date.now();
        console.log(`Elapsed time: ${endTime - startTime} ms`);


    })
    .catch(error => {
        console.error("There was an error:", error);
    });
}

function createCell(className, row, col) {
    let cell = document.createElement("div");
    cell.className = className;
    cell.id = `${row};${col}`;
    cell.innerHTML = '';
    cell.addEventListener('click', () => {
        onClickCell(row, col, cell);
    });
    cell._disabled = false;
    return cell;
}

function getColorForTurn(turn) {
    const hue = (turn * 137) % 360;
    return `hsl(${hue}, 70%, 60%)`;
}

function createRow(className) {
    let row = document.createElement("div");
    row.className = className;
    return row;
}

function getGameMode() {
    let hexGrid = document.querySelector('.hexagonal-grid');
    let triGrid = document.querySelector('.triangular-grid');
    if (hexGrid) {
        return 'hexagonal';
    } else if (triGrid) {
        return 'triangular';
    } else {
        throw new Error('Invalid game mode');
    }
}

function getHexagonalRowSize(rowNumber, dim) {
    return  (rowNumber < dim) ?  (dim + rowNumber): (3*dim-2-rowNumber);
}

function getBoardDimension() {
    const dim = document.getElementById("dim-input").value;
    return parseInt(dim, 10);
}

function generateGrid() {
    // function generates html structure based on the selected dimension of the board
    const dim = getBoardDimension();
    let classPrefix = getGameMode();

    let gridClass = `${classPrefix}-grid`;
    let grid = document.getElementsByClassName(gridClass)[0];

    grid.innerHTML = '';

    if (classPrefix === 'hexagonal') {
        for (let i = 0; i < 2 * dim -1; i++) {
            let row = createRow("hexagonal-row");
            let numCells = getHexagonalRowSize(i, dim);
            for (let j = 0; j < numCells; j++) {
                row.appendChild(
                    createCell("hexagonal-cell", i, j)
                );
            }
            grid.appendChild(row);
        }
    } else {
        for (let i=0; i < dim; i++) {
            let row = createRow("triangular-row");
            for (let j=0; j < 1 + 2*i; j++) {
                row.appendChild(
                    createCell("triangular-cell", i, j)
                );
            }
            grid.appendChild(row);
        }
    }
    boardMatrix = getBoardMatrix();
    moveMatrix = getBoardMatrix();
    cellsClicked = 0;
    turn = 1;
    updateSizes();
    let turnSpan =  document.getElementById('turn-span');
    if (turnSpan){
        turnSpan.innerHTML = String(turn);
    }
    startGame();
    let winnerHeader = document.getElementById('winner-header');
    winnerHeader.innerHTML = '';
    confirmMoveButton = document.getElementsByClassName('move-button')[0];
    confirmMoveButton._disabled = true;
}

function loadBoard() {
    // on load function
    generateGrid();
    boardMatrix = getBoardMatrix();

    // const openBtn = document.getElementById("openModal");
    // const closeBtn = document.getElementById("closeModal");
    // const modal = document.getElementById("modal");
    //
    // openBtn.addEventListener("click", () => {
    //     modal.classList.add("open");
    // });
    //
    // closeBtn.addEventListener("click", () => {
    //     modal.classList.remove("open");
    // });
}
function updateSizes() {
    // Updates the sizes of cells to maintain a consistent board size,
    // adjusting cell dimensions based on the number of cells or board dimensions.
    const dim = getBoardDimension();
    let hexGrid = document.querySelector('.hexagonal-grid');
    let triGrid = document.querySelector('.triangular-grid');
    if (hexGrid) {
        hexGrid.style.setProperty('--s', 280/dim + 'px')
    } else if (triGrid) {
        triGrid.style.setProperty('--s', 390/dim + 'px')
    }
    console.log(boardMatrix);
}

function getHexagonalBoardGame() {
    const dim = getBoardDimension();
    let boardMatrix = [];
    for (let i = 0; i < 2 * dim -1; i++) {
        let row = [];
        let numCells = getHexagonalRowSize(i, dim);

        for (let j = 0; j < numCells; j++) {
            row.push(0);
        }
        boardMatrix.push(row);
    }
    return boardMatrix;
}

function getTriangularBoardGame() {
    const dim = getBoardDimension();
    let boardMatrix = [];
    for (let i = 0; i < dim; i++) {
        let row = [];
        for (let j = 1; j <= 1 + 2 * i; j++) {
            row.push(0);
        }
        boardMatrix.push(row);
    }
    return boardMatrix;
}

function getBoardMatrix() {
    let gameMode = getGameMode();
    if (gameMode === 'hexagonal') {
        return getHexagonalBoardGame();
    } else {
        return getTriangularBoardGame();
    }
}



