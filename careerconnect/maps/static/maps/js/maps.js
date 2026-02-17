const map = L.map('map-box').setView([33.7502, -84.3885], 10);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'OpenStreetMap',
}).addTo(map);

const locations = JSON.parse(
  document.getElementById('locations-data').textContent
);

const distanceFilter = document.getElementById('distance-filter');
const jobList = document.getElementById('job-list');
const jobEmpty = document.getElementById('job-empty');
const geoStatus = document.getElementById('geo-status');
const useLocationButton = document.getElementById('use-location');

let userLatLng = null;
let userMarker = null;
let userCircle = null;
let jobMarkers = [];

const jobs = locations
  .map((loc) => ({
    id: loc.id,
    title: loc.title,
    location: loc.location,
    lat: parseFloat(loc.location_lat),
    lng: parseFloat(loc.location_long),
  }))
  .filter((job) => Number.isFinite(job.lat) && Number.isFinite(job.lng));

const toRadians = (value) => (value * Math.PI) / 180;

const haversineMiles = (lat1, lon1, lat2, lon2) => {
  const radius = 3958.8;
  const dLat = toRadians(lat2 - lat1);
  const dLon = toRadians(lon2 - lon1);
  const a =
    Math.sin(dLat / 2) ** 2 +
    Math.cos(toRadians(lat1)) *
      Math.cos(toRadians(lat2)) *
      Math.sin(dLon / 2) ** 2;
  const c = 2 * Math.atan2(Math.sqrt(a), Math.sqrt(1 - a));
  return radius * c;
};

const clearJobMarkers = () => {
  jobMarkers.forEach((marker) => map.removeLayer(marker));
  jobMarkers = [];
};

const createJobMarker = (job) => {
  const marker = L.marker([job.lat, job.lng])
    .addTo(map)
    .bindPopup(
      `<strong>${job.title}</strong><br>${job.location || 'Location unavailable'}`
    );
  jobMarkers.push(marker);
  return marker;
};

const renderJobs = (filteredJobs) => {
  jobList.innerHTML = '';
  if (filteredJobs.length === 0) {
    jobEmpty.style.display = 'block';
  } else {
    jobEmpty.style.display = 'none';
  }

  clearJobMarkers();

  filteredJobs.forEach((job) => {
    const listItem = document.createElement('li');
    listItem.className = 'map-job-card';
    listItem.innerHTML = `
      <div class="map-job-title">${job.title}</div>
      <div class="map-job-meta">${job.location || 'Location unavailable'}</div>
      <div class="map-job-distance">${job.distance.toFixed(1)} miles away</div>
    `;

    const marker = createJobMarker(job);
    listItem.addEventListener('click', () => {
      map.setView([job.lat, job.lng], 12, { animate: true });
      marker.openPopup();
    });

    jobList.appendChild(listItem);
  });
};

const applyFilter = () => {
  if (!userLatLng) {
    jobEmpty.textContent = 'Enable location to see nearby jobs.';
    jobEmpty.style.display = 'block';
    jobList.innerHTML = '';
    clearJobMarkers();
    return;
  }

  const filterValue = distanceFilter.value;
  const maxDistance =
    filterValue === 'any' ? Number.POSITIVE_INFINITY : parseFloat(filterValue);

  const filteredJobs = jobs
    .map((job) => ({
      ...job,
      distance: haversineMiles(userLatLng.lat, userLatLng.lng, job.lat, job.lng),
    }))
    .filter((job) => job.distance <= maxDistance)
    .sort((a, b) => a.distance - b.distance)
    .slice(0, 10);

  jobEmpty.textContent = 'No jobs found within the selected distance.';
  renderJobs(filteredJobs);
};

const updateUserLocation = (position) => {
  userLatLng = {
    lat: position.coords.latitude,
    lng: position.coords.longitude,
  };

  if (userMarker) {
    map.removeLayer(userMarker);
  }
  if (userCircle) {
    map.removeLayer(userCircle);
  }

  userMarker = L.marker([userLatLng.lat, userLatLng.lng], {
    icon: L.icon({
      iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
      iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
      shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
      iconSize: [25, 41],
      iconAnchor: [12, 41],
      popupAnchor: [1, -34],
      shadowSize: [41, 41],
    }),
  })
    .addTo(map)
    .bindPopup('You are here');

  userCircle = L.circle([userLatLng.lat, userLatLng.lng], {
    radius: 1600,
    color: '#00cfd5',
    fillColor: '#00cfd5',
    fillOpacity: 0.15,
  }).addTo(map);

  map.setView([userLatLng.lat, userLatLng.lng], 11);
  geoStatus.textContent =
    'Showing the 10 closest jobs within your chosen distance.';
  applyFilter();
};

const handleGeoError = () => {
  geoStatus.textContent =
    'Location access denied. Enable it to see nearby jobs.';
};

const requestUserLocation = () => {
  if (!navigator.geolocation) {
    geoStatus.textContent = 'Geolocation is not supported in this browser.';
    return;
  }

  geoStatus.textContent = 'Locating you...';
  navigator.geolocation.getCurrentPosition(updateUserLocation, handleGeoError, {
    enableHighAccuracy: true,
    timeout: 10000,
  });
};

distanceFilter.addEventListener('change', applyFilter);
useLocationButton.addEventListener('click', requestUserLocation);
requestUserLocation();
