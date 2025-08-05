function createRaindrop(){
    const raindrop = document.createElement("div");
    raindrop.classList.add("raindrop");
    raindrop.style.left = Math.random() * window.innerWidth + "px";

    const duration = Math.random() * 2 + .5; // Random duration between 0.5 and 2.5 seconds
    raindrop.style.animationDuration = duration + "s";

    document.body.appendChild(raindrop);

    setTimeout(() => {
        raindrop.remove();
    }, duration * 1000);
}

setInterval(createRaindrop, randomInterval()); // Create a raindrop every 200 milliseconds

function randomInterval() {
    return Math.random() * 100 + 20; // Random interval between 20ms and 120ms
}