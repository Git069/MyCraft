<script setup>
import { ref, onMounted, computed } from 'vue';
import { useToastStore } from '@/stores/toast';
import BookingCard from '@/components/BookingCard.vue';
import ReviewModal from '@/components/ReviewModal.vue';
import api from '@/api';

/* ==========================================================================
   State & Setup
   ========================================================================== */

const toast = useToastStore();

const bookings = ref([]);
const loading = ref(true);
const error = ref(null);

// Review State
const showReviewModal = ref(false);
const reviewTarget = ref(null);

/* ==========================================================================
   Computed Properties
   ========================================================================== */

/**
 * Filters bookings to show only active ones.
 * Active bookings are those that are not cancelled and not completed with a review.
 * @returns {Array} List of active bookings.
 */
const activeBookings = computed(() => bookings.value.filter((b) => {
  if (b.status === 'CANCELLED') return false;
  if (b.status === 'COMPLETED' && b.review) return false;
  return true;
}));

/**
 * Filters bookings to show only past ones.
 * Past bookings are those that are cancelled or completed with a review.
 * @returns {Array} List of past bookings.
 */
const pastBookings = computed(() => bookings.value.filter((b) => b.status === 'CANCELLED' || (b.status === 'COMPLETED' && b.review)));

/* ==========================================================================
   Lifecycle Hooks
   ========================================================================== */

/**
 * Fetches bookings when the component is mounted.
 */
onMounted(fetchBookings);

/* ==========================================================================
   Methods
   ========================================================================== */

/**
 * Fetches the user's bookings from the API.
 * Updates the bookings state with the results.
 */
async function fetchBookings() {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.getMyBookings();
    bookings.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = 'Deine Buchungen konnten nicht geladen werden.';
  } finally {
    loading.value = false;
  }
}

/**
 * Cancels a booking after user confirmation.
 * @param {number} bookingId - The ID of the booking to cancel.
 */
const handleCancel = async (bookingId) => {
  if (!confirm('Möchtest du diese Buchung wirklich stornieren?')) return;

  try {
    await api.cancelBooking(bookingId);
    toast.addToast('Buchung erfolgreich storniert', 'success');
    await fetchBookings();
  } catch (err) {
    toast.addToast('Fehler beim Stornieren der Buchung', 'error');
  }
};

/**
 * Opens the review modal for a specific booking.
 * @param {Object} booking - The booking object to review.
 */
const openReviewModal = (booking) => {
  reviewTarget.value = {
    id: booking.id,
    title: booking.service.title,
  };
  showReviewModal.value = true;
};

/**
 * Submits a review for a booking.
 * @param {Object} payload - The review data containing job ID, rating, and comment.
 */
const handleReviewSubmit = async (payload) => {
  try {
    await api.createReview({
      booking: payload.job,
      rating: payload.rating,
      comment: payload.comment,
    });

    toast.addToast('Bewertung erfolgreich gesendet!', 'success');
    showReviewModal.value = false;
    await fetchBookings();
  } catch (err) {
    const msg = err.response?.data?.detail || 'Fehler beim Senden der Bewertung.';
    toast.addToast(msg, 'error');
  }
};
</script>

<template>
  <div class="container page-wrapper">
    <header class="page-header">
      <h1>Meine Buchungen</h1>
      <p class="subtitle">Hier findest du alle Dienstleistungen, die du angefragt hast.</p>
    </header>

    <div v-if="loading" class="loading-state">
      Lade deine Buchungen...
    </div>

    <div v-else-if="error" class="error-state">
      {{ error }}
      <button @click="fetchBookings" class="base-button secondary-action">Erneut versuchen</button>
    </div>

    <div v-else-if="bookings.length === 0" class="empty-state">
      <div class="empty-icon">📅</div>
      <h3>Noch keine Buchungen</h3>
      <p>Du hast noch keine Handwerker beauftragt.</p>
      <router-link :to="{ name: 'JobMarketplace' }" class="base-button primary-action">
        Jetzt Handwerker finden
      </router-link>
    </div>

    <div v-else class="content-wrapper">

      <section v-if="activeBookings.length > 0" class="section-group">
        <h2 class="section-title">Aktuelle Aufträge</h2>
        <div class="bookings-grid">
          <BookingCard
            v-for="booking in activeBookings"
            :key="booking.id"
            :booking="booking"
            :show-controls="true"
            @cancel="handleCancel"
            @review="openReviewModal"
            @update="fetchBookings"
          />
        </div>
      </section>

      <div v-else-if="pastBookings.length > 0" class="info-message">
        <p>Aktuell keine offenen Aufträge.</p>
      </div>

      <section v-if="pastBookings.length > 0" class="section-group past-section">
        <h2 class="section-title">Vergangene Aufträge</h2>
        <div class="bookings-grid faded-grid">
          <BookingCard
            v-for="booking in pastBookings"
            :key="booking.id"
            :booking="booking"
            :show-controls="true"
            @cancel="handleCancel"
            @review="openReviewModal"
          />
        </div>
      </section>

    </div>

    <ReviewModal
      v-if="reviewTarget"
      :isOpen="showReviewModal"
      :job="reviewTarget"
      @close="showReviewModal = false"
      @submit="handleReviewSubmit"
    />
  </div>
</template>

<style scoped>
.page-wrapper {
  padding-top: var(--spacing-lg);
  padding-bottom: var(--spacing-xxl);
}

.page-header {
  margin-bottom: var(--spacing-xl);
}

.page-header h1 {
  font-size: 2rem;
  font-weight: 800;
  margin-bottom: var(--spacing-xs);
}

.subtitle {
  color: var(--color-text-light);
  font-size: 1.1rem;
}

/* Section Styles */
.section-group {
  margin-bottom: var(--spacing-xxl);
}

.section-title {
  font-size: 1.4rem;
  font-weight: 700;
  color: var(--color-text);
  margin-bottom: var(--spacing-lg);
  padding-bottom: var(--spacing-xs);
  border-bottom: 2px solid #f0f0f0;
}

.past-section .section-title {
  color: var(--color-text-light);
}

.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
}

.faded-grid {
  opacity: 0.85;
}

.info-message {
  padding: 20px 0;
  color: var(--color-text-light);
  font-style: italic;
}

/* Empty State Styles */
.empty-state {
  text-align: center;
  padding: var(--spacing-xxl) 0;
  background-color: #f9f9f9;
  border-radius: 16px;
  border: 2px dashed var(--color-border);
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: var(--spacing-md);
}

.empty-state h3 {
  margin-bottom: var(--spacing-sm);
  font-weight: 700;
}

.empty-state p {
  color: var(--color-text-light);
  margin-bottom: var(--spacing-lg);
}

.loading-state, .error-state {
  text-align: center;
  padding: 40px;
  color: var(--color-text-light);
}
</style>
