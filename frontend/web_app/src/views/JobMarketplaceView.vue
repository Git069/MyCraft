<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const jobs = ref([]);
const loading = ref(true);

const apiUrl = import.meta.env.VITE_API_URL;

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

const fetchJobs = async () => {
  try {
    const response = await axios.get(`${apiUrl}/jobs/`);
    jobs.value = response.data;
  } catch (error) {
    console.error("Fehler beim Laden:", error);
  } finally {
    loading.value = false;
  }
};

const availableJobs = computed(() => {
  return jobs.value.filter(job => job.status === 'OPEN');
});

onMounted(() => {
  fetchJobs();
});
</script>

<template>
  <!-- Use the global .container utility class -->
  <div class="container">

    <!-- Use the global .text-center utility class -->
    <header class="market-header text-center">
      <h1>Offene Aufträge finden</h1>
      <p>Wähle aus {{ availableJobs.length }} verfügbaren Handwerksaufträgen</p>
    </header>

    <div v-if="loading" class="loading-state">Lade Angebote...</div>

    <div v-else class="jobs-grid">
      <article v-for="job in availableJobs" :key="job.id" class="job-card">
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
            <!-- Use the global .base-button class -->
            <button class="base-button book-btn">Details ansehen</button>
          </div>
        </div>
      </article>
    </div>
  </div>
</template>

<style scoped>
/* --- HEADER --- */
.market-header {
  margin-bottom: var(--spacing-xxl); /* Use spacing token */
}
.market-header h1 {
  color: var(--color-text); /* Use color token */
}
.market-header p {
  color: var(--color-text-light); /* Use color token */
  font-size: var(--font-size-lg);
}

/* --- GRID SYSTEM --- */
.jobs-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: var(--spacing-lg); /* Use spacing token */
}

/* --- CARD DESIGN --- */
.job-card {
  background: var(--color-surface); /* Use color token */
  border-radius: var(--border-radius); /* Use border-radius token */
  overflow: hidden;
  box-shadow: var(--box-shadow); /* Use box-shadow token */
  transition: transform var(--transition-speed), box-shadow var(--transition-speed);
  display: flex;
  flex-direction: column;
}

.job-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 20px rgba(0,0,0,0.12); /* Keep a slightly stronger hover shadow */
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
  padding: var(--spacing-md); /* Use spacing token */
  display: flex;
  flex-direction: column;
  flex-grow: 1;
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: var(--spacing-sm); /* Use spacing token */
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

/* --- BUTTON OVERRIDE --- */
/* Extend the .base-button, but give it a specific background color */
.book-btn {
  width: 100%;
  background-color: var(--color-accent); /* Use accent color from tokens */
}
.book-btn:hover {
  background-color: #3e8e41; /* A darker version of the accent color */
}

/* --- RESPONSIVE --- */
@media (max-width: 600px) {
  .jobs-grid {
    grid-template-columns: 1fr;
  }
}
</style>
