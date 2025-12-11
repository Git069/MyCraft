<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';
import { useToastStore } from '@/stores/toast';
import JobCard from '@/components/JobCard.vue';
import JobCardSkeleton from '@/components/JobCardSkeleton.vue'; // Import Skeleton

const authStore = useAuthStore();
const toastStore = useToastStore();
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
  } finally {
    loading.value = false;
  }
};

const handleDeleteJob = async (jobId) => {
  if (window.confirm("Möchtest du diesen Auftrag wirklich löschen?")) {
    try {
      await api.deleteJob(jobId);
      myJobs.value = myJobs.value.filter(job => job.id !== jobId);
      toastStore.addToast("Auftrag erfolgreich gelöscht.", "success");
    } catch (err) {
      toastStore.addToast("Fehler beim Löschen des Auftrags.", "error");
    }
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="container dashboard-container">
    <header class="dashboard-header">
      <h1>Mein Dashboard</h1>
    </header>

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

    <main class="tab-content">
      <!-- SKELETON LOADING STATE -->
      <div v-if="loading" class="jobs-grid">
        <JobCardSkeleton v-for="n in 4" :key="n" />
      </div>

      <div v-if="error" class="error-message">{{ error }}</div>

      <!-- ACTUAL DATA -->
      <template v-if="!loading">
        <div v-if="activeTab === 'my-jobs'">
          <div v-if="myJobs.length === 0" class="empty-state">
            <h2>Keine Angebote</h2>
            <p>Du hast noch keine Angebote erstellt.</p>
            <router-link :to="{ name: 'CreateJob' }" class="base-button primary-action">Erstes Angebot erstellen</router-link>
          </div>
          <div v-else class="jobs-grid">
            <JobCard
              v-for="job in myJobs"
              :key="job.id"
              :job="job"
              :show-controls="true"
              @delete="handleDeleteJob"
            />
          </div>
        </div>

        <div v-if="activeTab === 'my-bookings'">
          <div v-if="myBookings.length === 0" class="empty-state">
            <h2>Keine Buchungen</h2>
            <p>Du hast noch keine Aufträge gebucht.</p>
            <router-link :to="{ name: 'JobMarketplace' }" class="base-button primary-action">Aufträge finden</router-link>
          </div>
          <div v-else class="jobs-grid">
            <JobCard v-for="job in myBookings" :key="job.id" :job="job" />
          </div>
        </div>
      </template>
    </main>
  </div>
</template>

<style scoped>
/* Styles remain the same */
.dashboard-container {
  padding-top: 48px;
  padding-bottom: 64px;
}
.dashboard-header h1 {
  margin-top: 0;
  margin-bottom: 32px;
  font-size: 2rem;
  font-weight: 800;
}
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
}
.tab-button:hover {
  color: var(--color-text);
}
.tab-button.active {
  color: var(--color-text);
}
.tab-button.active::after {
  content: '';
  position: absolute;
  bottom: -1px;
  left: 0;
  width: 100%;
  height: 2px;
  background-color: var(--color-text);
}
.jobs-grid {
  display: grid;
  gap: 24px;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
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
