var game_data = {};
var game_delay = 1000;

$(document).ready(function () {
    var canvas = $("#game");

    canvas.width(500);
    canvas.height(500);

    // window.setInterval(function () {
    //
    //     $.ajax({
    //         url:"/gamedata.json"
    //     }).done(function (data) {
    //         game_data = JSON.parse(data);
    //         drawGame();
    //     });
    // }, game_delay);
    drawGame();

    
});


function drawGame() {
    var ctx = $("#game")[0].getContext('2d');
    ctx.imageSmoothingEnabled= false;
    ctx.translate(.5, .5);


    ctx.fillRect(0, 0, 10, 10);
}