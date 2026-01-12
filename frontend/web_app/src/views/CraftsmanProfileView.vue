<script setup>
// --- Imports ---
import { ref, onMounted, computed } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import { useAuthStore } from '@/stores/auth';
import StarRating from '@/components/StarRating.vue';

// --- Setup ---
const route = useRoute();
const router = useRouter();
const authStore = useAuthStore();

// --- State ---
const craftsman = ref(null);
const loading = ref(true);
const craftsmanId = route.params.id;

// --- Computed Properties ---
const currentUser = computed(() => authStore.currentUser);

const isOwnProfile = computed(() => {
  return currentUser.value && currentUser.value.id === parseInt(craftsmanId, 10);
});

const memberSince = computed(() => {
  if (!craftsman.value?.date_joined) return '';
  return new Date(craftsman.value.date_joined).getFullYear();
});

// --- Methods ---

/**
 * Constructs the full URL for an image path.
 * @param {string} url - The relative image URL.
 * @returns {string|null} The full URL or null.
 */
const fullImageUrl = (url) => url ? `http://localhost:8000${url}` : null;

/**
 * Formats a date string into a localized month and year string.
 * @param {string} dateString - The date string to format.
 * @returns {string} Formatted date string.
 */
const formatReviewDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('de-DE', { month: 'long', year: 'numeric' });
};

/**
 * Handles the contact button click.
 * Navigates to the inbox.
 */
const handleContactClick = () => {
  // This would ideally start a conversation about a generic topic,
  // for now, we just navigate to the inbox.
  router.push({ name: 'Inbox' });
};

// --- Lifecycle Hooks ---
onMounted(async () => {
  try {
    const response = await api.getUserDetails(craftsmanId);
    craftsman.value = response.data;
  } catch (error) {
    console.error("Failed to fetch craftsman details:", error);
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="container">
    <div v-if="loading" class="loading-state">Lade Profil...</div>
    <div v-else-if="craftsman" class="profile-layout">

      <!-- Left Column (Sticky Identity Card) -->
      <aside class="identity-card-wrapper">
        <div class="identity-card">
          <div class="card-content">
            <img v-if="craftsman.profile_picture" :src="fullImageUrl(craftsman.profile_picture)" class="profile-avatar" />
            <div v-else class="avatar-placeholder"></div>
            <h1>{{ craftsman.company_name || craftsman.username }}</h1>

            <div class="stats-row">
              <span class="icon">★</span>
              <span class="value">{{ craftsman.average_rating?.toFixed(1) || 'Neu' }}</span>
              <span class="count">({{ craftsman.review_count }} Bewertungen)</span>
            </div>

            <div class="divider"></div>

            <div class="verification-badge">
              <span>✓</span> Identität verifiziert
            </div>

            <div class="cta-wrapper">
              <button v-if="isOwnProfile" @click="router.push({ name: 'Profile' })" class="base-button secondary-action">
                Profil bearbeiten
              </button>
              <button v-else @click="handleContactClick" class="base-button primary-action">
                Kontaktieren
              </button>
            </div>
          </div>
        </div>
      </aside>

      <!-- Right Column (Content) -->
      <main class="main-content">
        <section class="about-section">
          <h2>Über {{ craftsman.company_name || craftsman.username }}</h2>
          <p class="bio">{{ craftsman.bio || 'Keine Beschreibung vorhanden.' }}</p>
          <p class="member-since">Mitglied seit {{ memberSince }}</p>
        </section>

        <section v-if="craftsman.reviews && craftsman.reviews.length > 0" class="reviews-section">
          <h2>
            <span class="icon">★</span> {{ craftsman.average_rating?.toFixed(1) || 'Neu' }} ({{ craftsman.review_count }} Bewertungen)
          </h2>
          <div class="reviews-grid">
            <div v-for="review in craftsman.reviews" :key="review.id" class="review-card">
              <div class="review-header">
                <div class="reviewer-info">
                  <img v-if="review.reviewer_avatar" :src="fullImageUrl(review.reviewer_avatar)" class="reviewer-avatar" />
                  <div v-else class="avatar-placeholder small"></div>
                  <div>
                    <div class="reviewer-name">{{ review.reviewer_name }}</div>
                    <div class="review-date">{{ formatReviewDate(review.created_at) }}</div>
                  </div>
                </div>
                <StarRating :modelValue="review.rating" :readonly="true" />
              </div>
              <p class="review-comment">{{ review.comment }}</p>
              <p class="review-job-context">Für: {{ review.job_title }}</p>
            </div>
          </div>
        </section>
      </main>
    </div>
  </div>
</template>

<style scoped>
.profile-layout {
  display: grid;
  grid-template-columns: 1fr;
  gap: 4rem;
  padding: 48px 0;
}
@media (min-width: 1024px) {
  grid-template-columns: 350px 1fr;
}

/* Left Card */
.identity-card-wrapper {
  position: relative;
}
.identity-card {
  position: sticky;
  top: 120px;
  align-self: start;
}
.card-content {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 6px 16px rgba(0,0,0,0.12);
  text-align: center;
}
.profile-avatar, .avatar-placeholder {
  width: 128px;
  height: 128px;
  border-radius: 50%;
  margin: 0 auto 16px;
  object-fit: cover;
  background-color: #f1f1f1;
}
.identity-card h1 {
  font-size: 1.5rem;
  margin: 0;
}
.stats-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  margin-top: 8px;
  font-size: 0.9rem;
}
.stats-row .icon { font-size: 1.2rem; color: #ffc107; }
.stats-row .value { font-weight: 700; }
.stats-row .count { color: var(--color-text-light); }

.divider {
  border-bottom: 1px solid var(--color-border);
  margin: 24px 0;
}
.verification-badge {
  font-weight: 600;
  margin-bottom: 24px;
}
.cta-wrapper button {
  width: 100%;
  padding: 12px;
}

/* Right Content */
.main-content h2 {
  font-size: 1.5rem;
  margin-top: 0;
  margin-bottom: 24px;
  display: flex;
  align-items: center;
  gap: 8px;
}
.bio {
  line-height: 1.7;
}
.member-since {
  color: var(--color-text-light);
  font-size: 0.9rem;
}
.reviews-section {
  margin-top: 48px;
}
.reviews-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: 32px;
}
@media (min-width: 768px) {
  .reviews-grid { grid-template-columns: 1fr 1fr; }
}
.review-card {
  display: flex;
  flex-direction: column;
}
.review-header {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  margin-bottom: 12px;
}
.reviewer-info {
  display: flex;
  align-items: center;
  gap: 12px;
}
.reviewer-avatar, .avatar-placeholder.small {
  width: 48px;
  height: 48px;
  border-radius: 50%;
  object-fit: cover;
  background-color: #f1f1f1;
}
.reviewer-name { font-weight: 600; }
.review-date { font-size: 0.85rem; color: #717171; }
.review-comment {
  line-height: 1.6;
  margin-bottom: 8px;
}
.review-job-context {
  font-size: 0.8rem;
  color: #717171;
  font-style: italic;
}
</style>
