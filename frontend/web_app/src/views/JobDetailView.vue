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
const isStartingConversation = ref(false);

// KI State
const aiAdvice = ref(null);
const loadingAi = ref(false);

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
    router.push({ name: 'Inbox', query: { active_convo: conversationId } });
  } catch (err) {
    error.value = err.response?.data?.detail || "Konversation konnte nicht gestartet werden.";
  } finally {
    isStartingConversation.value = false;
  }
};

// -- NEU: KI Preis-Check Funktion --
const getPriceAdvice = async () => {
  loadingAi.value = true;
  aiAdvice.value = null;
  try {
    // Ruft die neue Funktion in api.js auf
    const response = await api.getPriceAdvice(jobId);
    aiAdvice.value = response.data.advice;
  } catch (err) {
    console.error(err);
    aiAdvice.value = "Entschuldigung, die KI ist gerade nicht erreichbar.";
  } finally {
    loadingAi.value = false;
  }
};
// ----------------------------------

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

          <div class="divider"></div>

          <section class="ai-section">
            <div class="ai-header">
              <h3>🤖 KI-Preischeck</h3>
              <span class="beta-badge">Beta</span>
            </div>
            <p class="ai-intro">Unsicher beim Preis? Lass dir von unserer KI eine unverbindliche Einschätzung geben.</p>

            <div v-if="!aiAdvice" class="ai-action">
              <button
                @click="getPriceAdvice"
                class="base-button ai-btn"
                :disabled="loadingAi"
              >
                {{ loadingAi ? 'KI analysiert...' : 'Preis einschätzen lassen' }}
              </button>
            </div>

            <div v-else class="ai-result">
              <div class="result-bubble">
                {{ aiAdvice }}
              </div>
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
/* Bestehende Styles */
.detail-page-wrapper { padding: var(--spacing-lg) 0; }
.image-hero-section { width: 100%; max-height: 400px; overflow: hidden; border-radius: 16px; margin-bottom: var(--spacing-xl); }
.hero-image { width: 100%; height: 100%; object-fit: cover; }
.main-content-grid { display: grid; grid-template-columns: 1fr; gap: var(--spacing-xxl); }
@media (min-width: 992px) { .main-content-grid { grid-template-columns: minmax(0, 1.5fr) minmax(0, 1fr); } }
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

/* Rechte Spalte */
.right-column { position: relative; }
.action-card { background-color: white; border: 1px solid var(--color-border); border-radius: 12px; padding: 24px; box-shadow: 0 6px 16px rgba(0,0,0,0.12); position: sticky; top: 120px; }
.price-header { display: flex; align-items: baseline; gap: 8px; margin-bottom: 24px; }
.price { font-size: 1.5rem; font-weight: 800; }
.price-label { color: var(--color-text-light); font-size: 1rem; }
.primary-action { width: 100%; font-size: 1rem; padding: 14px; font-weight: 600; cursor: pointer; border: none; background-color: var(--color-primary); color: white; border-radius: 8px; }
.primary-action:hover { background-color: var(--color-primary-dark, #0056b3); }
.primary-action:disabled { background-color: #ccc; cursor: not-allowed; }
.action-footer { text-align: center; font-size: 0.85rem; color: var(--color-text-light); margin-top: 16px; }

/* --- NEU: KI Styles --- */
.ai-section {
  background: linear-gradient(to right, #f8f9fa, #e3f2fd);
  padding: 24px;
  border-radius: 12px;
  border: 1px solid #d1e7dd;
  margin-top: 20px;
}
.ai-header { display: flex; align-items: center; gap: 10px; margin-bottom: 8px; }
.ai-header h3 { margin: 0; font-size: 1.2rem; font-weight: 700; color: #333; }
.beta-badge { background: #666; color: white; font-size: 0.7rem; padding: 2px 8px; border-radius: 12px; font-weight: 600; text-transform: uppercase; }
.ai-intro { font-size: 0.95rem; color: #555; margin-bottom: 20px; line-height: 1.5; }

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
.ai-btn:hover:not(:disabled) { background-color: #0d6efd; color: white; }
.ai-btn:disabled { opacity: 0.6; cursor: wait; }

.result-bubble {
  background: white;
  padding: 16px;
  border-radius: 8px;
  border-left: 4px solid #0d6efd;
  font-style: italic;
  color: #333;
  line-height: 1.6;
  box-shadow: 0 2px 8px rgba(0,0,0,0.05);
  white-space: pre-wrap; /* Wichtig für Zeilenumbrüche der KI */
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
.retry-link:hover { color: #333; }
</style>