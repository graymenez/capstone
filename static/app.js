mapboxgl.accessToken = 'pk.eyJ1IjoiZ3JleW1lbmV6IiwiYSI6ImNrdm0xaXkyNDNhcjUydXFpazZoN3dzejEifQ.3UPkaylDPQMh9yeUMxiLUw';
const map = new mapboxgl.Map({
    container: 'map', // container ID
    style: 'mapbox://styles/mapbox/streets-v11', // style URL
    center: [-96, 37.8], // starting position
    zoom: 3 // starting zoom
});









const geolocate = new mapboxgl.GeolocateControl({
    positionOptions: {
        enableHighAccuracy: true
    },
    // When active the map will receive updates to the device's location as it changes.
    trackUserLocation: true,
    // Draw an arrow next to the location dot to indicate which direction the device is heading.
    showUserHeading: true
});
map.addControl(geolocate);
map.on('load', () => {
    geolocate.trigger();
})

const geocoder = new MapboxGeocoder({
    // Initialize the geocoder
    accessToken: mapboxgl.accessToken, // Set the access token
    mapboxgl: mapboxgl, // Set the mapbox-gl instance
    marker: true // Do not use the default marker style
});

document.getElementById('geocoder').appendChild(geocoder.onAdd(map));

$('#fade').fadeOut(1000);