<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';
import DetailHighlight from '@/components/DetailHighlight.vue';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const job = ref(null);
const loading = ref(true);
const error = ref(null);

// Buchungs-State
const isStartingConversation = ref(false);
const isBooking = ref(false);
const bookingDate = ref('');
const bookingError = ref(null);
const busyDates = ref([]); // Liste der blockierten Tage vom Backend

const jobId = route.params.id;

const isLoggedIn = computed(() => authStore.isLoggedIn);
const currentUser = computed(() => authStore.currentUser);

// Darf der User buchen/kontaktieren? (Nicht der eigene Job)
const canInteract = computed(() => {
  if (!isLoggedIn.value || !job.value) return false;
  return job.value.contractor !== currentUser.value?.id;
});

// Datumsgrenzen für das Input-Feld
const minDate = computed(() => {
  const tomorrow = new Date();
  tomorrow.setDate(tomorrow.getDate() + 1);
  return tomorrow.toISOString().split('T')[0];
});

// -- LOGIK: Verfügbarkeit laden --
const fetchAvailability = async () => {
  try {
    const response = await api.getServiceAvailability(jobId);
    busyDates.value = response.data; // Erwartet Array ["2024-10-25", ...]
  } catch (err) {
    console.error("Konnte Verfügbarkeit nicht laden", err);
  }
};

const fetchJobDetails = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.getJobDetails(jobId);
    job.value = response.data;
    // Wenn Job geladen, hole Verfügbarkeit
    if (job.value) {
      await fetchAvailability();
    }
  } catch (err) {
    error.value = "Fehler: Der Auftrag konnte nicht geladen werden.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchJobDetails);

// -- LOGIK: Buchung durchführen --
const handleBooking = async () => {
  if (!bookingDate.value) return;

  // Client-Side Check: Ist das Datum in der busy-list?
  if (busyDates.value.includes(bookingDate.value)) {
    bookingError.value = "Dieser Termin ist leider schon vergeben.";
    return;
  }

  isBooking.value = true;
  bookingError.value = null;

  try {
    await api.createBooking({
      service_id: job.value.id,
      scheduled_date: bookingDate.value
    });

    // Erfolg! Weiterleitung zur Startseite statt zum Chat
    router.push({ name: 'Home' });

  } catch (err) {
    // Fehler vom Backend anzeigen (z.B. "Bereits ausgebucht")
    bookingError.value = err.response?.data?.scheduled_date?.[0] ||
                         err.response?.data?.non_field_errors?.[0] ||
                         "Buchung fehlgeschlagen.";
  } finally {
    isBooking.value = false;
  }
};

const handleContact = async () => {
  if (!canInteract.value) return;
  isStartingConversation.value = true;
  error.value = null;
  try {
    const initialMessage = `Hallo, ich interessiere mich für deinen Auftrag "${job.value.title}".`;
    const response = await api.startConversation(jobId, initialMessage);
    const conversationId = response.data.id;
    router.push({ name: 'Inbox', query: { active_convo: conversationId } });
  } catch (err) {
    error.value = err.response?.data?.detail || "Konversation konnte nicht gestartet werden.";
  } finally {
    isStartingConversation.value = false;
  }
};

const formatPrice = (price) => {
  if (!price) return 'Preis auf Anfrage';
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
};

const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=800&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=800&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=800&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=800&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=800&q=80'
};

const heroImage = computed(() => {
  if (!job.value) return tradeImages.OTHER;
  return tradeImages[job.value.trade] || tradeImages.OTHER;
});
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading-state">Lade Auftragsdetails...</div>
    <div v-else-if="job" class="detail-page-wrapper">

      <div class="image-hero-section">
        <img :src="heroImage" alt="Job category image" class="hero-image" />
      </div>

      <div class="main-content-grid">
        <div class="left-column">
          <header class="job-header">
            <h1>{{ job.title }}</h1>
            <p class="meta-info">{{ job.city }}, {{ job.zip_code }}</p>
          </header>

          <div class="divider"></div>

          <section class="contractor-section">
            <RouterLink :to="{ name: 'CraftsmanProfile', params: { id: job.contractor } }">
              <div class="avatar-placeholder"></div>
            </RouterLink>
            <div class="contractor-text">
              <span class="title">Auftrag von {{ job.contractor_username }}</span>
              <span class="subtitle">Seit 2024 dabei</span>
            </div>
          </section>

          <div class="divider"></div>

          <section class="highlights-section">
            <DetailHighlight icon="🛠️" title="Gewerk" :subtitle="job.trade" />
            <DetailHighlight v-if="job.execution_date" icon="🗓️" title="Wunschtermin" :subtitle="new Date(job.execution_date).toLocaleDateString()" />
            <DetailHighlight icon="💰" title="Status" :subtitle="job.status" />
          </section>

          <div class="divider"></div>

          <section class="description-section">
            <h2>Beschreibung</h2>
            <p>{{ job.description }}</p>
          </section>
        </div>

        <div class="right-column">
          <aside class="action-card">
            <div class="price-header">
              <span class="price">{{ formatPrice(job.price) }}</span>
              <span class="price-label">Festpreis</span>
            </div>

            <div class="action-body">
              <div v-if="!isLoggedIn" class="login-prompt">
                <router-link :to="{ name: 'Login' }">Melde dich an</router-link>, um zu buchen.
              </div>

              <div v-else-if="canInteract" class="booking-form">

                <div class="date-picker-group">
                  <label for="booking-date">Wunschtermin wählen:</label>
                  <input
                    type="date"
                    id="booking-date"
                    v-model="bookingDate"
                    :min="minDate"
                    class="date-input"
                  />
                  <div v-if="busyDates.includes(bookingDate)" class="date-warning">
                    ⚠️ Dieser Termin ist bereits belegt.
                  </div>
                </div>

                <button
                  @click="handleBooking"
                  class="base-button primary-action book-btn"
                  :disabled="isBooking || !bookingDate || busyDates.includes(bookingDate)"
                >
                  {{ isBooking ? 'Buche...' : 'Verbindlich buchen' }}
                </button>

                <div v-if="bookingError" class="error-message booking-error">
                  {{ bookingError }}
                </div>

                <div class="divider-small">oder</div>

                <button
                  @click="handleContact"
                  class="base-button secondary-action"
                  :disabled="isStartingConversation"
                >
                  {{ isStartingConversation ? '...' : 'Frage stellen' }}
                </button>
              </div>

              <div v-else class="owner-info">
                Das ist dein eigener Auftrag.
              </div>
            </div>

            <footer class="action-footer">
              <p v-if="canInteract">Mit der Buchung akzeptierst du die AGB.</p>
            </footer>
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Layout */
.detail-page-wrapper { padding: var(--spacing-lg) 0; }
.image-hero-section { width: 100%; max-height: 400px; overflow: hidden; border-radius: 16px; margin-bottom: var(--spacing-xl); }
.hero-image { width: 100%; height: 100%; object-fit: cover; }
.main-content-grid { display: grid; grid-template-columns: 1fr; gap: var(--spacing-xxl); }

@media (min-width: 992px) {
  .main-content-grid { grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); }
}

/* Header & Info */
.job-header h1 { font-size: 2rem; font-weight: 800; margin-top: 0; margin-bottom: var(--spacing-xs); text-transform: capitalize; }
.meta-info { font-size: 1rem; color: var(--color-text-light); }
.divider { border-bottom: 1px solid var(--color-border); margin: 32px 0; }
.contractor-section { display: flex; align-items: center; gap: 16px; padding: 8px 0; }
.avatar-placeholder { width: 56px; height: 56px; border-radius: 50%; background-color: #f1f1f1; flex-shrink: 0; }
.contractor-text .title { display: block; font-weight: 600; font-size: 1.1rem; }
.contractor-text .subtitle { font-size: 0.9rem; color: var(--color-text-light); }
.highlights-section { display: grid; grid-template-columns: 1fr; gap: 24px; }
@media (min-width: 768px) { .highlights-section { grid-template-columns: 1fr 1fr; } }
.description-section h2 { font-size: 1.5rem; margin-top: 0; margin-bottom: var(--spacing-md); }
.description-section p { line-height: 1.7; white-space: pre-wrap; }

/* Rechte Spalte (Sticky Card) */
.right-column { position: relative; }
.action-card { background-color: white; border: 1px solid var(--color-border); border-radius: 12px; padding: 24px; box-shadow: 0 6px 16px rgba(0,0,0,0.12); position: sticky; top: 120px; }
.price-header { display: flex; align-items: baseline; gap: 8px; margin-bottom: 24px; }
.price { font-size: 1.5rem; font-weight: 800; }
.price-label { color: var(--color-text-light); font-size: 1rem; }

/* Buchungsformular */
.booking-form { display: flex; flex-direction: column; gap: 12px; }
.date-picker-group { display: flex; flex-direction: column; gap: 8px; margin-bottom: 8px; }
.date-picker-group label { font-size: 0.9rem; font-weight: 600; color: var(--color-text); }
.date-input { padding: 12px; border: 1px solid var(--color-border); border-radius: 8px; font-family: inherit; font-size: 1rem; }
.date-input:focus { border-color: var(--color-primary); outline: none; }
.date-warning { font-size: 0.85rem; color: var(--color-error); margin-top: 4px; }

/* Buttons */
.primary-action { width: 100%; font-size: 1rem; padding: 14px; font-weight: 600; cursor: pointer; }
.book-btn { background-color: var(--color-primary); color: white; border: none; border-radius: 8px; transition: background-color 0.2s; }
.book-btn:hover:not(:disabled) { background-color: var(--color-primary-dark, #0056b3); }
.book-btn:disabled { background-color: #ccc; cursor: not-allowed; }

/* HIER WAR DER FEHLER: */
.secondary-action {
  width: 100%;
  background-color: transparent;
  color: var(--color-text); /* <--- Das fehlte! */
  border: 1px solid var(--color-border);
  padding: 10px;
  border-radius: 8px;
  cursor: pointer;
  font-weight: 600;
  transition: all 0.2s;
}
.secondary-action:hover { border-color: var(--color-text); background-color: #f9f9f9; }

.divider-small { text-align: center; font-size: 0.85rem; color: var(--color-text-light); margin: 4px 0; }
.error-message { color: var(--color-error); font-size: 0.9rem; margin-top: 8px; text-align: center; }
.action-footer { text-align: center; font-size: 0.85rem; color: var(--color-text-light); margin-top: 16px; }
.owner-info { text-align: center; color: var(--color-text-light); font-style: italic; padding: 10px; background-color: #f5f5f5; border-radius: 8px; }
</style>