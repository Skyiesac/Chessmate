
let pdict = { '-': 'empty', 'p':  'pawn', 'r':  'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king' };
function lower(s)       { return s.toLowerCase(); }
function gcolor(s)      { if (s == '-') { return 'empty'; } return lower(s) == s ? 'black' : 'white' }
function piece_url(p)   { return chess_url_image_base + gcolor(p) + '_' + pdict[lower(p)] + '.svg' }
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

function rem_all(class_name) {
    let els = document.getElementsByClassName(class_name);
    for (let i = 0; i < els.length; i++) {
        els[i].classList.remove(class_name);
    }
}

function valid_move(piece) {
    return piece;
}

function handle_click(event) {
    let piece = event.target;
    rem_all('highlighted-piece-secondary');
    if (piece.classList.contains("to-move-piece")) {
        let z = piece.classList.contains("highlighted-piece-main");
        rem_all('highlighted-piece-main');
        if (!z) {
            piece.classList.add("highlighted-piece-main");
            valid_move(piece);
        } else {
            rem_all("valid-moves");
        }
    }
    else {
        if (document.getElementsByClassName("highlighted-piece-main").length >= 1) {
            console.log("HI");
            piece.classList.add("highlighted-piece-secondary");
        }
    }
}

function handle_piece(piece, addt = true) {
    if (addt) {
        piece.classList.add("to-move-piece");
        piece.addEventListener("click", handle_click);
    } else {
        piece.classList.remove("to-move-piece");
        piece.removeEventListener("click", handle_click);
    }
}

function populate_board(ll, rev = false, to_move = false) {
    if (rev) { populate_board(ll.reverse()) };
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (to_move && gcolor(ll[i][j]) == to_move) {
                handle_piece(get_square(i+1, j+1));
            } else {
                handle_piece(get_square(i+1, j+1), addt = false);
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

