const API_KEY = '006cf4f089f53d9b07142a382f93266f';
const CITY = 'Dhaka'; // Change to your city

document.addEventListener('DOMContentLoaded', function () {
    const tempElem = document.getElementById('weather-temp');
    const descElem = document.getElementById('weather-desc');

    if (!tempElem || !descElem) {
        // Elements not found, do nothing
        return;
    }

    fetch(`https://api.openweathermap.org/data/2.5/weather?q=${CITY}&units=metric&appid=${API_KEY}`)
        .then(res => res.json())
        .then(data => {
            if (data && data.main && data.main.temp) {
                tempElem.textContent = Math.round(data.main.temp) + '°C';
            } else {
                tempElem.textContent = '..°C';
            }

            if (data && data.weather && data.weather[0] && data.weather[0].description) {
                descElem.textContent = data.weather[0].description.charAt(0).toUpperCase() + data.weather[0].description.slice(1);
            } else {
                descElem.textContent = 'loading data';
            }
        })
        .catch(() => {
            tempElem.textContent = '..°C';
            descElem.textContent = '--';
        });
});
