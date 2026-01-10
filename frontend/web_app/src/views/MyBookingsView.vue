<script setup>
import { ref, onMounted, computed } from 'vue';
import api from '@/api';
import BookingCard from '@/components/BookingCard.vue';
import ReviewModal from '@/components/ReviewModal.vue';
import { useToastStore } from '@/stores/toast';

const bookings = ref([]);
const loading = ref(true);
const error = ref(null);
const toast = useToastStore();

// --- Review State ---
const showReviewModal = ref(false);
const reviewTarget = ref(null);

const fetchBookings = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.getMyBookings();
    bookings.value = response.data;
  } catch (err) {
    console.error(err);
    error.value = "Deine Buchungen konnten nicht geladen werden.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchBookings);

// --- Computed Properties für die Aufteilung ---
const activeBookings = computed(() => {
  return bookings.value.filter(b => {
    // Stornierte sind immer vergangen
    if (b.status === 'CANCELLED') return false;
    // Erledigte mit Bewertung sind vergangen
    if (b.status === 'COMPLETED' && b.review) return false;
    // Alles andere (Pending, Confirmed, Completed ohne Review) ist "Aktuell"
    return true;
  });
});

const pastBookings = computed(() => {
  return bookings.value.filter(b => {
    // Stornierte ODER (Erledigte MIT Bewertung)
    return b.status === 'CANCELLED' || (b.status === 'COMPLETED' && b.review);
  });
});


const handleCancel = async (bookingId) => {
  if (!confirm("Möchtest du diese Buchung wirklich stornieren?")) return;

  try {
    await api.cancelBooking(bookingId);
    toast.addToast("Buchung erfolgreich storniert", "success");
    await fetchBookings();
  } catch (err) {
    toast.addToast("Fehler beim Stornieren der Buchung", "error");
  }
};

const openReviewModal = (booking) => {
  reviewTarget.value = {
    id: booking.id,
    title: booking.service.title
  };
  showReviewModal.value = true;
};

const handleReviewSubmit = async (payload) => {
  try {
    await api.createReview({
      booking: payload.job,
      rating: payload.rating,
      comment: payload.comment
    });

    toast.addToast("Bewertung erfolgreich gesendet!", "success");
    showReviewModal.value = false;
    await fetchBookings();
  } catch (err) {
    const msg = err.response?.data?.detail || "Fehler beim Senden der Bewertung.";
    toast.addToast(msg, "error");
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

/* Neue Styles für die Sektionen */
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

/* Optional: Vergangene Aufträge leicht ausblassen, um Fokus auf Aktuelles zu lenken */
.faded-grid {
  opacity: 0.85;
}

.info-message {
  padding: 20px 0;
  color: var(--color-text-light);
  font-style: italic;
}

/* Empty State Styles (wie zuvor) */
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