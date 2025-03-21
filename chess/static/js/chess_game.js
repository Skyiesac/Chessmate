import { post_request } from "./helper_functions.js";

var csrftoken;
var flip_board_button, game_info, game_board, extra_info, to_move;
var pdict = { '-': 'empty', 'p':  'pawn', 'r':  'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king' };

function lower(s)       { return s.toLowerCase(); }
function gcolor(s)      { if (s == '-') { return 'empty'; } return lower(s) == s ? 'black' : 'white' }
function oppo(color)    { return color == 'black' ? 'white' : 'black' }
function piece_url(p)   { return chess_url_image_base + gcolor(p) + '_' + pdict[lower(p)] + '.svg' }

function set_info() {
    game_board  = parse_str_board(game_info["board"]);
    to_move     = game_info["to_move"];
    extra_info  = game_info["info"].split(";;").slice(3);
    populate_board(game_board, to_move);

    let game_stat = document.getElementById("game-status");
    if (extra_info.includes("checkmate")) {
        rem_all("to-move-piece");
        game_stat.innerText  = "Checkmate " + oppo(to_move) + " wins!";
    } else if (extra_info.includes("check")) {
        game_stat.innerText  = "Check, " + to_move + " to move.";
    } else {
        game_stat.innerText  = to_move[0].toUpperCase() + to_move.slice(1) + " to move.";
    }
}


function parse_str_board(str_board) {
    return str_board.split("\n").reverse();
}

function handle_piece(piece, addt=true) {
    piece.removeEventListener("click", second_click);
    piece.removeEventListener("click", handle_click);
    if (addt) {
        piece.classList.add("to-move-piece");
        piece.addEventListener("click", handle_click);
    } else {
        piece.classList.remove("to-move-piece");
    }
}

function populate_board(ll, to_move = false) {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (to_move && gcolor(ll[i][j]) == to_move) {
                handle_piece(get_square(i+1, j+1));
            } else {
                handle_piece(get_square(i+1, j+1), false);
            }
            get_square(i+1, j+1).innerHTML = '<img class="chess-piece-image" src="' + piece_url( ll[i][j] ) + '">';
        }
    }
}

function translate(y, x = null) {
    return  ( typeof(y) == 'string'
            ? [parseInt(y[1]), 'abcdefgh'.indexOf(y[0])]
            : 'abcdefgh'[x] + x.toString() );
}

function get_square(y, x = null) {
    return  ( typeof(y) == 'string'
            ? get_square(translate(y, x))
            : document.getElementById('board-'+y+'-'+x) );
}

function get_from_el(piece_el) {
    let id_g = piece_el.id.split("-");
    return [parseInt(id_g[1]) - 1, parseInt(id_g[2]) - 1];
}

function rem_all(class_name) {
    let els = document.getElementsByClassName(class_name);
    while (els.length >= 1) {
        els[0].classList.remove(class_name);
    }
}

function success_move(response) {
    rem_all("highlighted-piece-main");
    response.json().then(data => {
        if (data["result"] == "valid move") {
            game_info = data;
            set_info();
        } else {
            alert("invalid move");
        }
    });
}

function second_click(event) {
    let piece_main = document.getElementsByClassName("highlighted-piece-main")[0];
    let piece_second = event.target;

    let data_body = {"op": get_from_el(piece_main), "np": get_from_el(piece_second)}
    post_request("", csrftoken, data_body, success_move);
}

function highlight_add(piece) {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            if (game_board[i][j] == '-' || gcolor(game_board[i][j]) != to_move) {
                get_square(i+1, j+1).addEventListener("click", second_click);
            }
        }
    }
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
            highlight_add(piece);
        } else {
            rem_all("valid-moves");
        }
    }
    else {
        if (document.getElementsByClassName("highlighted-piece-main").length >= 1) {
            piece.classList.add("highlighted-piece-secondary");
        }
    }
}

function flip_table() {
    let table_body = document.getElementById("chess-board-table-body");
    for (const i of table_body.children) {
        table_body.prepend(i);
    }
}

document.addEventListener('DOMContentLoaded', function() {
    csrftoken           = document.querySelector('[name=csrfmiddlewaretoken]').value;
    flip_board_button   = document.getElementById("flip-board");
    game_info           = JSON.parse(document.getElementById("game-get-info").textContent);
    set_info(game_info);

    flip_board_button.addEventListener("click", (event) => {
        flip_table();
    });
});

