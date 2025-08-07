
async function fetchData() {
    const res = await fetch('/input');
    const data = await res.json();

    document.getElementById('gas').innerText = data.gas;
    document.getElementById('brake').innerText = data.brake;
    document.getElementById('steering').innerText = data.steering;

    const angle = (data.gas / 100) * 180 - 90;
    document.getElementById('speed-needle').style.transform = `rotate(${angle}deg)`;
}

setInterval(fetchData, 500);
