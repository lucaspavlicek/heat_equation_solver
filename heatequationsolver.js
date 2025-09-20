//color slider stuff
var colorslider = document.getElementById("colorpicker");
var temp = document.getElementById("temperature");
var color;

//pen size slider stuff
var sizeslider = document.getElementById("sizepicker");
var sizeoutput = document.getElementById("size");
var size = 32;

//frame slider stuff
var frameslider = document.getElementById("framepicker");
var framedisplay = document.getElementById("frame");

//dropdown menu
var dropdown = document.getElementById("penselect");
var type;

//painting canvas
const paintcanvas = document.getElementById('paintcanvas');
const ctx = paintcanvas.getContext('2d');

//pen preview canvas
const previewcanvas = document.getElementById('pencanvas');
const previewctx = previewcanvas.getContext('2d');

//result canvas
const resultcanvas = document.getElementById('resultcanvas');
const resultctx = resultcanvas.getContext('2d');

//run button
const runbutton = document.getElementById("runbutton");

//pausebutton
const pausebutton = document.getElementById("pausebutton");

//variable to store canvas state
var drawing = ctx.getImageData(0, 0, paintcanvas.width, paintcanvas.height);

var pixelSize = 8;

//flags
var drawpermission = false;
var isDrawing = false;
var resultdone = false

main();

async function main() {
    //File can be found at cvrl.ioo.ucl.ac.uk/cmfs.htm
    colormap = await loadCSV("colortable.csv");

    await initializetoolbar();
    await initializecanvas();

    drawer();

    await until(_ => resultdone == true);

    drawpermission = false;
    runbutton.disabled = true;
    U = U.toJs();
    window.currentframe = 0;
    window.pauseflag = 0;

    showresults();


}

function until(condition) {

    const poll = resolve => {
        if (condition()) resolve();
        else setTimeout(_ => poll(resolve), 500);
    }

    return new Promise(poll);
}

async function loadCSV(filename) {
    const response = await fetch(filename);
    const text = await response.text();

    const output = Papa.parse(text, { header: false });
    console.log("Csv loaded successfully.")
    return output.data;
}

async function initializetoolbar() {
    color = findcolor(colorslider.value);
    temp.innerHTML = colorslider.value;

    size = parseInt(sizeslider.value);
    sizeoutput.innerHTML = size;

    updatepreview();
    console.log('Toolbar initialized.')
}

async function initializecanvas() {
    drawpermission = true;
    clearcanvas();
}

function drawer() {
    runbutton.onclick = function() {
        resulttext.scrollIntoView();
    }

    colorslider.oninput = function () {
        color = findcolor(this.value);
        temp.innerHTML = this.value;
        updatepreview();
    }

    sizeslider.oninput = function () {
        size = parseInt(this.value);
        sizeoutput.innerHTML = size;
        updatepreview();
    }

    dropdown.oninput = function () {
        type = this.value;
        updatepreview();
    }

    paintcanvas.addEventListener("mousedown", (e) => {
        isDrawing = true;
        drawPixel(e);
    });

    paintcanvas.addEventListener("mousemove", (e) => {
        if (isDrawing) drawPixel(e);
    });

    paintcanvas.addEventListener("mouseup", () => {
        isDrawing = false;
    });

    paintcanvas.addEventListener("mouseleave", () => {
        isDrawing = false;
    });
}

function findcolor(i) {
    r = colormap[i][0];
    g = colormap[i][1];
    b = colormap[i][2];
    return `rgb(${r}, ${g}, ${b})`;
}

function drawPixel(e) {
    if (drawpermission) {
        // Find mouse pos relative to paintcanvas
        const rect = paintcanvas.getBoundingClientRect();
        const scaleX = paintcanvas.width / rect.width;
        const scaleY = paintcanvas.height / rect.height;

        const x = Math.floor((e.clientX - rect.left) * scaleX);
        const y = Math.floor((e.clientY - rect.top) * scaleY);

        for (let i = x - size; i < x + size + 1; i++) {
            for (let j = y - size; j < y + size + 1; j++) {
                ctx.fillStyle = color; // or any color
                if (type == 'square' || Math.hypot(i - x, j - y) < size) {
                    ctx.fillRect(Math.floor(i / 8) * 8, Math.floor(j / 8) * 8, pixelSize, pixelSize);
                }
            }
        }
    }
}

function updatepreview() {
    previewctx.clearRect(0, 0, pencanvas.width, pencanvas.height);
    const center_x = 76;
    const center_y = 76;
    for (let i = center_x - size; i < center_x + size + 1; i++) {
        for (let j = center_y - size; j < center_y + size + 1; j++) {
            previewctx.fillStyle = color;
            if (type == 'square' || Math.hypot(i - center_x, j - center_y) < size) {
                previewctx.fillRect(Math.floor(i / 8) * 8, Math.floor(j / 8) * 8, pixelSize, pixelSize);
            }
        }
    }
}

function resetpage() {
    drawtext.scrollIntoView();
    location.reload();
    return false;
}

function clearcanvas() {
    ctx.fillStyle = findcolor(0); // color associated with temperature zero
    ctx.fillRect(0, 0, paintcanvas.width, paintcanvas.height);

    resultctx.fillStyle = findcolor(0); // color associated with temperature zero
    resultctx.fillRect(0, 0, resultcanvas.width, resultcanvas.height);
    console.log('Canvases reset.');
}


function sendArray(event) {
    drawing = ctx.getImageData(0, 0, paintcanvas.width, paintcanvas.height);
    console.log('Sending paint canvas data to Python.')
    return drawing.data;
}

function drawFrame(k) {
    const Uk = U[k]; // 2D array

    for (let i = 0; i < resultcanvas.height/pixelSize; i++) {
        for (let j = 0; j < resultcanvas.width/pixelSize; j++) {
            resultctx.fillStyle = findcolor(Uk[i][j]);
            resultctx.fillRect(j*8, i*8, pixelSize, pixelSize);
        }
    }
}



function showresults() {
    currentframe = parseInt(frameslider.value);
    framedisplay.innerHTML = currentframe;
    animate();



    pausebutton.onclick = function () {
        pauseflag = !pauseflag
        if (pauseflag) {
            pausebutton.innerText = '▶';
        } else {
            pausebutton.innerText = '❚❚';
        }

    }

    frameslider.oninput = function () {
        currentframe = parseInt(this.value);
        framedisplay.innerHTML = currentframe;
        drawFrame(currentframe);
    }

    
}

function animate () {
    if (!pauseflag) {
        frameslider.value = currentframe;
        framedisplay.innerHTML = currentframe;
        drawFrame(currentframe);
        currentframe = (currentframe + 1) % U.length;
    }
    setTimeout(animate, 50); // ~10 fps
}