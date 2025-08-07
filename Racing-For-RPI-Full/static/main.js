const rpmCanvas = document.getElementById("rpmGauge");
const speedCanvas = document.getElementById("speedGauge");
const rpmCtx = rpmCanvas.getContext("2d");
const speedCtx = speedCanvas.getContext("2d");

function drawGauge(ctx, value, max, label) {
    ctx.clearRect(0, 0, 300, 150);
    ctx.beginPath();
    ctx.arc(150, 150, 100, Math.PI, 2 * Math.PI);
    ctx.strokeStyle = "white";
    ctx.lineWidth = 10;
    ctx.stroke();

    const angle = Math.PI + (value / max) * Math.PI;
    ctx.beginPath();
    ctx.moveTo(150, 150);
    ctx.lineTo(150 + 100 * Math.cos(angle), 150 + 100 * Math.sin(angle));
    ctx.strokeStyle = "red";
    ctx.lineWidth = 5;
    ctx.stroke();

    ctx.fillStyle = "white";
    ctx.font = "20px monospace";
    ctx.fillText(label + ": " + value, 80, 140);
}

function update() {
    fetch("/data")
        .then(response => response.json())
        .then(data => {
            drawGauge(rpmCtx, data.rpm, 10000, "RPM");
            drawGauge(speedCtx, data.speed, 340, "Speed");
        });
}

setInterval(update, 200);