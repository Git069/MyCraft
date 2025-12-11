<script setup>
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';
import DetailHighlight from '@/components/DetailHighlight.vue';
import { TRADE_IMAGES } from '@/constants';

const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

const job = ref(null);
const loading = ref(true);
const error = ref(null);
const isStartingConversation = ref(false);

const jobId = route.params.id;

const isLoggedIn = computed(() => authStore.isLoggedIn);
const currentUser = computed(() => authStore.currentUser);

const canContact = computed(() => {
  if (!isLoggedIn.value || !job.value) return false;
  return job.value.contractor !== currentUser.value?.id;
});

const handleContact = async () => {
  if (!canContact.value) return;

  isStartingConversation.value = true;
  error.value = null;
  try {
    const initialMessage = `Hallo, ich interessiere mich für deinen Auftrag "${job.value.title}".`;
    const response = await api.startConversation(jobId, initialMessage);

    const conversationId = response.data.id;

    // Redirect to the inbox and pass the new conversation ID as a query param
    router.push({ name: 'Inbox', query: { active_convo: conversationId } });

  } catch (err) {
    error.value = err.response?.data?.detail || "Konversation konnte nicht gestartet werden.";
    console.error("Conversation start failed:", err);
  } finally {
    isStartingConversation.value = false;
  }
};

const fetchJobDetails = async () => {
  loading.value = true;
  error.value = null;
  try {
    const response = await api.getJobDetails(jobId);
    job.value = response.data;
  } catch (err) {
    error.value = "Fehler: Der Auftrag konnte nicht geladen werden.";
  } finally {
    loading.value = false;
  }
};

onMounted(fetchJobDetails);

const formatPrice = (price) => {
  if (!price) return 'Preis auf Anfrage';
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
};

const heroImage = computed(() => {
  if (!job.value) return TRADE_IMAGES.OTHER;
  return TRADE_IMAGES[job.value.trade] || TRADE_IMAGES.OTHER;
});
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading-state">Lade Auftragsdetails...</div>
    <div v-if="error && !isStartingConversation" class="error-message">{{ error }}</div>

    <div v-if="job" class="detail-page-wrapper">
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
            <div class="avatar-placeholder"></div>
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
              <button v-if="canContact" @click="handleContact" class="base-button primary-action" :disabled="isStartingConversation">
                {{ isStartingConversation ? 'Wird gesendet...' : 'Handwerker kontaktieren' }}
              </button>
              <div v-else-if="!isLoggedIn" class="login-prompt">
                <router-link :to="{ name: 'Login' }">Melde dich an</router-link>, um zu kontaktieren.
              </div>
            </div>

            <div v-if="error && isStartingConversation" class="error-message booking-error">{{ error }}</div>

            <footer class="action-footer">
              <p>Du gehst noch keine verbindliche Buchung ein.</p>
            </footer>
          </aside>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
/* Styles remain the same */
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
  margin-top: 0;
  margin-bottom: var(--spacing-xs);
}
.meta-info {
  font-size: 1rem;
  color: var(--color-text-light);
}
.divider {
  border-bottom: 1px solid var(--color-border);
  margin: var(--spacing-lg) 0;
}
.contractor-section {
  display: flex;
  align-items: center;
  gap: 16px;
}
.avatar-placeholder {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  background-color: #f1f1f1;
  flex-shrink: 0;
}
.contractor-text .title {
  display: block;
  font-weight: 600;
}
.contractor-text .subtitle {
  font-size: 0.9rem;
  color: var(--color-text-light);
}
.highlights-section {
  display: grid;
  gap: var(--spacing-lg);
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
.right-column {
  position: relative;
}
.action-card {
  background-color: white;
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: var(--spacing-lg);
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
  position: sticky;
  top: 100px;
}
.price-header {
  display: flex;
  align-items: baseline;
  gap: 8px;
  margin-bottom: var(--spacing-lg);
}
.price {
  font-size: 1.5rem;
  font-weight: 700;
}
.price-label {
  color: var(--color-text-light);
}
.primary-action {
  width: 100%;
  font-size: 1rem;
  padding: 12px;
}
.action-footer {
  text-align: center;
  font-size: 0.8rem;
  color: var(--color-text-light);
  margin-top: var(--spacing-md);
}
.login-prompt {
  text-align: center;
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  background-color: #f8f9fa;
  color: var(--color-text-light);
}
.login-prompt a {
  font-weight: bold;
}
.error-message {
  background-color: #fff0f0;
  color: var(--color-error);
  padding: 12px;
  border-radius: 8px;
  margin-top: 1rem;
  text-align: center;
}
</style>
