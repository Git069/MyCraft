<script setup>
import { computed } from 'vue';
import { useRouter } from 'vue-router';

const props = defineProps({
  job: {
    type: Object,
    required: true
  },
  showControls: {
    type: Boolean,
    default: false
  }
});

const emit = defineEmits(['delete']);

const router = useRouter();

const goToDetail = () => {
  router.push({ name: 'JobDetail', params: { id: props.job.id } });
};

const goToEdit = () => {
  // We will create this route later
  // router.push({ name: 'JobEdit', params: { id: props.job.id } });
  alert('Edit-Funktion kommt bald!');
};

const handleDelete = () => {
  emit('delete', props.job.id);
};

const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=400&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=400&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=400&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=400&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=400&q=80'
};

const jobImage = computed(() => tradeImages[props.job.trade] || tradeImages.OTHER);
const formattedPrice = computed(() => {
  if (!props.job.price) return 'Preis auf Anfrage';
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(props.job.price);
});
const formattedDate = computed(() => {
  if (!props.job.execution_date) return 'Termin flexibel';
  return new Date(props.job.execution_date).toLocaleDateString('de-DE', { day: 'numeric', month: 'short' });
});
const displayTitle = computed(() => `${props.job.title} in ${props.job.city}`);

</script>

<template>
  <div class="job-card" @click="goToDetail">
    <div class="image-container">
      <img :src="jobImage" :alt="job.title" class="job-image" />

      <!-- Status Badge -->
      <div class="status-badge" :class="`status-${job.status.toLowerCase()}`">
        {{ job.status }}
      </div>

      <!-- Controls for Dashboard -->
      <div v-if="showControls" class="card-controls">
        <button class="icon-btn edit-btn" @click.stop="goToEdit">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15.232 5.232l3.536 3.536m-2.036-5.036a2.5 2.5 0 113.536 3.536L6.5 21.036H3v-3.536L16.732 3.732z"></path></svg>
        </button>
        <button class="icon-btn delete-btn" @click.stop="handleDelete">
          <svg fill="none" viewBox="0 0 24 24" stroke="currentColor"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"></path></svg>
        </button>
      </div>
    </div>

    <div class="info-container">
      <div class="title-row">
        <span class="title">{{ displayTitle }}</span>
      </div>
      <div class="details-row">
        <span>{{ formattedDate }}</span>
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
}

.image-container {
  position: relative;
  aspect-ratio: 1 / 1;
  border-radius: 16px;
  overflow: hidden;
  background-color: #f0f0f0;
}

.job-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.job-card:hover .job-image {
  transform: scale(1.05);
}

/* --- BADGE & CONTROLS --- */
.status-badge {
  position: absolute;
  top: 12px;
  left: 12px;
  padding: 4px 10px;
  border-radius: 20px;
  font-size: 0.75rem;
  font-weight: 700;
  color: white;
  text-transform: uppercase;
}
.status-open { background-color: var(--color-success); }
.status-booked { background-color: var(--color-text-light); }
.status-completed { background-color: var(--color-primary); }

.card-controls {
  position: absolute;
  top: 12px;
  right: 12px;
  display: flex;
  gap: 8px;
  background-color: rgba(255, 255, 255, 0.8);
  padding: 4px;
  border-radius: 20px;
}
.icon-btn {
  background: none;
  border: none;
  cursor: pointer;
  padding: 4px;
  color: var(--color-text);
  transition: color 0.2s;
}
.icon-btn svg {
  width: 20px;
  height: 20px;
}
.edit-btn:hover { color: var(--color-primary); }
.delete-btn:hover { color: var(--color-error); }


/* --- INFO SECTION --- */
.info-container { display: flex; flex-direction: column; gap: 2px; }
.title-row { display: flex; justify-content: space-between; align-items: flex-start; }
.title { font-weight: 600; color: var(--color-text); font-size: 1rem; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.details-row { font-size: 0.9rem; color: var(--color-text-light); line-height: 1.2; }
.price-row { margin-top: 6px; display: flex; align-items: baseline; gap: 4px; }
.price { font-weight: 600; color: var(--color-text); font-size: 1rem; }
.price-label { font-size: 0.9rem; color: var(--color-text); }
</style>
