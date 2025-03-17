
let pdict = { '-': 'empty', 'p':  'pawn', 'r':  'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king' };

function lower(s) { return s.toLowerCase(); }

function gcolor(s) { if (s == '-') { return 'empty'; } return lower(s) == s ? 'black' : 'white' }

function piece_url(p) { return chess_url_image_base + gcolor(p) + '_' + pdict[lower(p)] + '.svg' }

function translate(y, x = null) {
    return  ( typeof(y) == 'string'
            ? [parseInt(y[1]), 'abcdefgh'.indexOf(y[0])]
            : 'abcdefgh'[x] + x.toString() );
}

function get_square(y, x = null) {
    return  ( typeof(y) == 'string'
            ? get_square(translate(y, x=x))
            : document.getElementById('board-'+y+'-'+x) );
}

function add_highlight() {
    if (piece.classList.contains("highlight-piece")) {
        piece.remove
    }
    else {
    }
}

function populate_board(ll, rev = false, to_move = false) {
    if (rev) { populate_board(ll.reverse()) };
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (to_move && gcolor(ll[i][j]) == to_move) {
                get_square(i+1, j+1).classList.add("to-move-piece");
                //get_square(i+1, j+1).addEventListener("click", add_highlight);
            } else {
                get_square(i+1, j+1).classList.remove("to-move-piece");
            }
            get_square(i+1, j+1).innerHTML = '<img class="chess-piece-image" src="' + piece_url( ll[i][j] ) + '">';
        }
    }
}


function get_id(p_id) {
    return p_id;
}


document.addEventListener('DOMContentLoaded', function() {
    let flip_board_button = document.getElementById("flip-board");
    let game_info         = JSON.parse(document.getElementById("game-get-info").textContent);
    let game_board        = game_info.board.split("\n").reverse();
    let to_move           = game_info.to_move;
    let ord               = false;

    populate_board(game_board, rev=false, to_move=to_move);
    console.log(game_info);

    flip_board_button.addEventListener("click", (event) => {
        populate_board(game_board, rev=(! ord), to_move = to_move);
    });
});

