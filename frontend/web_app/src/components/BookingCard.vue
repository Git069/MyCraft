<script setup>
/**
 * BookingCard.vue
 *
 * A card component representing a booking.
 * Displays booking details, status, and provides actions for contractors and customers.
 */

// --- Imports ---
import { computed, ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { STATUS_TRANSLATIONS } from '@/constants';

// --- Props & Emits ---

/**
 * Props definition.
 * @property {Object} booking - The booking object containing details.
 * @property {boolean} showControls - Whether to show action buttons (default: false).
 */
const props = defineProps({
  booking: { type: Object, required: true },
  showControls: { type: Boolean, default: false }
});

/**
 * Emits definition.
 * @emits review - Emitted when the user wants to review a completed booking.
 * @emits mark-completed - Emitted when the contractor marks the booking as completed.
 * @emits cancel - Emitted when the booking is cancelled.
 */
const emit = defineEmits(['review', 'mark-completed', 'cancel']);

// --- Reactive State ---

const router = useRouter();
const authStore = useAuthStore();

/** @type {import('vue').Ref<boolean>} State for menu visibility (currently unused but preserved) */
const isMenuOpen = ref(false);

// --- Computed Properties ---

/**
 * Checks if the logged-in user is the contractor for this booking.
 * @returns {boolean} True if the current user is the contractor.
 */
const isContractor = computed(() => {
  return authStore.user && authStore.user.id === props.booking.contractor;
});

/**
 * Determines if the booking can be cancelled.
 * Contractors can always cancel confirmed bookings.
 * Customers can cancel if the scheduled date is more than 7 days away.
 * @returns {boolean} True if cancellable.
 */
const isCancellable = computed(() => {
  if (props.booking.status !== 'CONFIRMED') return false;
  if (isContractor.value) return true; // Contractors can always cancel (or logic to be defined)

  // Customer logic: > 7 days in future
  if (!props.booking.scheduled_date) return false;
  const today = new Date();
  today.setHours(0, 0, 0, 0);
  const scheduledDate = new Date(props.booking.scheduled_date);
  const diffTime = scheduledDate - today;
  const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
  return diffDays >= 7;
});

/**
 * Mapping of trade types to image URLs.
 */
const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=400&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=400&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=400&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=400&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=400&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=400&q=80'
};

/**
 * Returns the image URL based on the trade type.
 */
const jobImage = computed(() => tradeImages[props.booking.service.trade] || tradeImages.OTHER);

/**
 * Formats the price as currency (EUR).
 */
const formattedPrice = computed(() => new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(props.booking.price || 0));

/**
 * Formats the creation date.
 */
const formattedDate = computed(() => {
  if (!props.booking.created_at) return 'Datum unbekannt';
  return new Date(props.booking.created_at).toLocaleDateString('de-DE', { day: 'numeric', month: 'short' });
});

/**
 * Returns the display title for the booking.
 */
const displayTitle = computed(() => props.booking.service.title);

/**
 * Translates the booking status code to a human-readable string.
 */
const translatedStatus = computed(() => {
  const status = props.booking.status;
  return STATUS_TRANSLATIONS[status] || status;
});

// --- Methods ---

/**
 * Navigates to the job detail page.
 */
const goToDetail = () => router.push({ name: 'JobDetail', params: { id: props.booking.service.id } });
</script>

<template>
  <div class="booking-card" @click="goToDetail">
    <div class="image-container">
      <img :src="jobImage" :alt="displayTitle" class="job-image" />

      <div class="status-badge" :class="`status-${booking.status.toLowerCase()}`">
        {{ translatedStatus }}
      </div>
    </div>

    <div class="info-container">
      <div class="title-row">
        <span class="title">{{ displayTitle }}</span>
      </div>
      <div class="details-row">
        <span>Gebucht am {{ formattedDate }}</span>
      </div>
      <div class="price-row">
        <span class="price">{{ formattedPrice }}</span>
        <span class="price-label">Preis</span>
      </div>
    </div>

    <div v-if="showControls" class="card-footer-actions" @click.stop>

      <div v-if="booking.status === 'CONFIRMED' && isContractor" class="action-group">
        <button class="action-btn complete" @click="$emit('mark-completed', booking.id)">Als erledigt markieren</button>
      </div>

      <div v-else-if="booking.status === 'CONFIRMED' && !isContractor" class="action-group">
        <button v-if="isCancellable" class="action-btn cancel" @click="$emit('cancel', booking.id)">Stornieren</button>
        <span v-else class="disabled-text">Wartet auf Ausführung</span>
      </div>

      <div v-else-if="booking.status === 'COMPLETED'">
        <div v-if="!booking.review && !isContractor" class="action-group">
          <button class="action-btn review" @click="$emit('review', booking)">Bewerten</button>
        </div>
        <div v-else class="review-display">
          <span>{{ isContractor ? 'Auftrag abgeschlossen' : 'Bewertung abgegeben' }}</span>
        </div>
      </div>

      <div v-else class="action-group disabled">
        <span>{{ booking.status === 'CANCELLED' ? 'Storniert' : 'In Bearbeitung' }}</span>
      </div>
    </div>
  </div>
</template>

<style scoped>
.booking-card { cursor: pointer; display: flex; flex-direction: column; background-color: white; border-radius: 16px; overflow: hidden; border: 1px solid transparent; transition: box-shadow 0.2s; }
.booking-card:has(.card-footer-actions) { border-color: var(--color-border); }
.booking-card:hover { box-shadow: 0 4px 12px rgba(0,0,0,0.08); }
.image-container { position: relative; aspect-ratio: 1 / 1; border-radius: 16px; overflow: hidden; background-color: #f0f0f0; }
.job-image { width: 100%; height: 100%; object-fit: cover; transition: transform 0.3s ease; }
.booking-card:hover .job-image { transform: scale(1.05); }
.status-badge { position: absolute; top: 12px; left: 12px; padding: 4px 10px; border-radius: 20px; font-size: 0.7rem; font-weight: 700; color: white; text-transform: uppercase; z-index: 2; box-shadow: 0 2px 4px rgba(0,0,0,0.2); }
.status-pending { background-color: var(--color-secondary); }
.status-confirmed { background-color: var(--color-primary); }
.status-completed { background-color: var(--color-success); }
.status-cancelled { background-color: var(--color-error); }
.info-container { display: flex; flex-direction: column; gap: 2px; padding: 12px 4px; }
.title { font-weight: 600; color: var(--color-text); font-size: 1rem; line-height: 1.2; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
.price { font-weight: 400; }
.card-footer-actions { padding: 12px; border-top: 1px solid var(--color-border); background-color: #fcfcfc; }
.action-group { display: flex; gap: 8px; width: 100%; justify-content: center; }
.action-btn { flex: 1; padding: 8px 12px; border-radius: 8px; font-size: 0.9rem; font-weight: 600; cursor: pointer; border: 1px solid transparent; transition: all 0.2s; }
.action-btn.complete { background-color: var(--color-success); color: white; width: 100%; }
.action-btn.complete:hover { background-color: #218838; }
.action-btn.review { width: 100%; background-color: var(--color-secondary); color: white; }
.action-btn.cancel { background-color: transparent; color: var(--color-error); border: 1px solid var(--color-error); }
.action-btn.cancel:hover { background-color: var(--color-error); color: white; }
.review-display { padding: 8px; text-align: center; color: var(--color-text-light); font-size: 0.9rem; }
.action-group.disabled { justify-content: center; color: var(--color-text-light); font-size: 0.85rem; font-style: italic; }
.disabled-text { color: var(--color-text-light); font-size: 0.85rem; font-style: italic; }
</style>