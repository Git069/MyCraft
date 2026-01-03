<script setup>
import { LMap, LTileLayer, LMarker, LPopup } from "@vue-leaflet/vue-leaflet";
import "leaflet/dist/leaflet.css";

defineProps({
  services: {
    type: Array,
    required: true
  }
});

const getCoords = (service) => {
  if (service.location && service.location.coordinates) {
    // GeoJSON format is [longitude, latitude]
    // Leaflet expects [latitude, longitude]
    return [service.location.coordinates[1], service.location.coordinates[0]];
  }
  return null;
};
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
        v-for="service in services"
        :key="service.id"
        v-if="getCoords(service)" :lat-lng="getCoords(service)">

        <l-popup>
          <strong>{{ service.title }}</strong><br>
          <router-link :to="{ name: 'ServiceDetail', params: { id: service.id } }">
            Details ansehen
          </router-link>
        </l-popup>
      </l-marker>
    </l-map>
  </div>
</template>

<style scoped>
.map-container {
  height: 400px; /* Fixed height to prevent 0px issue */
  width: 100%;
  border-radius: 16px;
  overflow: hidden;
  margin-bottom: 2rem;
}
</style>
