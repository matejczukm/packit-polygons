let boardMatrix = null;

function yap(text) {
    console.log(text);
}

function onClickCell(row, col) {
    if(!boardMatrix) {
        boardMatrix = getBoardMatrix();
    }
    if(boardMatrix[row][col]) {
        alert('Cell already clicked');
        return;
    }
    yap(`Row: ${row}, col: ${col}`);
    boardMatrix[row][col] = 1;
    yap(boardMatrix);
}

function createCell(className, row, col) {
    let cell = document.createElement("div");
    cell.className = className;
    cell.id = `${row};${cell}`;
    cell.addEventListener('click', () => {
        onClickCell(row, col);
        cell.style.backgroundColor = 'orange';
    });
    return cell;
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
            for (let j=1; j <= 1 + 2*i; j++) {
                row.appendChild(
                    createCell("triangular-cell", i, j)
                );
            }
            grid.appendChild(row);
        }
    }
    boardMatrix = getBoardMatrix();
    updateSizes();
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



