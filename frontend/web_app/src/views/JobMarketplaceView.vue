<script setup>
import { ref, onMounted, watch } from 'vue';
import { useRoute } from 'vue-router';
import api from '@/api';
import JobSearch from '@/components/JobSearch.vue';

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
    };
    Object.keys(params).forEach(key => params[key] === undefined && delete params[key]);

    const response = await api.getJobs(params);
    jobs.value = response.data.results;
  } catch (err) {
    error.value = "Fehler beim Laden der Aufträge.";
    console.error(err);
  } finally {
    loading.value = false;
  }
};

onMounted(() => {
  fetchJobs();
});

watch(() => route.query, fetchJobs);

const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=400&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=400&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=400&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=400&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=400&q=80'
};
const formatPrice = (price) => {
  if (!price) return 'Auf Anfrage';
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div class="container">
    <header class="market-header">
      <div class="compact-search-wrapper">
        <JobSearch />
      </div>
    </header>

    <div v-if="loading" class="loading-state">Lade Angebote...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!loading && !error && jobs.length === 0" class="empty-state">
      <h2>Keine Aufträge gefunden</h2>
      <p>Versuche es mit anderen Suchbegriffen oder erweitere deinen Suchradius.</p>
    </div>

    <div v-if="!loading && !error && jobs.length > 0" class="jobs-grid">
      <router-link
        v-for="job in jobs"
        :key="job.id"
        :to="{ name: 'JobDetail', params: { id: job.id } }"
        class="job-card-link"
      >
        <article class="job-card">
          <div class="card-image">
            <img :src="tradeImages[job.trade] || tradeImages.OTHER" alt="Gewerk Bild" />
          </div>
          <div class="card-content">
            <h3 class="job-title">{{ job.title }}</h3>
            <p class="job-location">{{ job.zip_code }} {{ job.city }}</p>
            <div class="job-price-wrapper">
              <span class="job-price">{{ formatPrice(job.price) }}</span>
            </div>
          </div>
        </article>
      </router-link>
    </div>
  </div>
</template>

<style scoped>
.market-header {
  padding: var(--spacing-md) 0;
  margin-bottom: var(--spacing-xl);
  border-bottom: 1px solid var(--color-border);
}
.compact-search-wrapper {
  max-width: 500px;
  margin: 0 auto;
  transform: scale(0.85);
  transform-origin: center;
}

.job-card-link {
  text-decoration: none;
  color: inherit;
  display: block; /* Ensures the link takes up the full grid cell */
}

.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-xl);
}

.job-card {
  background: var(--color-surface);
  border-radius: var(--border-radius);
  overflow: hidden;
  transition: box-shadow var(--transition-speed);
  height: 100%;
}

.job-card-link:hover .job-card {
  box-shadow: var(--box-shadow);
}

.card-image {
  aspect-ratio: 4 / 3; /* Enforce a 4:3 aspect ratio for all images */
  width: 100%;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  border-radius: var(--border-radius); /* Apply border-radius to the image itself */
}

.card-content {
  padding: var(--spacing-sm) 0; /* Remove horizontal padding */
}

.job-title {
  font-size: 1rem; /* Slightly smaller for a cleaner look */
  font-weight: 600;
  margin: 0 0 var(--spacing-xs);
}

.job-location {
  font-size: var(--font-size-sm);
  color: var(--color-text-light);
  margin: 0 0 var(--spacing-md);
}

.job-price-wrapper {
  margin-top: auto; /* Push price to the bottom */
}

.job-price {
  font-weight: bold;
}

.empty-state {
  text-align: center;
  padding: var(--spacing-xxl) 0;
}
.empty-state h2 {
  margin-top: 0;
}
.error-message {
  text-align: center;
  padding: var(--spacing-lg);
  color: var(--color-error);
}
</style>
