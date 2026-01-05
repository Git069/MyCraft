<script setup>
import { computed } from 'vue';
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";
import L from 'leaflet';

// --- LEAFLET ICON FIX (bleibt gleich) ---
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
// ----------------------------------------

const props = defineProps({
  services: {
    type: Array,
    required: true
  }
});

// --- HELPER: Parse Location String OR Object ---
const getLatLng = (location) => {
  if (!location) return null;

  // Fall 1: GeoJSON Object { type: 'Point', coordinates: [lng, lat] }
  if (location.coordinates && Array.isArray(location.coordinates)) {
    return [location.coordinates[1], location.coordinates[0]];
  }

  // Fall 2: WKT String "SRID=4326;POINT (13.1405 52.5304)"
  if (typeof location === 'string' && location.includes('POINT')) {
    try {
      // Extrahiere den Teil in Klammern: "13.1405 52.5304"
      const coordsText = location.match(/\(([^)]+)\)/)[1];
      const [lng, lat] = coordsText.split(' ').map(parseFloat);

      if (!isNaN(lat) && !isNaN(lng)) {
        return [lat, lng]; // Leaflet will [Lat, Lng]
      }
    } catch (e) {
      console.warn("Konnte Location String nicht parsen:", location);
    }
  }

  return null;
};

const validServices = computed(() => {
  if (!props.services) return [];

  return props.services
    .map(service => {
      // Versuche Koordinaten zu ermitteln
      const latLng = getLatLng(service.location);
      return { ...service, latLng };
    })
    .filter(service => service.latLng !== null); // Nur die behalten, wo wir Koordinaten gefunden haben
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
  z-index: 1;
  border: 1px solid var(--color-border);
}
.popup-content {
  text-align: center;
  font-size: 0.9rem;
}
</style>