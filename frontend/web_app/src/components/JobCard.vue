<script setup>
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import StarRating from './StarRating.vue';

const props = defineProps({
  job: { type: Object, required: true },
  showControls: { type: Boolean, default: false }
});

const emit = defineEmits(['delete', 'mark-completed', 'cancel', 'review']);
const router = useRouter();

const goToDetail = () => router.push({ name: 'ServiceDetail', params: { id: props.job.id } });
const goToEdit = () => router.push({ name: 'ServiceEdit', params: { id: props.job.id } }); // FIX: Use 'ServiceEdit'

const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=400&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=400&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=400&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=400&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=400&q=80'
};

const jobImage = computed(() => tradeImages[props.job.trade] || tradeImages.OTHER);
const formattedPrice = computed(() => new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(props.job.price || 0));
const formattedDate = computed(() => {
  if (!props.job.execution_date) return 'Termin flexibel';
  return new Date(props.job.execution_date).toLocaleDateString('de-DE', { day: 'numeric', month: 'short' });
});
const displayTitle = computed(() => `${props.job.title} in ${props.job.city}`);
</script>

<template>
  <div class="job-card">
    <div class="image-container" @click="goToDetail">
      <img :src="jobImage" :alt="job.title" class="job-image" />
      <div v-if="showControls" class="status-badge" :class="`status-${job.status.toLowerCase()}`">
        {{ job.status }}
      </div>
    </div>

    <div class="info-container" @click="goToDetail">
      <span class="title">{{ displayTitle }}</span>
      <span class="price">{{ formattedPrice }}</span>
    </div>

    <div v-if="showControls" class="card-footer-actions" @click.stop>
      <div v-if="job.status === 'OPEN'" class="action-group">
        <button class="action-btn edit" @click="goToEdit">Bearbeiten</button>
        <button class="action-btn cancel" @click="$emit('cancel', job.id)">Stornieren</button>
      </div>
      <div v-else-if="job.status === 'BOOKED'" class="action-group">
        <button class="action-btn complete" @click="$emit('mark-completed', job.id)">Auftrag abschließen</button>
      </div>
      <div v-else-if="job.status === 'COMPLETED'">
        <div v-if="!job.review" class="action-group">
          <button class="action-btn review" @click="$emit('review', job)">Handwerker bewerten</button>
        </div>
        <div v-else class="review-display">
          <StarRating :modelValue="job.review.rating" :readonly="true" />
        </div>
      </div>
      <div v-else class="action-group disabled">
        <span>{{ job.status === 'CANCELLED' ? 'Storniert' : 'Abgeschlossen' }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styles remain the same */
.job-card { cursor: pointer; display: flex; flex-direction: column; background-color: white; border-radius: 16px; overflow: hidden; border: 1px solid transparent; transition: box-shadow 0.2s; }
.job-card:has(.card-footer-actions) { border-color: var(--color-border); }
.job-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.image-container { position: relative; aspect-ratio: 1 / 1; border-radius: 16px; overflow: hidden; background-color: #f0f0f0; }
.job-image { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.job-card:hover .job-image { transform: scale(1.05); }
.status-badge { position: absolute; top: 12px; left: 12px; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; color: white; text-transform: uppercase; z-index: 2; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.status-open { background-color: var(--color-success); }
.status-booked { background-color: var(--color-primary); }
.status-completed { background-color: #717171; }
.status-cancelled { background-color: var(--color-error); }
.info-container { display: flex; flex-direction: column; gap: 2px; padding: 12px 4px; }
.title { font-weight: 600; color: var(--color-text); font-size: 1rem; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.price { font-weight: 400; }
.card-footer-actions { padding: 12px; border-top: 1px solid var(--color-border); background-color: #fcfcfc; }
.action-group { display: flex; gap: 8px; }
.action-btn { flex: 1; padding: 8px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: all 0.2s; }
.action-btn.edit { background-color: white; border-color: var(--color-border); color: var(--color-text); }
.action-btn.edit:hover { background-color: #f0f0f0; }
.action-btn.cancel { background-color: transparent; color: var(--color-error); border-color: transparent; }
.action-btn.cancel:hover { background-color: #fff0f0; }
.action-btn.complete { background-color: var(--color-success); color: white; width: 100%; }
.action-btn.complete:hover { background-color: #218838; }
.action-btn.review { width: 100%; background-color: var(--color-secondary); color: white; }
.review-display { padding: 8px; text-align: center; }
.action-group.disabled { justify-content: center; color: var(--color-text-light); font-size: 0.85rem; font-style: italic; }
</style>
