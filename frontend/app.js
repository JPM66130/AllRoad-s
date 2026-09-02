console.log("AllRoad’s frontend chargé.");

// Initialisation de la carte
const map = L.map('map').setView([42.670, 2.620], 13); // Ille-sur-Têt

// Fond de carte OpenStreetMap
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

// Bouton démarrer
document.getElementById("startNav").addEventListener("click", () => {
    getRoute();
});

// Bouton arrêter
document.getElementById("stopNav").addEventListener("click", () => {
    alert("Navigation arrêtée.");
});

async function getRoute() {
    try {
        const response = await fetch("https://allroads-api.onrender.com/route"); 
        const data = await response.json();

        console.log("Itinéraire reçu :", data);

        // Exemple : data = { coordinates: [[lat, lon], [lat, lon], ...] }

        const polyline = L.polyline(data.coordinates, { color: 'blue' }).addTo(map);
        map.fitBounds(polyline.getBounds());

    } catch (error) {
        console.error("Erreur API :", error);
        alert("Impossible de récupérer l’itinéraire.");
    }
}
