<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api'; // Import the centralized API service

const jobs = ref([]);
const loading = ref(true);
const error = ref(null);

// --- API Call ---
const fetchJobs = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Fetch only open jobs from the backend
    const response = await api.getJobs({ status: 'OPEN' });
    // The backend now returns a paginated response
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

// Helper functions and tradeImages remain the same...
const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=400&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=400&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=400&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=400&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=400&q=80'
};
const formatPrice = (price) => {
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div class="container">
    <header class="market-header text-center">
      <h1>Offene Aufträge finden</h1>
      <p v-if="!loading">Wähle aus {{ jobs.length }} verfügbaren Handwerksaufträgen</p>
    </header>

    <div v-if="loading" class="loading-state">Lade Angebote...</div>
    <div v-if="error" class="error-message">{{ error }}</div>

    <div v-if="!loading && !error" class="jobs-grid">
      <article v-for="job in jobs" :key="job.id" class="job-card">
        <div class="card-image">
          <img :src="tradeImages[job.trade] || tradeImages.OTHER" alt="Gewerk Bild" />
          <span class="category-badge">{{ job.trade }}</span>
        </div>
        <div class="card-content">
          <div class="card-header">
            <h3 class="job-title">{{ job.title }}</h3>
            <span class="job-price">{{ formatPrice(job.price) }}</span>
          </div>
          <p class="job-location">📍 {{ job.zip_code }} {{ job.city }}</p>
          <p class="job-desc">{{ job.description.substring(0, 80) }}...</p>
          <div class="card-footer">
            <button class="base-button book-btn">Details ansehen</button>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
/* Styles remain the same */
.market-header {
  margin-bottom: var(--spacing-xxl);
}
.market-header h1 {
  color: var(--color-text);
}
.market-header p {
  color: var(--color-text-light);
  font-size: var(--font-size-lg);
}
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-lg);
}
.job-card {
  background: var(--color-surface);
  border-radius: var(--border-radius);
  overflow: hidden;
  box-shadow: var(--box-shadow);
  transition: transform var(--transition-speed), box-shadow var(--transition-speed);
  display: flex;
  flex-direction: column;
}
.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px rgba(0,0,0,0.12);
}
.card-image {
  height: 200px;
  position: relative;
}
.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.category-badge {
  position: absolute;
  top: var(--spacing-sm);
  left: var(--spacing-sm);
  background: rgba(255, 255, 255, 0.9);
  padding: var(--spacing-xs) var(--spacing-sm);
  border-radius: 20px;
  font-size: var(--font-size-sm);
  font-weight: bold;
  color: var(--color-text);
}
.card-content {
  padding: var(--spacing-md);
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}
.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: var(--spacing-sm);
}
.job-title {
  margin: 0;
  font-size: var(--font-size-lg);
  color: var(--color-text);
  font-weight: 600;
  line-height: 1.4;
}
.job-price {
  font-weight: bold;
  color: var(--color-text);
  white-space: nowrap;
}
.job-location {
  color: var(--color-text-light);
  font-size: var(--font-size-sm);
  margin: 0 0 var(--spacing-sm) 0;
}
.job-desc {
  color: var(--color-text-light);
  font-size: var(--font-size-base);
  line-height: 1.5;
  margin-bottom: var(--spacing-lg);
}
.card-footer {
  margin-top: auto;
}
.book-btn {
  width: 100%;
  background-color: var(--color-accent);
}
.book-btn:hover {
  background-color: #3e8e41;
}
.error-message {
  background-color: var(--color-error);
  color: var(--color-text-inverted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  text-align: center;
}
</style>
