<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/api';

/* ==========================================================================
   State & Setup
   ========================================================================== */

const authStore = useAuthStore();
const router = useRouter();

// UI State
const isLoading = ref(false);
const errorMessage = ref('');
const showForm = ref(false);

// Calculator State
const hoursPerWeek = ref(10);
const hourlyRate = 50; // Constant for calculation
const weeksPerMonth = 4.2; // Constant for calculation

// Form State
const profileData = ref({
  company_name: '',
  street_address: '',
  zip_code: '',
  city: '',
  bio: '',
});

/* ==========================================================================
   Computed Properties
   ========================================================================== */

/**
 * Calculates the estimated monthly earnings based on the selected hours per week.
 * Returns a formatted currency string (EUR).
 *
 * @returns {string} Formatted earnings string
 */
const estimatedEarnings = computed(() => {
  const earnings = hoursPerWeek.value * hourlyRate * weeksPerMonth;
  return new Intl.NumberFormat('de-DE', {
    style: 'currency',
    currency: 'EUR',
    maximumFractionDigits: 0,
  }).format(earnings);
});

/* ==========================================================================
   Methods
   ========================================================================== */

/**
 * Initiates the process to become a craftsman.
 * If the user is logged in, shows the form. Otherwise, redirects to registration.
 */
const handleStartClick = () => {
  if (authStore.isLoggedIn) {
    showForm.value = true;
  } else {
    router.push({ name: 'Register' });
  }
};

/**
 * Hides the form and returns to the marketing view.
 */
const handleBackClick = () => {
  showForm.value = false;
};

/**
 * Submits the craftsman profile data.
 * Handles API calls, user store updates, and navigation.
 */
const handleSubmit = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    await api.becomeCraftsman(profileData.value);
    // Refresh user data to update roles/permissions
    await authStore.fetchUser();
    router.push({ name: 'JobMarketplace' });
  } catch (error) {
    // Handle validation errors from the backend
    if (error.response && error.response.data) {
      const errors = error.response.data;
      // Display the first error found
      const firstErrorKey = Object.keys(errors)[0];
      errorMessage.value = `${firstErrorKey}: ${errors[firstErrorKey][0]}`;
    } else {
      // Fallback generic error message
      errorMessage.value = 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.';
    }
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="page-container">
    <Transition name="fade" mode="out-in">

      <!-- Phase 1: Marketing Landing Page -->
      <div v-if="!showForm" class="marketing-view" key="marketing">
        <section class="hero-section">
          <div class="container hero-grid">
            <div class="hero-content">
              <h1 class="hero-headline">Mach dein Handwerk zu Geld.</h1>
              <p class="hero-subline">Finde passende Aufträge in deiner Nähe, ohne Akquise-Stress. Du entscheidest, wann und wo du arbeitest.</p>
              <div class="earnings-calculator">
                <div class="calculator-header">
                  <span class="earnings-amount">{{ estimatedEarnings }}</span>
                  <span class="earnings-label">pro Monat*</span>
                </div>
                <div class="slider-container">
                  <label for="hours">Bei <strong>{{ hoursPerWeek }} Stunden</strong> pro Woche</label>
                  <input type="range" id="hours" min="1" max="40" v-model="hoursPerWeek" class="slider" />
                </div>
                <p class="disclaimer">*Geschätzter Verdienst basierend auf einem Durchschnittsstundensatz von {{ hourlyRate }} €.</p>
              </div>
              <button @click="handleStartClick" class="base-button cta-button">Jetzt loslegen</button>
            </div>
            <div class="hero-visual">
              <img src="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1000&q=80" alt="Handwerker bei der Arbeit" class="hero-image" />
            </div>
          </div>
        </section>
        <section class="benefits-section">
          <div class="container">
            <h2 class="section-title text-center">Warum MyCraft?</h2>
            <div class="benefits-grid">
              <div class="benefit-card"><div class="icon">🛡️</div><h3>Abgesicherte Zahlungen</h3><p>Kein Risiko mehr. Der Kunde zahlt den Betrag sicher ein, und du erhältst dein Geld garantiert nach Abschluss der Arbeit.</p></div>
              <div class="benefit-card"><div class="icon">📅</div><h3>Volle Kontrolle</h3><p>Du bist dein eigener Chef. Wähle nur die Aufträge aus, die zu deinem Zeitplan und deinen Fähigkeiten passen.</p></div>
              <div class="benefit-card"><div class="icon">🔍</div><h3>Geprüfte Kunden</h3><p>Wir verifizieren Auftraggeber, damit du dich sicher fühlen kannst. Bewertungen helfen dir, die besten Kunden zu finden.</p></div>
            </div>
          </div>
        </section>
        <section class="how-it-works-section">
          <div class="container">
            <h2 class="section-title text-center">So einfach geht's</h2>
            <div class="steps-row">
              <div class="step"><span class="step-number">1</span><h4>Profil erstellen</h4><p>Registriere dich und gib an, welche Dienstleistungen du anbietest.</p></div>
              <div class="step-connector"></div>
              <div class="step"><span class="step-number">2</span><h4>Aufträge finden</h4><p>Durchsuche aktuelle Anfragen in deiner Umgebung und bewirb dich.</p></div>
              <div class="step-connector"></div>
              <div class="step"><span class="step-number">3</span><h4>Geld verdienen</h4><p>Erledige den Job und erhalte deine Auszahlung direkt auf dein Konto.</p></div>
            </div>
          </div>
        </section>
      </div>

      <!-- Phase 2: Onboarding Form -->
      <div v-else class="onboarding-view" key="onboarding">
        <div class="form-container">
          <div class="form-wrapper">
            <header class="form-header">
              <button @click="handleBackClick" class="back-link">← Zurück</button>
              <h1>Werde zum Handwerker</h1>
              <p>Vervollständige dein Profil, um Aufträge zu erhalten.</p>
            </header>

            <form @submit.prevent="handleSubmit" class="craftsman-form">
              <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

              <!-- Floating Label Input -->
              <div class="floating-label-group">
                <input id="company" v-model="profileData.company_name" type="text" required placeholder=" " />
                <label for="company">Firmenname</label>
              </div>

              <div class="floating-label-group">
                <input id="address" v-model="profileData.street_address" type="text" required placeholder=" " />
                <label for="address">Straße & Hausnummer</label>
              </div>

              <div class="form-row">
                <div class="floating-label-group">
                  <input id="zip" v-model="profileData.zip_code" type="text" required placeholder=" " />
                  <label for="zip">Postleitzahl</label>
                </div>
                <div class="floating-label-group">
                  <input id="city" v-model="profileData.city" type="text" required placeholder=" " />
                  <label for="city">Stadt</label>
                </div>
              </div>

              <div class="floating-label-group">
                <textarea id="bio" v-model="profileData.bio" rows="4" placeholder=" "></textarea>
                <label for="bio">Kurze Beschreibung</label>
              </div>

              <button type="submit" class="base-button cta-button" :disabled="isLoading">
                {{ isLoading ? 'Wird gespeichert...' : 'Profil abschließen & Handwerker werden' }}
              </button>
            </form>
          </div>
        </div>
      </div>

    </Transition>
  </div>
</template>

<style scoped>
/* --- Transition --- */
.fade-enter-active, .fade-leave-active { transition: opacity 0.3s ease; }
.fade-enter-from, .fade-leave-to { opacity: 0; }

/* --- Marketing View --- */
.hero-section { padding: var(--spacing-xxl) 0; background-color: white; }
.hero-grid { display: grid; grid-template-columns: 1fr; gap: var(--spacing-xl); align-items: center; }
@media (min-width: 992px) { .hero-grid { grid-template-columns: 1fr 1fr; } }
.hero-headline { font-size: 3rem; line-height: 1.1; margin-top: 0; margin-bottom: var(--spacing-md); }
.hero-subline { font-size: 1.2rem; color: var(--color-text-light); margin-bottom: var(--spacing-xl); max-width: 500px; }
.earnings-calculator { border: 1px solid var(--color-border); border-radius: 16px; padding: var(--spacing-lg); box-shadow: 0 6px 16px rgba(0,0,0,0.08); margin-bottom: var(--spacing-xl); max-width: 450px; }
.earnings-amount { font-size: 2.5rem; font-weight: 700; color: var(--color-primary); display: block; }
.slider { width: 100%; cursor: pointer; accent-color: var(--color-primary); }
.hero-visual { height: 500px; border-radius: 24px; overflow: hidden; box-shadow: var(--box-shadow); }
.hero-image { width: 100%; height: 100%; object-fit: cover; }
.benefits-section { padding: var(--spacing-xxl) 0; background-color: var(--color-background); }
.section-title { font-size: 2rem; margin-bottom: var(--spacing-xl); }
.benefits-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(280px, 1fr)); gap: var(--spacing-xl); }
.how-it-works-section { padding: var(--spacing-xxl) 0; background-color: white; }
.steps-row { display: flex; justify-content: space-between; align-items: flex-start; gap: var(--spacing-lg); flex-wrap: wrap; }

/* --- Onboarding Form --- */
.onboarding-view {
  background-color: white;
  min-height: calc(100vh - 80px);
  display: flex;
  justify-content: center;
  align-items: center;
  padding: var(--spacing-xl) 0;
}
.form-container {
  width: 100%;
}
.form-wrapper {
  width: 100%;
  max-width: 550px;
  margin: 0 auto;
  padding: 40px;
}
.form-header {
  margin-bottom: 32px;
  position: relative;
  text-align: left;
}
.form-header h1 {
  font-size: 2rem;
  font-weight: 800;
  margin: 0 0 8px 0;
}
.form-header p {
  color: var(--color-text-light);
  font-size: 1rem;
  margin: 0;
}
.back-link {
  background: none;
  border: none;
  color: var(--color-text);
  cursor: pointer;
  font-weight: 600;
  font-size: 1rem;
  margin-bottom: 24px;
  display: block;
  padding: 0;
}
.craftsman-form {
  display: flex;
  flex-direction: column;
  gap: 16px;
}
.form-row {
  display: grid;
  grid-template-columns: 1fr 1fr;
  gap: 16px;
}

/* --- Floating Label Inputs --- */
.floating-label-group {
  position: relative;
}
.floating-label-group input,
.floating-label-group textarea {
  width: 100%;
  height: 56px;
  padding: 20px 12px 8px 12px;
  font-size: 1rem;
  border: 1px solid #B0B0B0;
  border-radius: 8px;
  transition: border-color 0.2s ease;
}
.floating-label-group textarea {
  height: auto;
  min-height: 120px;
}
.floating-label-group label {
  position: absolute;
  top: 18px;
  left: 12px;
  font-size: 1rem;
  color: #717171;
  pointer-events: none;
  transition: all 0.2s ease;
  transform-origin: top left;
}

/* The Magic: When input is focused or has content */
.floating-label-group input:focus,
.floating-label-group input:not(:placeholder-shown),
.floating-label-group textarea:focus,
.floating-label-group textarea:not(:placeholder-shown) {
  border-width: 2px;
  border-color: var(--color-text);
  padding-top: 26px;
  padding-bottom: 2px;
}

.floating-label-group input:focus + label,
.floating-label-group input:not(:placeholder-shown) + label,
.floating-label-group textarea:focus + label,
.floating-label-group textarea:not(:placeholder-shown) + label {
  transform: translateY(-10px) scale(0.75);
  color: var(--color-text);
}

/* --- Button & Error --- */
.cta-button {
  width: 100%;
  height: 56px;
  padding: 16px;
  font-size: 1.1rem;
  margin-top: 16px;
  transition: transform 0.1s ease;
}
.cta-button:hover {
  transform: scale(1.01);
}
.error-message {
  background-color: #fff0f0;
  color: var(--color-error);
  padding: 12px;
  border-radius: 8px;
  text-align: center;
}
</style>
