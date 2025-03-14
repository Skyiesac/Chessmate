
function translate(y, x = null) {
    let ver = 'abcdefgh';
    if (typeof(y) == 'string' ) {
        if (x == null) { y = parseInt(y[1]); x = 'abcdefgh'.indexOf([y[0]]); }
        return (y, x);
    }
}

function get_square(y, x = null ) {
    console.log(x);
    if (typeof(y) == 'string') { return get_square(translate(y, x=x)); }
    return document.getElementById('board-'+y+'-'+x);
}

function populate_board(str_board) {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            get_square(i+1, j+1).innerText = str_board[i][j];
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {
    default_board = [];
    default_board.push("RNBQKBNR");
    default_board.push("PPPPPPPP");
    default_board.push("--------");
    default_board.push("--------");
    default_board.push("--------");
    default_board.push("--------");
    default_board.push("pppppppp");
    default_board.push("rnbqkbnr");

    console.log("HERE");
    get_square('e4');
    populate_board(default_board);
    console.log(document.getElementById('board-1-8'));
    console.log(a);
});

