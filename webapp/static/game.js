
var game_data = {
    blocks: [
        {
            type: "basic",
            color: "#F00",
            damage: .5,
            x: 10,
            y: 10
        }
    ]
};
var game_delay = 1000;
var canvas_offset_x = 0;
var canvas_offset_y = 0;
var canvas_zoom = 10;
var selected_block = {
    type: "basic",
    color: "#F00",
    damage: .5,
    x: 0,
    y: 0
};
var xhover = 0;
var yhover = 0;

var isDragging;

$(document).ready(function () {
    var canvas = $("#game");
    canvas[0].width = 500;
    canvas[0].height = 500;
    var ctx = canvas[0].getContext('2d');
    ctx.imageSmoothingEnabled = false;
    ctx.translate(.5, .5);
    ctx.scale(canvas_zoom, canvas_zoom);
    console.log("this happens once");


    // window.setInterval(function () {
    //
    //     $.ajax({
    //         url:"/gamedata.json"
    //     }).done(function (data) {
    //         game_data = JSON.parse(data);
    //         drawGame();
    //     });
    // }, game_delay);
    drawGame(canvas, ctx);
    
    canvas.click(function (e) {
        if(selected_block.type === "pan") {

            return;
        }
        var elm = $(this);
        selected_block.x = Math.round((e.pageX - elm.offset().left)/canvas_zoom) + canvas_offset_x;
        selected_block.y = Math.round((e.pageY - elm.offset().top)/canvas_zoom)  + canvas_offset_y;
        game_data.blocks.push(Object.assign({}, selected_block));
        drawGame(canvas, ctx);
    });

    canvas.mousedown(function () {
        if(selected_block.type === "pan") {
            canvas.css({"cursor": "grabbing"});
        }
    }).mouseup(function () {
        if(selected_block.type === "pan") {
            canvas.css({"cursor": "grab"});
        }
    });


    canvas.mousemove(function (e) {
        var elm = $(this);
        xhover = Math.round((e.pageX - elm.offset().left)/canvas_zoom) + canvas_offset_x;
        yhover = Math.round((e.pageY - elm.offset().top)/canvas_zoom)  + canvas_offset_y;
        drawGame(canvas, ctx);
    });

    $(".select").click(function () {
        canvas.css({"cursor": "none"});
        $(".select").removeClass("select-selected");
        $(this).addClass("select-selected");
    })

    $(".select-pan").click( function () {
        setBlock({
            type: "pan",
            color: "#0000"
        });
        canvas.css({"cursor": "grab"});
    });

    $(".select-red").click(    function () {setColor("#F00");});
    $(".select-green").click(  function () {setColor("#0F0");});
    $(".select-blue").click(   function () {setColor("#00F");});
    $(".select-cyan").click(   function () {setColor("#0FF");});
    $(".select-magenta").click(function () {setColor("#F0F");});
    $(".select-yellow").click( function () {setColor("#FF0");});

});

function setBlock(block) {
    selected_block = block;

}

function setColor(c) {
    setBlock({
        type: "basic",
        color: c,
        damage: .5,
        x: 0,
        y: 0
    });
}

function drawGame(canvas, ctx) {

    // Store the current transformation matrix
    ctx.save();

    // Use the identity matrix while clearing the canvas
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas[0].width, canvas[0].height);

    // Restore the transform
    ctx.restore();

    for (var i = 0; i < game_data.blocks.length; i++) {
        var block = game_data.blocks[i];
        ctx.fillStyle = block.color;
        ctx.fillRect(block.x, block.y, 1, 1);
    }

    ctx.strokeStyle = selected_block.color;
    ctx.lineWidth=1/canvas_zoom;
    ctx.strokeRect(xhover, yhover, 1, 1);
}