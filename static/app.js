function useMyLocation() {
    const status = document.getElementById("locationStatus");
    const lat = document.getElementById("lat");
    const lon = document.getElementById("lon");

    if (!navigator.geolocation) {
        status.textContent = "Geolocation is not supported by this browser.";
        return;
    }

    status.textContent = "Getting your location...";

    navigator.geolocation.getCurrentPosition(
        (position) => {
            lat.value = position.coords.latitude.toFixed(6);
            lon.value = position.coords.longitude.toFixed(6);
            status.textContent = "Location loaded. You can now search nearby providers.";
        },
        () => {
            status.textContent = "Location permission was not available. Demo coordinates remain active.";
        },
        {
            enableHighAccuracy: true,
            timeout: 8000,
            maximumAge: 60000
        }
    );
}
