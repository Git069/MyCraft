<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import JobSearch from '@/components/JobSearch.vue';
import JobCard from '@/components/JobCard.vue';
import ServiceMap from '@/components/ServiceMap.vue';
import { useToastStore } from '@/stores/toast';

const recentServices = ref([]);
const loading = ref(true);
const isLocating = ref(false);
const toastStore = useToastStore();

const defaultParams = { page_size: 8 };

// Diese Funktion akzeptiert jetzt Filter-Parameter
const fetchServices = async (filterParams = {}) => {
  loading.value = true;
  const requestParams = { ...defaultParams, ...filterParams };

  try {
    const response = await api.getServices(requestParams);

    // FIX: Filtere alle Ergebnisse heraus, die null/undefined sind
    const results = response.data.results || [];
    recentServices.value = results.filter(item => item && item.id); // Nur Items mit ID behalten

  } catch (error) {
    console.error("Failed to fetch services:", error);
    toastStore.addToast("Fehler beim Laden der Angebote.", "error");
  } finally {
    loading.value = false;
  }
};

// Handler für das Event aus der JobSearch Komponente
const handleSearchTriggered = (filters) => {
  // filters ist z.B. { trade: 'PAINTER', search: '' } oder { search: 'Test', city: 'Berlin' }
  console.log("Filtering Home View with:", filters);
  fetchServices(filters);
};

const findNearby = () => {
  if (!navigator.geolocation) {
    toastStore.addToast("Geolokalisierung wird von deinem Browser nicht unterstützt.", "error");
    return;
  }

  isLocating.value = true;
  navigator.geolocation.getCurrentPosition(
    (position) => {
      const { latitude, longitude } = position.coords;
      fetchServices({
        lat: latitude,
        lng: longitude,
        radius: 20
      });
      isLocating.value = false;
    },
    (error) => {
      console.error("Geolocation error:", error);
      toastStore.addToast("Standort konnte nicht ermittelt werden.", "error");
      isLocating.value = false;
    }
  );
};

onMounted(() => fetchServices());
</script>

<template>
  <div class="home-view">
    <header class="hero-section text-center">
      <div class="container">
        <h1 class="hero-title">Finde die besten Handwerker. Oder die besten Aufträge.</h1>
        <p class="hero-subtitle">MyCraft verbindet talentierte Handwerker mit den passenden Projekten in deiner Nähe.</p>
        <JobSearch />
        <button @click="findNearby" class="nearby-btn" :disabled="isLocating">
          <span v-if="isLocating">Suche...</span>
          <span v-else>📍 Handwerker in meiner Nähe finden</span>
        </button>
      </div>
    </header>

    <section class="main-content-section">
      <div class="container">
        <h2 class="section-title">Aktuelle Angebote</h2>

        <ServiceMap v-if="!loading && recentServices.length > 0" :services="recentServices" />

        <div v-if="loading" class="loading-state">Lade Angebote...</div>
        <div v-else-if="recentServices.length === 0" class="empty-state">
          <p>Keine Angebote für deine Suche gefunden.</p>
        </div>
        <div v-else class="jobs-grid">
          <!-- FIX: Pass 'service' prop instead of 'job' -->
          <JobCard
            v-for="service in recentServices"
            :key="service.id"
            :service="service"
          />
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
.hero-section {
  padding: var(--spacing-xxl) 0;
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);

  /* NEU: Damit das Dropdown über den darunterliegenden Karten erscheint */
  position: relative;
  z-index: 100;
}
.hero-title { font-size: 3.5rem; line-height: 1.1; margin-top: 0; margin-bottom: var(--spacing-lg); max-width: 800px; margin-left: auto; margin-right: auto; }
.hero-subtitle { font-size: var(--font-size-lg); color: var(--color-text-light); margin-bottom: var(--spacing-xl); max-width: 650px; margin-left: auto; margin-right: auto; }
.nearby-btn {
  margin-top: 16px;
  background-color: transparent;
  border: 1px solid var(--color-border);
  color: var(--color-text);
  padding: 10px 20px;
  border-radius: 24px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.nearby-btn:hover {
  background-color: #f0f0f0;
  border-color: #ccc;
}
.main-content-section { padding: var(--spacing-xxl) 0; }
.section-title { font-size: 2rem; font-weight: 700; margin-top: 0; margin-bottom: var(--spacing-xl); text-align: left; }
.jobs-grid {
  display: grid;
  gap: 24px;
  /* Mobile First: Flexibles Layout für Handys und kleine Tablets.
     Hier nutzen wir auto-fill, damit es auf kleinen Screens automatisch umbricht. */
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}

@media (min-width: 1024px) {
  .jobs-grid {
    /* repeat(3, 1fr) bedeutet: Teile die Breite IMMER durch 3.
       Egal ob du 1, 2 oder 10 Ergebnisse hast.
       Eine einzelne Karte ist damit exakt so breit wie eine Karte in einer vollen Reihe. */
    grid-template-columns: repeat(3, 1fr);
  }
}
</style>
