<script setup>
import { ref, onMounted, computed } from 'vue';
import axios from 'axios';

const jobs = ref([]);
const loading = ref(true);

// Mapping für Bilder basierend auf dem Gewerk (Trade)
// Hier nutzen wir kostenlose Platzhalter-Bilder von Unsplash
const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=400&q=80', // Klempner
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80', // Elektriker
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=400&q=80', // Maler
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=400&q=80', // Tischler
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=400&q=80', // Gärtner
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=400&q=80' // Sonstiges
};

// Hilfsfunktion für schöne Preisformatierung
const formatPrice = (price) => {
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
};

// API Call
const fetchJobs = async () => {
  try {
    const response = await axios.get('http://127.0.0.1:8000/api/jobs/');
    jobs.value = response.data;
  } catch (error) {
    console.error("Fehler beim Laden:", error);
  } finally {
    loading.value = false;
  }
};

// Computed Property: Filtere nur "OFFENE" Jobs
// (Damit keine erledigten Aufträge angezeigt werden)
const availableJobs = computed(() => {
  return jobs.value.filter(job => job.status === 'OPEN');
});

onMounted(() => {
  fetchJobs();
});
</script>

<template>
  <div class="marketplace-container">

    <header class="market-header">
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
            <button class="book-btn">Details ansehen</button>
          </div>
        </div>

      </article>

    </div>
  </div>
</template>

<style scoped>
.marketplace-container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  font-family: 'Segoe UI', sans-serif;
}

.market-header {
  text-align: center;
  margin-bottom: 3rem;
}
.market-header h1 { font-size: 2.5rem; color: #222; margin-bottom: 0.5rem; }
.market-header p { color: #717171; }

/* --- GRID SYSTEM --- */
.jobs-grid {
  display: grid;
  /* Das ist der responsive Zauber: Spalten füllen sich automatisch */
  grid-template-columns: repeat(auto-fill, minmax(280px, 1fr));
  gap: 24px;
}

/* --- CARD DESIGN --- */
.job-card {
  background: white;
  border-radius: 12px;
  overflow: hidden; /* Damit das Bild an den Ecken abgerundet wird */
  box-shadow: 0 4px 12px rgba(0,0,0,0.08);
  transition: transform 0.2s ease, box-shadow 0.2s ease;
  display: flex;
  flex-direction: column;
}

.job-card:hover {
  transform: translateY(-4px); /* Leichtes Anheben beim Hover */
  box-shadow: 0 12px 20px rgba(0,0,0,0.12);
}

.card-image {
  height: 200px;
  position: relative;
}

.card-image img {
  width: 100%;
  height: 100%;
  object-fit: cover; /* Bild füllt den Bereich ohne Verzerrung */
}

.category-badge {
  position: absolute;
  top: 10px;
  left: 10px;
  background: rgba(255, 255, 255, 0.9);
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: bold;
  color: #333;
}

.card-content {
  padding: 1rem;
  display: flex;
  flex-direction: column;
  flex-grow: 1; /* Füllt den restlichen Platz */
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: start;
  margin-bottom: 0.5rem;
}

.job-title {
  margin: 0;
  font-size: 1.1rem;
  color: #222;
  font-weight: 600;
  line-height: 1.4;
}

.job-price {
  font-weight: bold;
  color: #222;
  white-space: nowrap;
}

.job-location {
  color: #717171;
  font-size: 0.9rem;
  margin: 0 0 0.5rem 0;
}

.job-desc {
  color: #717171;
  font-size: 0.9rem;
  line-height: 1.5;
  margin-bottom: 1.5rem;
}

.card-footer {
  margin-top: auto; /* Drückt den Button immer ganz nach unten */
}

.book-btn {
  width: 100%;
  padding: 10px;
  background-color: #ff385c; /* Airbnb-Rot (ähnlich) */
  color: white;
  border: none;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
}
.book-btn:hover { background-color: #d90b3e; }

/* Mobile Anpassung */
@media (max-width: 600px) {
  .jobs-grid {
    grid-template-columns: 1fr; /* Auf Handy nur eine Spalte */
  }
}
</style>