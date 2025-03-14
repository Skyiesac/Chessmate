
// chess_url_image_base defined in chess_home.html, script (#load-image-z)

let piece_dict = {
    '-': 'empty',
    'p':  'pawn',
    'r':  'rook', 'n': 'knight', 'b': 'bishop', 'q': 'queen', 'k': 'king'
};

function lower(s) {
    return s.toLowerCase();
}

function gcolor(s) {
    if (s == '-') { return 'empty'; }
    return lower(s) == s ? 'black' : 'white'
}

function piece_url(p) {
    let color = gcolor(p);
    return chess_url_image_base + color + '_' + piece_dict[lower(p)] + '.svg';
}

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

function populate_board(ll) {
    for (let i = 0; i < 8; i++) {
        for (let j = 0; j < 8; j++) {
            let purl = piece_url( ll[i][j] );
            get_square(i+1, j+1).innerHTML = '<img class="chess-piece-image" src="' + purl + '">';
        }
    }
}


document.addEventListener('DOMContentLoaded', function() {

    console.log(gcolor('k'));
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
    console.log(piece_url('k'));
});

