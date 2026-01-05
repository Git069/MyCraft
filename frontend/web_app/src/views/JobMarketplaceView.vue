<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api';
import JobSearch from '@/components/JobSearch.vue';
import JobCard from '@/components/JobCard.vue';
import JobCardSkeleton from '@/components/JobCardSkeleton.vue';

const jobs = ref([]);
const loading = ref(true);
const error = ref(null);
const route = useRoute();

const fetchJobs = async () => {
  loading.value = true;
  error.value = null;
  try {
    const params = {
      status: 'OPEN',
      search: route.query.search,
      city: route.query.city,
      // WICHTIG: 'trade' muss hier auch ausgelesen werden, sonst filtert das Backend nicht!
      trade: route.query.trade
    };

    // Bereinigen von undefined Werten
    Object.keys(params).forEach(key => params[key] === undefined && delete params[key]);

    const response = await api.getJobs(params);
    // Sicherheitscheck wie auf der HomeView, falls leere Objekte kommen
    const results = response.data.results || [];
    jobs.value = results.filter(item => item && item.id);

  } catch (err) {
    console.error(err);
    error.value = "Fehler beim Laden der Aufträge.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchJobs);
// Reagiert auf Änderungen in der URL (z.B. neuer Filter)
watch(() => route.query, fetchJobs);
</script>

<template>
  <div class="container">
    <header class="market-header">
      <div class="compact-search-wrapper">
        <JobSearch />
      </div>
    </header>

    <div v-if="loading" class="jobs-grid">
      <JobCardSkeleton v-for="n in 8" :key="n" />
    </div>

    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!loading && !error && jobs.length === 0" class="empty-state">
      <h2>Keine Aufträge gefunden</h2>
      <p>Versuche es mit anderen Suchbegriffen.</p>
    </div>

    <div v-if="!loading && !error && jobs.length > 0" class="jobs-grid">
      <JobCard
        v-for="job in jobs"
        :key="job.id"
        :service="job"
      />
    </div>
  </div>
</template>

<style scoped>
/* Deine Styles bleiben unverändert */
.market-header { padding: var(--spacing-md) 0; margin-bottom: var(--spacing-xl); border-bottom: 1px solid var(--color-border); }
.compact-search-wrapper { max-width: 500px; margin: 0 auto; transform: scale(0.85); transform-origin: center; }
.jobs-grid { display: grid; gap: 24px; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); }
.empty-state { text-align: center; padding: var(--spacing-xxl) 0; }
.error-message { text-align: center; padding: var(--spacing-lg); color: var(--color-error); }
</style>