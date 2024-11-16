let boardMatrix = null;
let moveMatrix = null;
let cellsClicked = 0;
let turn = 1;

function onClickCell(row, col, cell) {
    if(!moveMatrix) {
        moveMatrix = getBoardMatrix();
    }
    if(moveMatrix[row][col]) {
        alert('Cell already clicked');
        return;
    }
    cellsClicked ++;

    if (cellsClicked > turn + 1) {
        alert(`You can click at most ${turn+1} cells`);
        return;
    }
    console.log(`Row: ${row}, col: ${col}`);
    moveMatrix[row][col] = 1;
    console.log(moveMatrix);
    cell.style.backgroundColor = getColorForTurn(turn);
    cell.innerHTML = turn;
}

function confirmMove() {
    turn ++;
    // moveMatrix = getBoardMatrix();
    cellsClicked = 0;
    let turnSpan =  document.getElementById('turn-span');
    if (turnSpan){
        turnSpan.innerHTML = String(turn);
        // console.log('turn span found')
    }
}

// function startGame() {
//     const response = fetch( '/start_game/', {
//         method: 'POST',
//         body : JSON.stringify({board_size : getBoardDimension()})
//         }
//     );
//     console.log(response);
// }

function createCell(className, row, col) {
    let cell = document.createElement("div");
    cell.className = className;
    cell.id = `${row};${col}`;
    cell.addEventListener('click', () => {
        onClickCell(row, col, cell);
    });
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
        // console.log('turn span found')
    }
    // startGame();
}

function loadBoard() {
    // on load function
    generateGrid();
    boardMatrix = getBoardMatrix();
    // console.log(boardMatrix);
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



