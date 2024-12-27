let boardMatrix = null;
let moveMatrix = null;
let cellsClicked = 0;
let turn = 1;
let possibleMoves = null;
let cellBaseColor = '#bab1b5';
let aiStarts = false;
let aiMode = false;
let confirmMoveButton = null;
let prevClicked = null;

function connectHorizontally(r, col1, col2) {
    let maxCol = Math.max(col1, col2);
    let minCol = Math.min(col1, col2);
    for (let i = minCol + 1; i < maxCol ; i++) {
        if (!moveMatrix[r][i]) {
            moveMatrix[r][i] = 1;
            cellsClicked++;
        }
    }
    updateCellsAfterMove(moveMatrix);
    // console.log(cellsClicked);
}

function hexConnectVertically(row1, col1, row2, col2) {
    // console.log(row1, col1, row2, col2);
    let counter = 1;
    if (row1 < row2 && col1 < col2 + (row2 > getBoardDimension())) {
        // counter++;
        for (let i = row1+1; i < row2; i++) {
            let j = i < getBoardDimension() ? col1 + counter : col2;
            counter++;
            if (!moveMatrix[i][j]) {
                moveMatrix[i][j] = 1
                cellsClicked++;
            }
        }
    } else if (row1 < row2 && col1 >= col2) {
        for (let i = row2-1; i > row1; i--) {
            let j = i < getBoardDimension() ? col1 : col2 + counter;
            counter++;
            if (!moveMatrix[i][j]) {
                moveMatrix[i][j] = 1
                cellsClicked++;
            }
        }
    } else {
        hexConnectVertically(row2, col2, row1, col1);
    }
    // console.log(cellsClicked);
}

function triConnectVertically(row1, col1, row2, col2) {
    if (row1 < row2 &&  col1 >= col2 || row1 < row2 && (row2-row1) > (col2-col1)) {
        let rowLength = moveMatrix[row1].length;
        let counter = rowLength - col1;
        if (col1 % 2) {
            moveMatrix[row1][rowLength - counter -1] = 1;
            counter++;
        }
        for (let i=row1+1; i <= row2; i++) {
            rowLength = moveMatrix[i].length;
            if (i !== row2 || (rowLength - counter - 1) >= col2) {
                moveMatrix[i][rowLength - counter - 1] = 1;
                counter++;
            }
            if (i !== row2 || (rowLength - counter - 1) >= col2) {
                moveMatrix[i][rowLength - counter -1] = 1;
                counter++;
            }
        }
    } else if (row1 < row2 && col1 < col2) {
        let counter = 1;
        if (col1 % 2) {
            moveMatrix[row1][col1+counter] = 1;
            counter++;
        }
        for (let i=row1+1; i <= row2; i++) {
            if (col1+counter <= col2) {
                moveMatrix[i][col1+counter] = 1;
                counter++;
            }
            if (col1+counter <= col2) {
                moveMatrix[i][col1+counter] = 1;
                counter++;
            }
        }
    } else {
        triConnectVertically(row2, col2, row1, col1);
    }
    updateCellsAfterMove(moveMatrix);

}

function connectVertically(row1, col1, row2, col2) {
    if (getGameMode() === 'triangular') {
        triConnectVertically(row1, col1, row2, col2);
    } else {
        hexConnectVertically(row1, col1, row2, col2);
    }
    updateCellsAfterMove(moveMatrix);
}



function hexFillPolygon() {
    for (let i=0; i<moveMatrix.length; i++) {
        const sum = moveMatrix[i].reduce((partialSum, a) => partialSum + a, 0);
        if (sum !== 2) continue;
        let start = 0;
        for (let j=0; j<moveMatrix[i].length; j++) {
            if (moveMatrix[i][j]) {
                start = 1 - start;
            } else {
                moveMatrix[i][j] = start;
            }
        }
    }
}
function triFillPolygon() {
    for (let i=0; i<moveMatrix.length; i++) {
        const sum = moveMatrix[i].reduce((partialSum, a) => partialSum + a, 0);
        if (sum !== 4) continue;
        let start = 0;
        for (let j=0; j<moveMatrix[i].length; j++) {
            if (moveMatrix[i][j]) {
                start++;
            } else {
                moveMatrix[i][j] = start && start < 4 ? 1 : 0;
            }
        }
    }
}

function fillPolygon() {
    if (getGameMode() === 'triangular') {
        triFillPolygon();
    } else {
        hexFillPolygon();
    }
    updateCellsAfterMove(moveMatrix);
}

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
    if (prevClicked) {
        if (row === prevClicked[0]) {
            connectHorizontally(row, prevClicked[1], col);
        } else {
            connectVertically(prevClicked[0], prevClicked[1], row, col);
        }
    }
    // else {
    //     cellsClicked ++;
    // }
    prevClicked = [row, col];
    // if(moveMatrix[row][col]) {
    //     unclickCell(row, col);
    //     moveMatrix[row][col] = 0;
    //     cellsClicked--;
    //     return;
    // }
    //
    // if (cellsClicked > turn + 1) {
    //     alert(`You can click at most ${turn+1} cells`);
    //     cellsClicked--;
    //     return;
    // }
    //
    if (moveMatrix[row][col]) {
        // alert('zaznaczone');
        fillPolygon();
    } else {
        cellsClicked++;
    }
    moveMatrix[row][col] = 1;
    cell.style.backgroundColor = getColorForTurn(turn);
    cell.innerHTML = turn;
    // console.log(cellsClicked);
}

function updateCellsAfterMove(matrix) {
    let updated = false;
    for (let i=0; i < matrix.length; i++) {
        for (let j = 0; j<matrix[i].length; j++) {
            if (matrix[i][j]) {
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

function toggleClicks(disable) {
    let cellClass = getGameMode() + '-cell';
    let cells = document.getElementsByClassName(cellClass);
    Array.from(cells).forEach(cell => {
        cell._disabled = disable;
    })
}

function getFinalBoard() {
    let cellClass = getGameMode() + '-cell';
    let cells = document.getElementsByClassName(cellClass);
    let board = getBoardMatrix();
    Array.from(cells).forEach(cell => {
        if (cell.innerHTML) {
            let cellId = cell.id.split(";");
            let i = cellId[0];
            let j = cellId[1];
            board[i][j] = parseInt(cell.innerHTML);
        }
    })
    return board;
}

function revertMove() {
    for(let i=0; i < moveMatrix.length; i++) {
        for(let j = 0; j<moveMatrix[i].length; j++) {
            if (moveMatrix[i][j]) {
                unclickCell(i, j);
            }
        }
    }
    moveMatrix = getBoardMatrix();
    cellsClicked = 0;
    prevClicked = null;
    toggleClicks(false);
}

function confirmMove() {
    if (confirmMoveButton._disabled) return;
    confirmMoveButton._disabled = true;
    const startTime = Date.now();
    toggleClicks(true);

    console.log('Board matrix:', boardMatrix);
    console.log('Move matrix:', moveMatrix);
    let moveMatrixJSON = JSON.stringify(moveMatrix);
    if (!possibleMoves.includes(moveMatrixJSON)) {
        alert('Not a valid move')
        revertMove();
        confirmMoveButton._disabled = false;
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
        if(updateCellsAfterMove(boardMatrix)) {
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
            let winnerHeader = document.getElementById('winner-header');
            winnerHeader.innerHTML = `Player ${turn % 2 + 1} wins!`;
            if (aiMode) {
                if ((aiStarts && ((turn+1) % 2 === 1)) || (!aiStarts && ((turn+1) % 2 === 0)))  {
                    winnerHeader.innerHTML = `AI wins!`;
                    let turnSpan = document.getElementById('turn-span');
                    if (turnSpan) {
                        turnSpan.innerHTML = String(turn-1);
                    }
                } else {
                    winnerHeader.innerHTML = `Player wins!`;
                }
            }
            saveGame();
            toggleClicks(true);

        }
        const endTime = Date.now();
        console.log(`Elapsed time: ${endTime - startTime} ms`);
        toggleClicks(false);
        confirmMoveButton._disabled = false;
        prevClicked = null;

    })
    .catch(error => {
        console.error("There was an error:", error);
    });
}

function saveGame() {
    fetch('/save_game/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            board_size: getBoardDimension(),
            game_mode: getGameMode(),
            ai_starts: aiStarts,
            ai_mode: aiMode,
            board: getFinalBoard(),
            turns: turn - 1
        }),
    })
    .then(response => {
        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        if (response.status === 204) {
            console.log("Game saved successfully, no content returned.");
            return null;
        }

        return response.json();
    })
    .then(data => {
        if (data) {
            console.log("Response data:", data);
        }
    })
    .catch(error => {
        console.error("There was an error:", error);
    });
}


function startGame() {
    const startTime = Date.now();
    toggleClicks(true);

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
        if(updateCellsAfterMove(boardMatrix)) {
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
        toggleClicks(false);


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
    prevClicked = null;
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



