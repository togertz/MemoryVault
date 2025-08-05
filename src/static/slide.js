document.addEventListener("DOMContentLoaded", async function() {

    // --------------- Code for loading and displaying the map ---------------
    if (typeof latitude !== 'undefined' && typeof longitude !== 'undefined'){
        // Load map
        const map = L.map('map').setView([latitude, longitude], 16);

        L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
            maxZoom: 19,
            attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
        }).addTo(map);

        // Set marker
        L.marker([latitude, longitude]).addTo(map);

        // Deactivate user interaction
        map.zoomControl.remove();
        map.dragging.disable();
        map.touchZoom.disable();
        map.doubleClickZoom.disable();
        map.scrollWheelZoom.disable();
        map.keyboard.disable();

        if (map.tap) map.tab.disable();

    } else {
        // If no coordinates are given: remove map element
        const map = document.getElementById('map');
        map.remove();
    }
});