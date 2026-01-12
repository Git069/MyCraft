<script setup>
/**
 * JobDetailView.vue
 *
 * Displays detailed information about a specific job.
 * Allows users to view job details, contact the contractor, create a booking,
 * and get AI-based price advice.
 */

import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter, RouterLink } from 'vue-router';

import { useAuthStore } from '@/stores/auth';
import api from '@/api';

import DetailHighlight from '@/components/DetailHighlight.vue';
import { STATUS_TRANSLATIONS, TRADE_TRANSLATIONS } from '@/constants';

/* ==========================================================================
   State & Setup
   ========================================================================== */

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const jobId = route.params.id;

// Job Data
const job = ref(null);
const loading = ref(true);
const error = ref(null);

// Interaction State
const isStartingConversation = ref(false);

// Booking State
const bookingDate = ref('');
const isBooking = ref(false);
const bookingError = ref(null);

// AI Advice State
const aiAdvice = ref(null);
const loadingAi = ref(false);

// Constants
const tradeImages = {
  PLUMBER: 'https://images.unsplash.com/photo-1581244277943-fe4a9c777189?auto=format&fit=crop&w=800&q=80',
  ELECTRICIAN: 'https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=800&q=80',
  PAINTER: 'https://images.unsplash.com/photo-1589939705384-5185137a7f0f?auto=format&fit=crop&w=800&q=80',
  CARPENTER: 'https://images.unsplash.com/photo-1611021061285-19a87a1964e2?auto=format&fit=crop&w=800&q=80',
  GARDENER: 'https://images.unsplash.com/photo-1558904541-efa843a96f01?auto=format&fit=crop&w=800&q=80',
  OTHER: 'https://images.unsplash.com/photo-1504328345606-18bbc8c9d7d1?auto=format&fit=crop&w=800&q=80',
};

/* ==========================================================================
   Computed Properties
   ========================================================================== */

const isLoggedIn = computed(() => authStore.isLoggedIn);
const currentUser = computed(() => authStore.currentUser);

/**
 * Calculates today's date in YYYY-MM-DD format for the date input min attribute.
 * @returns {string} Date string in YYYY-MM-DD format.
 */
const minDate = computed(() => {
  const today = new Date();
  return today.toISOString().split('T')[0];
});

/**
 * Determines if the current user can contact the job owner.
 * Users cannot contact themselves or if they are not logged in (though UI handles login prompt).
 * @returns {boolean} True if contact is allowed.
 */
const canContact = computed(() => {
  if (!isLoggedIn.value || !job.value) return false;
  return job.value.contractor !== currentUser.value?.id;
});

/**
 * Selects a hero image based on the job's trade category.
 * @returns {string} URL of the hero image.
 */
const heroImage = computed(() => {
  if (!job.value) return tradeImages.OTHER;
  return tradeImages[job.value.trade] || tradeImages.OTHER;
});

/**
 * Translates the job status code to a human-readable string.
 * @returns {string} Translated status.
 */
const translatedStatus = computed(() => {
  if (!job.value) return '';
  const status = job.value.status;
  return STATUS_TRANSLATIONS[status] || status;
});

/**
 * Translates the trade code to a human-readable string.
 * @returns {string} Translated trade name.
 */
const translatedTrade = computed(() => {
  if (!job.value) return '';
  const trade = job.value.trade;
  return TRADE_TRANSLATIONS[trade] || trade;
});

/* ==========================================================================
   Lifecycle Hooks
   ========================================================================== */

/**
 * Fetches job details when the component is mounted.
 */
onMounted(fetchJobDetails);

/* ==========================================================================
   Methods
   ========================================================================== */

/**
 * Fetches the job details from the API.
 * Updates the job state or sets an error message.
 */
async function fetchJobDetails() {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.getJobDetails(jobId);
    job.value = response.data;
  } catch (err) {
    error.value = 'Fehler: Der Auftrag konnte nicht geladen werden.';
  } finally {
    loading.value = false;
  }
}

/**
 * Formats a numeric price into a localized currency string.
 * @param {number} price - The price to format.
 * @returns {string} Formatted price string.
 */
const formatPrice = (price) => {
  if (!price) return 'Preis auf Anfrage';
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
};

/**
 * Handles the booking process.
 * Creates a booking for the current job at the selected date.
 * Redirects to "My Bookings" on success.
 */
const handleBooking = async () => {
  if (!bookingDate.value) return;

  isBooking.value = true;
  bookingError.value = null;

  try {
    // We only send service ID and date.
    // The price is automatically taken from the service in the backend.
    await api.createBooking({
      service_id: job.value.id,
      scheduled_date: bookingDate.value,
    });

    // Redirect to "My Bookings" on success
    router.push({ name: 'MyBookings' });
  } catch (err) {
    // Handle backend errors (e.g., date already taken)
    bookingError.value = err.response?.data?.scheduled_date?.[0]
                         || err.response?.data?.non_field_errors?.[0]
                         || 'Buchung fehlgeschlagen.';
  } finally {
    isBooking.value = false;
  }
};

/**
 * Initiates a conversation with the job owner.
 * Redirects to the Inbox with the new conversation active.
 */
const handleContact = async () => {
  if (!canContact.value) return;
  isStartingConversation.value = true;
  error.value = null;
  try {
    const initialMessage = `Hallo, ich interessiere mich für deinen Auftrag "${job.value.title}".`;
    const response = await api.startConversation(jobId, initialMessage);
    const conversationId = response.data.id;
    router.push({ name: 'Inbox', query: { active_convo: conversationId } });
  } catch (err) {
    error.value = err.response?.data?.detail || 'Konversation konnte nicht gestartet werden.';
  } finally {
    isStartingConversation.value = false;
  }
};

/**
 * Requests AI-based price advice for the current job.
 * Updates the aiAdvice state with the result.
 */
const getPriceAdvice = async () => {
  loadingAi.value = true;
  aiAdvice.value = null;
  try {
    const response = await api.getPriceAdvice(jobId);
    aiAdvice.value = response.data.advice;
  } catch (err) {
    console.error(err);
    aiAdvice.value = 'Entschuldigung, die KI ist gerade nicht erreichbar.';
  } finally {
    loadingAi.value = false;
  }
};
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
              <span class="title">Auftrag von {{ job.contractor_username || 'Unbekannt' }}</span>
              <span class="subtitle">Verifizierter Handwerker</span>
            </div>
          </section>

          <div class="divider"></div>

          <section class="highlights-section">
            <DetailHighlight icon="🛠️" title="Gewerk" :subtitle="translatedTrade" />
            <DetailHighlight v-if="job.execution_date" icon="🗓️" title="Wunschtermin" :subtitle="new Date(job.execution_date).toLocaleDateString()" />
            <DetailHighlight icon="💰" title="Status" :subtitle="translatedStatus" />
          </section>

          <div class="divider"></div>

          <section class="description-section">
            <h2>Beschreibung</h2>
            <p>{{ job.description }}</p>
          </section>

          <div class="divider"></div>

          <section class="ai-section">
            <div class="ai-header">
              <h3>🤖 KI-Preischeck</h3>
              <span class="beta-badge">Beta</span>
            </div>
            <p class="ai-intro">Unsicher beim Preis? Lass dir von unserer KI eine unverbindliche Einschätzung geben.</p>

            <div v-if="!aiAdvice" class="ai-action">
              <button @click="getPriceAdvice" class="base-button ai-btn" :disabled="loadingAi">
                {{ loadingAi ? 'KI analysiert...' : 'Preis einschätzen lassen' }}
              </button>
            </div>

            <div v-else class="ai-result">
              <div class="result-bubble">{{ aiAdvice }}</div>
              <button @click="getPriceAdvice" class="retry-link">Neu berechnen</button>
            </div>
          </section>
        </div>

        <div class="right-column">
          <aside class="action-card">
            <div class="price-header">
              <span class="price">{{ formatPrice(job.price) }}</span>
              <span class="price-label">Festpreis</span>
            </div>

            <div class="action-body">

              <button
                v-if="canContact"
                @click="handleContact"
                class="base-button secondary-action"
                :disabled="isStartingConversation"
              >
                {{ isStartingConversation ? 'Öffne Chat...' : 'Nachricht schreiben' }}
              </button>

              <div v-if="canContact" class="separator">oder direkt buchen</div>

              <div v-if="canContact" class="booking-widget">
                <label for="booking-date" class="date-label">Wunschtermin wählen:</label>
                <input
                  id="booking-date"
                  type="date"
                  v-model="bookingDate"
                  class="date-input"
                  :min="minDate"
                />

                <button
                  @click="handleBooking"
                  class="base-button primary-action"
                  :disabled="!bookingDate || isBooking"
                >
                  {{ isBooking ? 'Wird gebucht...' : 'Kostenpflichtig buchen' }}
                </button>

                <div v-if="bookingError" class="error-message">{{ bookingError }}</div>
              </div>

              <div v-else-if="!isLoggedIn" class="login-prompt">
                <router-link :to="{ name: 'Login' }">Melde dich an</router-link>, um diesen Auftrag zu buchen.
              </div>

              <div v-else-if="!canContact" class="own-job-info">
                Dies ist dein eigener Auftrag.
              </div>

            </div>

            <footer class="action-footer">
              <p v-if="bookingDate">Mit Klick auf "Kostenpflichtig buchen" gehst du einen verbindlichen Vertrag ein.</p>
              <p v-else>Wähle einen Termin für die Buchung.</p>
            </footer>
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.detail-page-wrapper {
  padding: var(--spacing-lg) 0;
}

.image-hero-section {
  width: 100%;
  max-height: 400px;
  overflow: hidden;
  border-radius: 16px;
  margin-bottom: var(--spacing-xl);
}

.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

.main-content-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-xxl);
}

@media (min-width: 992px) {
  .main-content-grid {
    grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr);
  }
}

.job-header h1 {
  font-size: 2rem;
  font-weight: 800;
  margin-top: 0;
  margin-bottom: var(--spacing-xs);
  text-transform: capitalize;
}

.meta-info {
  font-size: 1rem;
  color: var(--color-text-light);
}

.divider {
  border-bottom: 1px solid var(--color-border);
  margin: 32px 0;
}

.contractor-section {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.avatar-placeholder {
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background-color: #f1f1f1;
  flex-shrink: 0;
}

.contractor-text .title {
  display: block;
  font-weight: 600;
  font-size: 1.1rem;
}

.contractor-text .subtitle {
  font-size: 0.9rem;
  color: var(--color-text-light);
}

.highlights-section {
  display: grid;
  grid-template-columns: 1fr;
  gap: 24px;
}

@media (min-width: 768px) {
  .highlights-section {
    grid-template-columns: 1fr 1fr;
  }
}

.description-section h2 {
  font-size: 1.5rem;
  margin-top: 0;
  margin-bottom: var(--spacing-md);
}

.description-section p {
  line-height: 1.7;
  white-space: pre-wrap;
}

/* Right Column & Card Styles */
.right-column {
  position: relative;
}

.action-card {
  background-color: white;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  position: sticky;
  top: 120px;
}

.price-header {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: 24px;
}

.price {
  font-size: 1.5rem;
  font-weight: 800;
}

.price-label {
  color: var(--color-text-light);
  font-size: 1rem;
}

.action-body {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

/* Booking Widget Styles */
.booking-widget {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 8px;
}

.date-label {
  font-size: 0.9rem;
  font-weight: 600;
  color: var(--color-text);
}

.date-input {
  padding: 10px;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-family: inherit;
  font-size: 1rem;
  width: 100%;
}

.primary-action {
  width: 100%;
  font-size: 1rem;
  padding: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  background-color: var(--color-primary);
  color: white;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.primary-action:hover {
  background-color: var(--color-primary-dark, #0056b3);
}

.primary-action:disabled {
  background-color: #ccc;
  cursor: not-allowed;
}

.secondary-action {
  width: 100%;
  font-size: 1rem;
  padding: 14px;
  font-weight: 600;
  cursor: pointer;
  border: none;
  background-color: var(--color-primary);
  color: white;
  border-radius: 8px;
  transition: background-color 0.2s;
}

.secondary-action:hover {
  background-color: var(--color-primary-dark, #0056b3);
}

.separator {
  text-align: center;
  font-size: 0.85rem;
  color: #999;
  margin: 4px 0;
}

.error-message {
  color: var(--color-error);
  font-size: 0.85rem;
  margin-top: 4px;
}

.action-footer {
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-text-light);
  margin-top: 16px;
  line-height: 1.4;
}

.own-job-info {
  text-align: center;
  color: #666;
  font-style: italic;
}

/* AI Section Styles */
.ai-section {
  background: linear-gradient(to right, #f8f9fa, #e3f2fd);
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #d1e7dd;
  margin-top: 20px;
}

.ai-header {
  display: flex;
  align-items: center;
  gap: 10px;
  margin-bottom: 8px;
}

.ai-header h3 {
  margin: 0;
  font-size: 1.2rem;
  font-weight: 700;
  color: #333;
}

.beta-badge {
  background: #666;
  color: white;
  font-size: 0.7rem;
  padding: 2px 8px;
  border-radius: 12px;
  font-weight: 600;
  text-transform: uppercase;
}

.ai-intro {
  font-size: 0.95rem;
  color: #555;
  margin-bottom: 20px;
  line-height: 1.5;
}

.ai-btn {
  background-color: white;
  border: 1px solid #0d6efd;
  color: #0d6efd;
  padding: 10px 20px;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
}

.ai-btn:hover:not(:disabled) {
  background-color: #0d6efd;
  color: white;
}

.ai-btn:disabled {
  opacity: 0.6;
  cursor: wait;
}

.result-bubble {
  background: white;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #0d6efd;
  font-style: italic;
  color: #333;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  white-space: pre-wrap;
}

.retry-link {
  background: none;
  border: none;
  color: #666;
  font-size: 0.85rem;
  text-decoration: underline;
  cursor: pointer;
  margin-top: 12px;
  display: block;
}

.retry-link:hover {
  color: #333;
}
</style>
