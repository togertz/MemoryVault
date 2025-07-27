document.addEventListener("DOMContentLoaded", async function() {

    if (typeof latitude !== 'undefined' && typeof longitude !== 'undefined'){
        console.log("Loading map...")
        const map = L.map('map').setView([latitude, longitude], 16);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        L.marker([latitude, longitude]).addTo(map);

        map.zoomControl.remove();
        map.dragging.disable();
        map.touchZoom.disable();
        map.doubleClickZoom.disable();
        map.scrollWheelZoom.disable();
        map.keyboard.disable();

        if (map.tap) map.tab.disable();
    } else {
        console.log("removing map")
        const map = document.getElementById('map');
        map.remove();
    }
});