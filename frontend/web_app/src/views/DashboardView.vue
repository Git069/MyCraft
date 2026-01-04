<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import JobCard from '@/components/JobCard.vue';
import JobCardSkeleton from '@/components/JobCardSkeleton.vue';
import { useToastStore } from '@/stores/toast'; // Falls du Toast nutzt

const myServices = ref([]); // Hier kommen die Jobs rein
const loading = ref(true);
const activeTab = ref('my-services'); // Oder wie auch immer deine Tabs heißen

const fetchMyServices = async () => {
  loading.value = true;
  try {
    const response = await api.getMyServices();

    // WICHTIG: api.js transformiert GeoJSON und packt die Liste in 'results'
    // Wenn hier nur 'response.data' steht, ist das der Fehler!
    myServices.value = response.data.results || [];

    console.log("Geladene Services:", myServices.value); // Debugging
  } catch (error) {
    console.error("Fehler beim Laden der Services:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchMyServices();
});
</script>

<template>
  <div class="container-fluid dashboard-container">
    <!-- ... (header and tabs remain the same) ... -->
    <main class="tab-content">
      <div v-if="loading" class="dashboard-grid">
        <JobCardSkeleton v-for="n in 4" :key="n" />
      </div>
      <template v-else>
        <div v-if="activeTab === 'my-services'">
          <div v-if="myServices.length === 0" class="empty-state">
            <!-- ... -->
          </div>
          <div v-else class="dashboard-grid">
            <!-- FIX: Pass 'service' prop instead of 'job' -->
            <JobCard
              v-for="service in myServices"
              :key="service.id"
              :service="service"
              :show-controls="true"
            />
          </div>
        </div>
        <!-- ... (other tabs remain the same) ... -->
      </template>
    </main>
    <!-- ... (modal remains the same) ... -->
  </div>
</template>

<style scoped>
.dashboard-grid {
  display: grid;
  /* Das ist der Zaubertrick für Responsive Design:
     Erstelle so viele Spalten wie möglich (auto-fill),
     aber jede Spalte muss mindestens 280px breit sein (minmax).
     Den Rest (1fr) verteilt er gleichmäßig.
  */
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px; /* Abstand zwischen den Karten */
  margin-top: 20px;
  width: 100%;
}

/* Optional: Damit es auf sehr kleinen Handys nicht am Rand klebt */
@media (max-width: 600px) {
  .dashboard-grid {
    grid-template-columns: 1fr; /* Auf Handys volle Breite, aber mit Abstand */
    gap: 16px;
  }
}
</style>
