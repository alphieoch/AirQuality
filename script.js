
// Air Quality App JavaScript Logic
// This script handles the Google Maps integration, user location search,
// fetching data from the AirVisual API, and updating the UI based on the API response.

// Global Variables
let map;
let geocoder;
const AIRVISUAL_API_KEY = "c58f03e3-9d50-47b7-9306-08808afda89c";
const AIRVISUAL_API_ENDPOINT = "https://api.airvisual.com/v2/nearest_city";

// Initialize Google Maps
function initMap() {
    const center = { lat: 40.730610, lng: -73.935242 };  // Default to New York City
    map = new google.maps.Map(document.getElementById("map"), {
        zoom: 10,
        center: center
    });

    geocoder = new google.maps.Geocoder();

    // Add listener to search input
    document.getElementById("location-search").addEventListener("keypress", function(e) {
        if (e.key === "Enter") {
            geocodeAddress(geocoder, map);
        }
    });
}

// Geocode address and fetch air quality data
function geocodeAddress(geocoder, map) {
    let address = document.getElementById("location-search").value;
    geocoder.geocode({ "address": address }, function(results, status) {
        if (status === "OK") {
            map.setCenter(results[0].geometry.location);
            fetchAirQualityData(results[0].geometry.location.lat(), results[0].geometry.location.lng());
        } else {
            alert("Geocode was not successful for the following reason: " + status);
        }
    });
}

// Fetch air quality data using AirVisual API
function fetchAirQualityData(lat, lng) {
    let url = `${AIRVISUAL_API_ENDPOINT}?lat=${lat}&lon=${lng}&key=${AIRVISUAL_API_KEY}`;
    fetch(url)
    .then(response => response.json())
    .then(data => {
        if (data && data.status === "success") {
            updateUI(data.data);
        }
    })
    .catch(error => {
        console.error("Error fetching air quality data:", error);
    });
}

// Update UI with air quality data
function updateUI(data) {
    document.getElementById("aqi-value").textContent = data.current.pollution.aqius;
    document.getElementById("main-pollutant").textContent = data.current.pollution.mainus;

    let aqi = data.current.pollution.aqius;
    if (aqi <= 50) {
        document.getElementById("mask-rec").textContent = "No mask recommended.";
    } else if (aqi <= 100) {
        document.getElementById("mask-rec").textContent = "No mask recommended for the general public.";
    } else if (aqi <= 150) {
        document.getElementById("mask-rec").textContent = "Sensitive individuals should consider wearing a mask.";
    } else if (aqi <= 200) {
        document.getElementById("mask-rec").textContent = "Consider wearing a mask during outdoor activities.";
    } else if (aqi <= 300) {
        document.getElementById("mask-rec").textContent = "Wear a mask during outdoor activities.";
    } else {
        document.getElementById("mask-rec").textContent = "Stay indoors and use masks if needed.";
    }
}

