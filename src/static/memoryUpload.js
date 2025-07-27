document.addEventListener("DOMContentLoaded", async function () {
    const imageUpload = document.getElementById("imageUpload");
    const previewImg = document.getElementById("previewImg");
    const removeImageBtn = document.getElementById("removeImageBtn");

    const convert_to_base64 = file => new Promise((response) => {
        const fileReader = new FileReader();
        fileReader.readAsDataURL(file);
        fileReader.onload = () => response(fileReader.result);
    });

    imageUpload.addEventListener('change', async function () {
        const file = imageUpload.files;
        if (file && file[0]) {
            const img = await convert_to_base64(file[0]);
            previewImg.src = img;
            previewImg.style.display = 'block';
        } else {
            previewImg.src = '';
            previewImg.style.display = 'none';
        }
    });

    removeImageBtn.addEventListener('click', function () {
        imageUpload.value = '';
        previewImg.src = '';
        previewImg.style.display = 'none';
    });

    // MAP
    const map = L.map('map').setView([51.00399384674889, 10.296337678675117], 5);
    const latitude = document.getElementById("latitude");
    const longitude = document.getElementById("longitude");
    var marker;

    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
        attribution: '&copy; <a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
    }).addTo(map);


    const fillCoordinates = function(lat, lng) {
        latitude.value = lat;
        longitude.value = lng;
    }

    const setMarker = function(latlng) {
        if (marker) {
            marker.setLatLng(latlng);
        } else {
            marker = L.marker(latlng)
                .addTo(map);
        }

        marker.on('click', function(e) {
            if (marker){
                map.removeLayer(marker);
                marker=null;
                fillCoordinates('', '');
            }
        })
    };

    map.on('click', function (e) {
        setMarker(e.latlng);
        fillCoordinates(e.latlng.lat.toFixed(6), e.latlng.lng.toFixed(6));
    });

    const map_search = document.getElementById("map-search");
    map_search.addEventListener('keypress', function(e) {
        if (e.key === "Enter"){
            e.preventDefault();
            const query = e.target.value;
            fetch(`https://nominatim.openstreetmap.org/search?format=json&q=${encodeURIComponent(query)}`)
                .then(response => response.json())
                .then(data => {
                    if (data.length > 0) {
                        const place = data[0];
                        const latlng = [parseFloat(place.lat), parseFloat(place.lon)];
                        map.setView(latlng, 14);
                        setMarker(latlng);
                        fillCoordinates(latlng[0], latlng[1]);
                    } else {
                        alert("Location could not be found");
                    }
                })
        }
    });
});