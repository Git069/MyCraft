<script setup>
/**
 * ServiceMap.vue
 *
 * A map component using Leaflet to display service locations.
 * Parses location data (GeoJSON or WKT) and renders markers with popups.
 */

// --- Imports ---
import { computed } from 'vue';
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from 'leaflet';

// --- Leaflet Icon Fix ---
// Fixes missing marker icons in production builds by explicitly importing them.
import iconUrl from 'leaflet/dist/images/marker-icon.png';
import iconRetinaUrl from 'leaflet/dist/images/marker-icon-2x.png';
import shadowUrl from 'leaflet/dist/images/marker-shadow.png';

const customIcon = L.icon({
  iconUrl: iconUrl,
  iconRetinaUrl: iconRetinaUrl,
  shadowUrl: shadowUrl,
  iconSize: [25, 41],
  iconAnchor: [12, 41],
  popupAnchor: [1, -34],
  tooltipAnchor: [16, -28],
  shadowSize: [41, 41]
});

// --- Props ---

/**
 * Props definition.
 * @property {Array} services - List of service objects to display on the map.
 */
const props = defineProps({
  services: {
    type: Array,
    required: true
  }
});

// --- Methods ---

/**
 * Parses a location string or object into Leaflet-compatible coordinates [lat, lng].
 * Supports GeoJSON objects and WKT (Well-Known Text) strings.
 *
 * @param {Object|string} location - The location data.
 * @returns {Array<number>|null} Array [latitude, longitude] or null if invalid.
 */
const getLatLng = (location) => {
  if (!location) return null;

  // Case 1: GeoJSON Object { type: 'Point', coordinates: [lng, lat] }
  if (location.coordinates && Array.isArray(location.coordinates)) {
    return [location.coordinates[1], location.coordinates[0]];
  }

  // Case 2: WKT String "SRID=4326;POINT (13.1405 52.5304)"
  if (typeof location === 'string' && location.includes('POINT')) {
    try {
      // Extract the part inside parentheses: "13.1405 52.5304"
      const coordsText = location.match(/\(([^)]+)\)/)[1];
      const [lng, lat] = coordsText.split(' ').map(parseFloat);

      if (!isNaN(lat) && !isNaN(lng)) {
        return [lat, lng]; // Leaflet expects [Lat, Lng]
      }
    } catch (e) {
      console.warn("Could not parse location string:", location);
    }
  }

  return null;
};

// --- Computed Properties ---

/**
 * Filters and maps the services to include parsed coordinates.
 * Only services with valid coordinates are returned.
 */
const validServices = computed(() => {
  if (!props.services) return [];

  return props.services
    .map(service => {
      // Attempt to determine coordinates
      const latLng = getLatLng(service.location);
      return { ...service, latLng };
    })
    .filter(service => service.latLng !== null); // Keep only those where coordinates were found
});
</script>

<template>
  <div class="map-container">
    <l-map :zoom="6" :center="[51.1657, 10.4515]">
      <l-tile-layer
        url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"
        layer-type="base"
        name="OpenStreetMap"
      ></l-tile-layer>

      <l-marker
        v-for="service in validServices"
        :key="service.id"
        :lat-lng="service.latLng"
        :icon="customIcon"
      >
        <l-popup>
          <div class="popup-content">
            <strong>{{ service.title }}</strong><br>
            <router-link :to="{ name: 'ServiceDetail', params: { id: service.id } }">
              Details ansehen
            </router-link>
          </div>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<style scoped>
.map-container {
  height: 400px;
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 2rem;
  position: relative;
  z-index: 0;
  border: 1px solid var(--color-border);
}

.popup-content {
  text-align: center;
  font-size: 0.9rem;
}
</style>