<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';
import { useToastStore } from '@/stores/toast';
import JobCard from '@/components/JobCard.vue';
import JobCardSkeleton from '@/components/JobCardSkeleton.vue';
import ReviewModal from '@/components/ReviewModal.vue';

const authStore = useAuthStore();
const toastStore = useToastStore();
const isCraftsman = computed(() => authStore.isCraftsman);

const activeTab = ref(isCraftsman.value ? 'my-jobs' : 'my-bookings');
const myJobs = ref([]);
const myBookings = ref([]);
const loading = ref(true);

const showReviewModal = ref(false);
const selectedJobForReview = ref(null);

const fetchData = async () => {
  loading.value = true;
  try {
    const [jobsResponse, bookingsResponse] = await Promise.all([
      isCraftsman.value ? api.getMyJobs() : Promise.resolve({ data: [] }),
      api.getMyBookings(),
    ]);
    myJobs.value = jobsResponse.data;
    myBookings.value = bookingsResponse.data;
  } catch (err) {
    toastStore.addToast("Fehler beim Laden deiner Aufträge.", "error");
  } finally {
    loading.value = false;
  }
};

const updateJobInList = (jobId, list, updatedData) => {
  const jobIndex = list.value.findIndex(j => j.id === jobId);
  if (jobIndex !== -1) {
    list.value[jobIndex] = { ...list.value[jobIndex], ...updatedData };
  }
};

const handleMarkCompleted = async (jobId) => {
  try {
    const response = await api.markJobAsCompleted(jobId);
    updateJobInList(jobId, myJobs, { status: response.data.status });
    toastStore.addToast("Auftrag als erledigt markiert.", "success");
  } catch (err) { toastStore.addToast("Aktion fehlgeschlagen.", "error"); }
};

const handleCancelJob = async (jobId) => {
  if (window.confirm("Möchtest du diesen Auftrag wirklich stornieren?")) {
    try {
      const response = await api.cancelJob(jobId);
      updateJobInList(jobId, myJobs, { status: response.data.status });
      toastStore.addToast("Auftrag storniert.", "info");
    } catch (err) { toastStore.addToast("Aktion fehlgeschlagen.", "error"); }
  }
};

const openReviewModal = (job) => {
  selectedJobForReview.value = job;
  showReviewModal.value = true;
};

const handleCreateReview = async (reviewPayload) => {
  try {
    const response = await api.createReview(reviewPayload);
    updateJobInList(reviewPayload.job, myBookings, { review: response.data });
    toastStore.addToast("Bewertung erfolgreich abgegeben.", "success");
    showReviewModal.value = false;
  } catch (err) {
    toastStore.addToast(err.response?.data?.detail || "Fehler beim Senden der Bewertung.", "error");
  }
};

onMounted(fetchData);
</script>

<template>
  <div class="container-fluid dashboard-container">
    <header class="dashboard-header">
      <h1>Mein Dashboard</h1>
    </header>

    <div class="tabs-wrapper">
      <nav class="tab-nav">
        <button v-if="isCraftsman" @click="activeTab = 'my-jobs'" class="tab-button" :class="{ 'active': activeTab === 'my-jobs' }">
          Meine Angebote
        </button>
        <button @click="activeTab = 'my-bookings'" class="tab-button" :class="{ 'active': activeTab === 'my-bookings' }">
          Meine Buchungen
        </button>
      </nav>
    </div>

    <main class="tab-content">
      <div v-if="loading" class="jobs-grid">
        <JobCardSkeleton v-for="n in 4" :key="n" />
      </div>

      <template v-else>
        <div v-if="activeTab === 'my-jobs'">
          <div v-if="myJobs.length === 0" class="empty-state">
            <h2>Keine Angebote</h2>
            <router-link :to="{ name: 'CreateJob' }" class="base-button primary-action">Erstes Angebot erstellen</router-link>
          </div>
          <div v-else class="jobs-grid">
            <JobCard
              v-for="job in myJobs"
              :key="job.id"
              :job="job"
              :show-controls="true"
              @cancel="handleCancelJob"
              @mark-completed="handleMarkCompleted"
            />
          </div>
        </div>

        <div v-if="activeTab === 'my-bookings'">
          <div v-if="myBookings.length === 0" class="empty-state">
            <h2>Keine Buchungen</h2>
            <router-link :to="{ name: 'JobMarketplace' }" class="base-button primary-action">Aufträge finden</router-link>
          </div>
          <div v-else class="jobs-grid">
            <JobCard
              v-for="job in myBookings"
              :key="job.id"
              :job="job"
              :show-controls="true"
              @review="openReviewModal"
            />
          </div>
        </div>
      </template>
    </main>

    <ReviewModal
      v-if="selectedJobForReview"
      :is-open="showReviewModal"
      :job="selectedJobForReview"
      @close="showReviewModal = false"
      @submit="handleCreateReview"
    />
  </div>
</template>

<style scoped>
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
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
}
.empty-state {
  text-align: center;
  padding: 64px 0;
  background-color: #f8f9fa;
  border-radius: 12px;
}
</style>
