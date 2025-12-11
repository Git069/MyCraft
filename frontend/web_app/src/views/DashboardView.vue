<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';
import JobCard from '@/components/JobCard.vue';

const authStore = useAuthStore();
const isCraftsman = computed(() => authStore.isCraftsman);

const activeTab = ref(isCraftsman.value ? 'my-jobs' : 'my-bookings');
const myJobs = ref([]);
const myBookings = ref([]);
const loading = ref(true);
const error = ref(null);

const fetchData = async () => {
  loading.value = true;
  error.value = null;
  try {
    const [jobsResponse, bookingsResponse] = await Promise.all([
      isCraftsman.value ? api.getMyJobs() : Promise.resolve({ data: [] }),
      api.getMyBookings(),
    ]);
    myJobs.value = jobsResponse.data;
    myBookings.value = bookingsResponse.data;
  } catch (err) {
    error.value = "Fehler beim Laden deiner Aufträge.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="container dashboard-container">
    <header class="dashboard-header">
      <h1>Mein Dashboard</h1>
    </header>

    <!-- Airbnb-Style Tab Navigation -->
    <div class="tabs-wrapper">
      <nav class="tab-nav">
        <button
          v-if="isCraftsman"
          @click="activeTab = 'my-jobs'"
          class="tab-button"
          :class="{ 'active': activeTab === 'my-jobs' }"
        >
          Meine Angebote
        </button>
        <button
          @click="activeTab = 'my-bookings'"
          class="tab-button"
          :class="{ 'active': activeTab === 'my-bookings' }"
        >
          Meine Buchungen
        </button>
      </nav>
    </div>

    <!-- Content Area -->
    <main class="tab-content">
      <div v-if="loading" class="loading-state">Lade...</div>
      <div v-if="error" class="error-message">{{ error }}</div>

      <!-- My Jobs (for Craftsmen) -->
      <div v-if="!loading && activeTab === 'my-jobs'">
        <div v-if="myJobs.length === 0" class="empty-state">
          <h2>Keine Angebote</h2>
          <p>Du hast noch keine Angebote erstellt.</p>
          <router-link :to="{ name: 'CreateJob' }" class="base-button primary-action">Erstes Angebot erstellen</router-link>
        </div>
        <div v-else class="jobs-grid">
          <JobCard v-for="job in myJobs" :key="job.id" :job="job" />
        </div>
      </div>

      <!-- My Bookings (for Clients) -->
      <div v-if="!loading && activeTab === 'my-bookings'">
        <div v-if="myBookings.length === 0" class="empty-state">
          <h2>Keine Buchungen</h2>
          <p>Du hast noch keine Aufträge gebucht.</p>
          <router-link :to="{ name: 'JobMarketplace' }" class="base-button primary-action">Aufträge finden</router-link>
        </div>
        <div v-else class="jobs-grid">
          <JobCard v-for="job in myBookings" :key="job.id" :job="job" />
        </div>
      </div>
    </main>
  </div>
</template>

<style scoped>
.dashboard-container {
  padding-top: 48px; /* More top spacing */
  padding-bottom: 64px;
}

.dashboard-header h1 {
  margin-top: 0;
  margin-bottom: 32px;
  font-size: 2rem;
  font-weight: 800;
  color: var(--color-text);
}

/* --- TABS --- */
.tabs-wrapper {
  border-bottom: 1px solid var(--color-border);
  margin-bottom: 32px;
}

.tab-nav {
  display: flex;
  gap: 32px;
}

.tab-button {
  background: none;
  border: none;
  padding: 12px 0;
  font-size: 1rem;
  font-weight: 600;
  color: var(--color-text-light);
  cursor: pointer;
  position: relative;
  transition: color 0.2s;
}

.tab-button:hover {
  color: var(--color-text); /* Darker on hover */
  background-color: transparent; /* Ensure no background on hover */
}

.tab-button.active {
  color: var(--color-text); /* Black text for active */
}

/* The active underline */
.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px; /* Align with the wrapper border */
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-text); /* Black underline */
}

/* --- CONTENT --- */
.jobs-grid {
  display: grid;
  gap: 24px;
  /* Responsive Grid matching HomeView */
  grid-template-columns: repeat(1, 1fr);
}
@media (min-width: 768px) {
  .jobs-grid {
    grid-template-columns: repeat(2, 1fr);
  }
}
@media (min-width: 1024px) {
  .jobs-grid {
    grid-template-columns: repeat(4, 1fr);
  }
}

.empty-state {
  text-align: center;
  padding: 64px 0;
  background-color: #f8f9fa;
  border-radius: 12px;
}

.empty-state h2 {
  margin-top: 0;
  font-size: 1.5rem;
  margin-bottom: 8px;
}

.empty-state p {
  color: var(--color-text-light);
  margin-bottom: 24px;
}

.primary-action {
  padding: 12px 24px;
  font-size: 1rem;
}
</style>
