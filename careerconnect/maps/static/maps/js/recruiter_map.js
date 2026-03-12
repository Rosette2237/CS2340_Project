const map = L.map('map-box').setView([39.5, -98.35], 4);

L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19,
  attribution: 'OpenStreetMap',
}).addTo(map);

const jobLocations = JSON.parse(
  document.getElementById('job-locations-data').textContent
);
const applicantLocations = JSON.parse(
  document.getElementById('applicant-locations-data').textContent
);

// ── Default Leaflet icon (same as applicant map) ───────────────
const defaultIcon = L.icon({
  iconUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon.png',
  iconRetinaUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-icon-2x.png',
  shadowUrl: 'https://unpkg.com/leaflet@1.9.4/dist/images/marker-shadow.png',
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  shadowSize: [41, 41],
});

// ── Orange SVG pin (same shape, different color) ───────────────
function makeColoredIcon(color) {
  const svg = `
    <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 25 41" width="25" height="41">
      <path d="M12.5 0C5.596 0 0 5.596 0 12.5
               C0 22 12.5 41 12.5 41
               S25 22 25 12.5
               C25 5.596 19.404 0 12.5 0z"
            fill="${color}" stroke="white" stroke-width="1.5"/>
      <circle cx="12.5" cy="12.5" r="5" fill="white" opacity="0.85"/>
    </svg>`;
  return L.divIcon({
    className: '',
    html: svg,
    iconSize: [25, 41],
    iconAnchor: [12, 41],
    popupAnchor: [1, -34],
  });
}

const applicantIcon = makeColoredIcon('#ff9800');

const jobMarkers = {};

// ── Job office markers (default blue Leaflet pin) ──────────────
jobLocations.forEach((job) => {
  const marker = L.marker([job.lat, job.lng], { icon: defaultIcon }).addTo(map);

  marker.bindPopup(
    `<div style="font-family:sans-serif; min-width:160px;">
      <strong style="font-size:0.95rem;">${job.title}</strong><br>
      <span style="color:#555; font-size:0.85rem;">${job.location}</span><br>
      <a href="/jobs/${job.id}/edit/"
         style="color:#ff9800; font-size:0.85rem; margin-top:6px; display:inline-block;">
        ✏ Edit office location
      </a>
    </div>`
  );

  jobMarkers[job.id] = marker;
});

// ── Applicant markers (orange pin, same shape) ─────────────────
applicantLocations.forEach((applicant) => {
  L.marker([applicant.lat, applicant.lng], { icon: applicantIcon })
    .addTo(map)
    .bindPopup(
      `<div style="font-family:sans-serif;">
        <span style="font-size:0.85rem;">Applicant for:</span><br>
        <strong style="font-size:0.9rem;">${applicant.job_title}</strong>
      </div>`
    );
});

// ── Sidebar: click job card to pan to its office marker ────────
document.querySelectorAll('.map-job-card').forEach((card) => {
  card.addEventListener('click', () => {
    const jobId = parseInt(card.id.replace('job-item-', ''));
    const marker = jobMarkers[jobId];
    if (marker) {
      map.setView(marker.getLatLng(), 13, { animate: true });
      marker.openPopup();
    }
  });
});

// ── Fit map to all visible markers ────────────────────────────
const allPoints = [
  ...jobLocations.map((j) => [j.lat, j.lng]),
  ...applicantLocations.map((a) => [a.lat, a.lng]),
];
if (allPoints.length > 0) {
  map.fitBounds(allPoints, { padding: [60, 60] });
}
