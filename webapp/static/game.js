
var game_data = {
    blocks: []
};
var game_delay = 1000;
var canvas_offset_x = 0;
var canvas_offset_y = 0;
var canvas_zoom = 10;
var selected_block ={};
setColor("#F00");
var xhover = 0;
var yhover = 0;

var dragging = null;

var next_block = Date.now()+1000;

$(document).ready(function () {
    var canvas = $("#game");
    canvas[0].width = $(document).width();
    canvas[0].height = $(document).height();
    var ctx = canvas[0].getContext('2d');
    ctx.imageSmoothingEnabled = false;
    ctx.translate(.5, .5);
    ctx.scale(canvas_zoom, canvas_zoom);

    window.setInterval(function () {
        updateTimeout();

        $.ajax({
            url:"/gamedata.json",
            method: "POST"
        }).done(function (data) {
            game_data = JSON.parse(data);
            drawGame();
        });
    }, game_delay);
    drawGame(canvas, ctx);
    
    canvas.click(function (e) {
        if(selected_block.type === "pan" || !cooldownReady()) {
            return;
        }

        var elm = $(this);
        selected_block.x = Math.round((e.pageX - elm.offset().left - canvas_offset_x) / canvas_zoom);
        selected_block.y = Math.round((e.pageY - elm.offset().top - canvas_offset_y) / canvas_zoom);

        if(selected_block.type === "remove") {
            for(var i = 0; i < game_data.blocks.length; i++) {
                var b = game_data.blocks[i];
                if(b.x === selected_block.x && b.y === selected_block.y) {
                    b.health = Math.floor(b.health-1);
                    if(b.health <= 0)
                        game_data.blocks.splice(i, 1);

                    sendBlock(selected_block);
                    drawGame(canvas, ctx);
                    break;
                }
            }
            return;
        }


        var b2p = Object.assign({}, selected_block);
        for(var i = 0; i < game_data.blocks.length; i++) {
            var b = game_data.blocks[i];
            if(b.x === b2p.x && b.y === b2p.y) {
                b2p.health = Math.floor(b.health+1);
                game_data.blocks.splice(i, 1);
                break;
            }
        }
        game_data.blocks.push(b2p);
        sendBlock(b2p);
        drawGame(canvas, ctx);
    });

    canvas.mousedown(function (e) {
        if(selected_block.type === "pan") {
            canvas.css({"cursor": "grabbing"});
            dragging = {x:e.pageX, y:e.pageY};
        }
    }).mousemove(function (e) {
        if(dragging !==null) {

            var offset_x = (e.pageX - dragging.x);
            var offset_y = (e.pageY - dragging.y);
            canvas_offset_x+=offset_x;
            canvas_offset_y+=offset_y;
            ctx.translate(offset_x/canvas_zoom, offset_y/canvas_zoom);
            dragging = {x:e.pageX, y:e.pageY};
            drawGame(canvas, ctx);

        }
    }).mouseup(function () {
        if(selected_block.type === "pan") {
            canvas.css({"cursor": "grab"});
            dragging = null;
        }
    });

    canvas.mousemove(function (e) {
        var elm = $(this);
        xhover = Math.round((e.pageX - elm.offset().left - canvas_offset_x)/canvas_zoom);
        yhover = Math.round((e.pageY - elm.offset().top  - canvas_offset_y)/canvas_zoom);
        drawGame(canvas, ctx);
    });

    $(".select").click(function () {
        canvas.css({"cursor": "none"});
        $(".select").removeClass("select-selected");
        $(this).addClass("select-selected");
    })

    $(".select-pan").click( function () {
        setSelectedBlock({
            type: "pan",
            color: "#0000"
        });
        canvas.css({"cursor": "grab"});
    });

    $(".select-remove").click( function () {
        setSelectedBlock({
            type: "remove",
            color: "#000",
            cooldown:0
        });
    });

    $(".select-red").click(    function () {setColor("#F00");});
    $(".select-green").click(  function () {setColor("#0F0");});
    $(".select-blue").click(   function () {setColor("#00F");});
    $(".select-cyan").click(   function () {setColor("#0FF");});
    $(".select-magenta").click(function () {setColor("#F0F");});
    $(".select-yellow").click( function () {setColor("#FF0");});

});

function setSelectedBlock(block) {
    selected_block = block;

}

function setColor(c) {

    setSelectedBlock({
        type: "basic",
        color: c,
        health: 1.0,
        cooldown: 0,
        x: 0,
        y: 0
    });
}

function cooldownReady() {
    return next_block - Date.now() <= 0;
}

function updateTimeout() {
    var secsRemaining = Math.round((next_block - Date.now())/1000);

    if(secsRemaining <= 0) {
        $("#countdown").text("0:00");
    } else {
        var mins = Math.round(secsRemaining/60);
        var secs = secsRemaining % 60;
        if(secs < 10)
            secs = "0"+secs;
        $("#countdown").text(mins+":"+secs);
    }
}

function sendBlock(b) {
    $.ajax({
        url: "/place_block/",
        data: JSON.stringify(b),
        method: "POST"
    }).done(function (data) {
        game_data = JSON.parse(data);
        drawGame();
    }).fail(function () {
       // window.alert("shits broken yo. Reload the page I guess idk");
    });
}

function drawGame(canvas, ctx) {

    ctx.save();
    ctx.setTransform(1, 0, 0, 1, 0, 0);
    ctx.clearRect(0, 0, canvas[0].width, canvas[0].height);
    ctx.restore();

    for (var i = 0; i < game_data.blocks.length; i++) {
        var block = game_data.blocks[i];
        ctx.fillStyle = block.color;
        ctx.fillRect(block.x, block.y, 1, 1);
        ctx.fillStyle = "#000" + Math.floor(Math.min(9, block.health));
        ctx.fillRect(block.x, block.y, 1, 1);
    }

    ctx.strokeStyle = selected_block.color;
    ctx.lineWidth=1/canvas_zoom;
    ctx.strokeRect(xhover, yhover, 1, 1);
}