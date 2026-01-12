<script setup>
import { ref, onMounted, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import StarRating from '@/components/StarRating.vue';
import UserAvatar from '@/components/UserAvatar.vue';
import EditProfileModal from '@/components/EditProfileModal.vue';
import api from '@/api';

/* ==========================================================================
   State & Setup
   ========================================================================== */

const authStore = useAuthStore();

const loading = ref(true);
const showEditModal = ref(false);
const fullUserProfile = ref(null);

/* ==========================================================================
   Computed Properties
   ========================================================================== */

/**
 * Retrieves the currently logged-in user from the store.
 * @returns {Object|null} The user object.
 */
const user = computed(() => authStore.currentUser);

/**
 * Extracts the year the user joined the platform.
 * @returns {number|string} The year of joining or an empty string if not available.
 */
const memberSince = computed(() => {
  if (!fullUserProfile.value?.date_joined) return '';
  return new Date(fullUserProfile.value.date_joined).getFullYear();
});

/* ==========================================================================
   Lifecycle Hooks
   ========================================================================== */

/**
 * Fetches the user profile when the component is mounted.
 */
onMounted(() => {
  fetchUserProfile();
});

/* ==========================================================================
   Methods
   ========================================================================== */

/**
 * Fetches the full user profile details from the API.
 * Updates the fullUserProfile state.
 */
const fetchUserProfile = async () => {
  if (user.value) {
    loading.value = true;
    try {
      const response = await api.getUserDetails(user.value.id);
      fullUserProfile.value = response.data;
    } catch (error) {
      console.error('Failed to fetch full user profile:', error);
    } finally {
      loading.value = false;
    }
  }
};

/**
 * Callback function to handle profile updates.
 * Refetches the user profile to display the latest data.
 */
const handleProfileUpdate = () => {
  fetchUserProfile();
};

/**
 * Constructs the full URL for an image path.
 * @param {string} url - The relative image URL.
 * @returns {string|null} The full URL or null if url is missing.
 */
const fullImageUrl = (url) => (url ? `http://localhost:8000${url}` : null);

/**
 * Formats a date string into a localized month and year string.
 * @param {string} dateString - The date string to format.
 * @returns {string} Formatted date string (e.g., "January 2023").
 */
const formatReviewDate = (dateString) => {
  const date = new Date(dateString);
  return date.toLocaleDateString('de-DE', { month: 'long', year: 'numeric' });
};
</script>

<template>
  <div class="container">

    <EditProfileModal
      v-if="fullUserProfile"
      :isOpen="showEditModal"
      :user="fullUserProfile"
      @close="showEditModal = false"
      @updated="handleProfileUpdate"
    />

    <div v-if="loading" class="loading-state">Lade Profil...</div>
    <div v-else-if="fullUserProfile" class="profile-layout">

      <aside class="identity-card-wrapper">
        <div class="identity-card">
          <div class="card-content">
            <UserAvatar :src="fullImageUrl(fullUserProfile.profile_picture)" :name="fullUserProfile.username" :size="128" />
            <h1>{{ fullUserProfile.company_name || fullUserProfile.username }}</h1>

            <div v-if="fullUserProfile.is_craftsman" class="stats-row">
              <span class="icon">★</span>
              <span class="value">{{ fullUserProfile.average_rating?.toFixed(1) || 'Neu' }}</span>
              <span class="count">({{ fullUserProfile.review_count }} Bewertungen)</span>
            </div>

            <div class="divider"></div>

            <div class="verification-badge">
              <span>✓</span> Identität verifiziert
            </div>

            <div class="cta-wrapper">
              <button class="base-button primary-action" @click="showEditModal = true">
                Profil bearbeiten
              </button>
            </div>
          </div>
        </div>
      </aside>

      <main class="main-content">
        <section class="about-section">
          <h2>Über mich</h2>
          <p class="bio">{{ fullUserProfile.bio || 'Keine Beschreibung vorhanden. Bearbeite dein Profil, um mehr über dich zu erzählen.' }}</p>

          <p v-if="fullUserProfile.city" class="location">📍 {{ fullUserProfile.city }}</p>

          <p class="member-since">Mitglied seit {{ memberSince }}</p>
        </section>

        <section v-if="fullUserProfile.is_craftsman && fullUserProfile.reviews && fullUserProfile.reviews.length > 0" class="reviews-section">
          <h2>
            <span class="icon">★</span> {{ fullUserProfile.average_rating?.toFixed(1) || 'Neu' }} ({{ fullUserProfile.review_count }} Bewertungen)
          </h2>
          <div class="reviews-grid">
            <div v-for="review in fullUserProfile.reviews" :key="review.id" class="review-card">
              <div class="review-header">
                <div class="reviewer-info">
                  <UserAvatar :src="fullImageUrl(review.reviewer_avatar)" :name="review.reviewer_name" :size="48" />
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
/* Reusing styles from CraftsmanProfileView */
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
  box-shadow: 0 6px 16px rgba(0, 0, 0, 0.12);
  text-align: center;
}

.identity-card h1 {
  font-size: 1.5rem;
  margin: 16px 0 8px 0;
}

.stats-row {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 8px;
  font-size: 0.9rem;
}

.stats-row .icon {
  font-size: 1.2rem;
  color: #ffc107;
}

.stats-row .value {
  font-weight: 700;
}

.stats-row .count {
  color: var(--color-text-light);
}

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
  margin-top: 8px;
}

.location {
  color: #555;
  font-size: 0.95rem;
  margin: 8px 0;
  display: flex;
  align-items: center;
  gap: 4px;
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
  .reviews-grid {
    grid-template-columns: 1fr 1fr;
  }
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

.reviewer-name {
  font-weight: 600;
}

.review-date {
  font-size: 0.85rem;
  color: #717171;
}

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
