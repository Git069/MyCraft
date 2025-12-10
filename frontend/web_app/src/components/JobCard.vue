<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  job: {
    type: Object,
    required: true
  }
});

const router = useRouter();

const goToDetail = () => {
  router.push({ name: 'JobDetail', params: { id: props.job.id } });
};

// --- Helper for Images ---
const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=400&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=400&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=400&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=400&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=400&q=80'
};

const jobImage = computed(() => {
  // In the future, check for props.job.image_url
  return tradeImages[props.job.trade] || tradeImages.OTHER;
});

// --- Helper for Price ---
const formattedPrice = computed(() => {
  if (!props.job.price) return 'Preis auf Anfrage';
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(props.job.price);
});

// --- Helper for Date ---
const formattedDate = computed(() => {
  if (!props.job.execution_date) return 'Termin flexibel';
  const date = new Date(props.job.execution_date);
  return date.toLocaleDateString('de-DE', { day: 'numeric', month: 'short' });
});

// --- Helper for Title ---
// Format: [Category] in [City]
const displayTitle = computed(() => {
  // Map trade codes to readable names if needed, or use job title
  // For Airbnb style "Category in City":
  return `${props.job.title} in ${props.job.city}`;
});

</script>

<template>
  <div class="job-card" @click="goToDetail">
    <!-- A. Image Section -->
    <div class="image-container">
      <img :src="jobImage" :alt="job.title" class="job-image" />

      <!-- Favorite Icon (Top Right) -->
      <button class="favorite-btn" @click.stop>
        <svg viewBox="0 0 32 32" xmlns="http://www.w3.org/2000/svg" aria-hidden="true" role="presentation" focusable="false" style="display: block; fill: rgba(0, 0, 0, 0.5); height: 24px; width: 24px; stroke: white; stroke-width: 2; overflow: visible;"><path d="m16 28c7-4.733 14-10 14-17 0-1.792-.683-3.583-2.05-4.95-1.367-1.366-3.158-2.05-4.95-2.05-1.791 0-3.583.684-4.949 2.05l-2.051 2.051-2.05-2.051c-1.367-1.366-3.158-2.05-4.95-2.05-1.791 0-3.583.684-4.949 2.05-1.367 1.367-2.051 3.158-2.051 4.95 0 7 7 12.267 14 17z"></path></svg>
      </button>

      <!-- Badge (Optional, e.g. for new jobs) -->
      <!-- <div class="badge">Neu</div> -->
    </div>

    <!-- B. Info Section -->
    <div class="info-container">
      <div class="title-row">
        <span class="title">{{ displayTitle }}</span>
        <!-- Optional: Rating star here -->
      </div>

      <div class="details-row">
        <!-- Placeholder for distance logic -->
        <span>5 km entfernt</span> • <span>{{ formattedDate }}</span>
      </div>

      <div class="price-row">
        <span class="price">{{ formattedPrice }}</span>
        <span class="price-label">Budget</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.job-card {
  cursor: pointer;
  display: flex;
  flex-direction: column;
  gap: 12px;
  group: job-card; /* For hover effects */
}

/* --- IMAGE SECTION --- */
.image-container {
  position: relative;
  aspect-ratio: 1 / 1; /* Square aspect ratio like Airbnb often uses */
  border-radius: 16px; /* Strong rounding */
  overflow: hidden;
  background-color: #f0f0f0; /* Placeholder color */
}

.job-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

/* Hover Effect: Zoom */
.job-card:hover .job-image {
  transform: scale(1.05);
}

.favorite-btn {
  position: absolute;
  top: 12px;
  right: 12px;
  background: transparent;
  border: none;
  cursor: pointer;
  padding: 0;
  z-index: 2;
  transition: transform 0.1s;
}

.favorite-btn:active {
  transform: scale(0.9);
}

/* --- INFO SECTION --- */
.info-container {
  display: flex;
  flex-direction: column;
  gap: 2px;
}

.title-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
}

.title {
  font-weight: 600; /* Bold */
  color: var(--color-text);
  font-size: 1rem;
  line-height: 1.2;
  /* Truncate text if too long */
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.details-row {
  font-size: 0.9rem;
  color: var(--color-text-light); /* Grey */
  line-height: 1.2;
}

.price-row {
  margin-top: 6px; /* Spacing before price */
  display: flex;
  align-items: baseline;
  gap: 4px;
}

.price {
  font-weight: 600; /* Bold */
  color: var(--color-text);
  font-size: 1rem;
}

.price-label {
  font-size: 0.9rem;
  color: var(--color-text); /* Keep it dark for readability */
}
</style>
