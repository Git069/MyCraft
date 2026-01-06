<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import BookingCard from '@/components/BookingCard.vue';
import { useToastStore } from '@/stores/toast';

const bookings = ref([]);
const loading = ref(true);
const error = ref(null);
const toast = useToastStore();

const fetchBookings = async () => {
  loading.value = true;
  error.value = null;
  try {
    // Ruft /bookings/my_bookings/ auf (Backend filtert nach customer=request.user)
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

// Funktion zum Stornieren (wird vom Event der BookingCard ausgelöst)
const handleCancel = async (bookingId) => {
  if (!confirm("Möchtest du diese Buchung wirklich stornieren?")) return;

  try {
    await api.cancelBooking(bookingId);
    toast.addToast("Buchung erfolgreich storniert", "success");
    // Liste aktualisieren, um den neuen Status anzuzeigen
    await fetchBookings();
  } catch (err) {
    toast.addToast("Fehler beim Stornieren der Buchung", "error");
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

    <div v-else class="bookings-grid">
      <BookingCard
        v-for="booking in bookings"
        :key="booking.id"
        :booking="booking"
        :show-controls="true"
        @cancel="handleCancel"
      />
    </div>
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

.bookings-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: var(--spacing-lg);
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