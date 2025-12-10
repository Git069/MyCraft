<script setup>
import { ref, computed } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const router = useRouter();
const isLoading = ref(false);

// --- Earnings Calculator Logic ---
const hoursPerWeek = ref(10);
const hourlyRate = 50; // Realistic average hourly rate
const weeksPerMonth = 4.2;

const estimatedEarnings = computed(() => {
  const earnings = hoursPerWeek.value * hourlyRate * weeksPerMonth;
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR', maximumFractionDigits: 0 }).format(earnings);
});

const handleCtaClick = async () => {
  // If user is already logged in, start the process to become a craftsman
  if (authStore.isLoggedIn) {
    isLoading.value = true;
    try {
      await authStore.becomeCraftsman();
      // Redirect to a relevant page for new craftsmen
      router.push({ name: 'JobMarketplace' });
    } catch (error) {
      console.error('Failed to become a craftsman:', error);
      // Optionally, show an error message here
    } finally {
      isLoading.value = false;
    }
  } else {
    // If user is not logged in, redirect to the registration page
    router.push({ name: 'Register' });
  }
};
</script>

<template>
  <div class="landing-page">

    <!-- 1. HERO SECTION -->
    <section class="hero-section">
      <div class="container hero-grid">
        <!-- Left: Content & Calculator -->
        <div class="hero-content">
          <h1 class="hero-headline">Mach dein Handwerk zu Geld.</h1>
          <p class="hero-subline">Finde passende Aufträge in deiner Nähe, ohne Akquise-Stress. Du entscheidest, wann und wo du arbeitest.</p>

          <!-- Earnings Calculator -->
          <div class="earnings-calculator">
            <div class="calculator-header">
              <span class="earnings-amount">{{ estimatedEarnings }}</span>
              <span class="earnings-label">pro Monat*</span>
            </div>
            <div class="slider-container">
              <label for="hours">Bei <strong>{{ hoursPerWeek }} Stunden</strong> pro Woche</label>
              <input
                type="range"
                id="hours"
                min="1"
                max="40"
                v-model="hoursPerWeek"
                class="slider"
              />
            </div>
            <p class="disclaimer">*Geschätzter Verdienst basierend auf einem Durchschnittsstundensatz von {{ hourlyRate }} €.</p>
          </div>

          <button @click="handleCtaClick" class="base-button cta-button" :disabled="isLoading">
            {{ isLoading ? 'Wird eingerichtet...' : 'Jetzt loslegen' }}
          </button>
        </div>

        <!-- Right: Visual -->
        <div class="hero-visual">
          <img src="https://images.unsplash.com/photo-1621905251189-08b45d6a269e?auto=format&fit=crop&w=1000&q=80" alt="Handwerker bei der Arbeit" class="hero-image" />
        </div>
      </div>
    </section>

    <!-- 2. BENEFITS SECTION -->
    <section class="benefits-section">
      <div class="container">
        <h2 class="section-title text-center">Warum MyCraft?</h2>
        <div class="benefits-grid">
          <div class="benefit-card">
            <div class="icon">🛡️</div>
            <h3>Abgesicherte Zahlungen</h3>
            <p>Kein Risiko mehr. Der Kunde zahlt den Betrag sicher ein, und du erhältst dein Geld garantiert nach Abschluss der Arbeit.</p>
          </div>
          <div class="benefit-card">
            <div class="icon">📅</div>
            <h3>Volle Kontrolle</h3>
            <p>Du bist dein eigener Chef. Wähle nur die Aufträge aus, die zu deinem Zeitplan und deinen Fähigkeiten passen.</p>
          </div>
          <div class="benefit-card">
            <div class="icon">🔍</div>
            <h3>Geprüfte Kunden</h3>
            <p>Wir verifizieren Auftraggeber, damit du dich sicher fühlen kannst. Bewertungen helfen dir, die besten Kunden zu finden.</p>
          </div>
        </div>
      </div>
    </section>

    <!-- 3. HOW IT WORKS SECTION -->
    <section class="how-it-works-section">
      <div class="container">
        <h2 class="section-title text-center">So einfach geht's</h2>
        <div class="steps-row">
          <div class="step">
            <span class="step-number">1</span>
            <h4>Profil erstellen</h4>
            <p>Registriere dich und gib an, welche Dienstleistungen du anbietest.</p>
          </div>
          <div class="step-connector"></div>
          <div class="step">
            <span class="step-number">2</span>
            <h4>Aufträge finden</h4>
            <p>Durchsuche aktuelle Anfragen in deiner Umgebung und bewirb dich.</p>
          </div>
          <div class="step-connector"></div>
          <div class="step">
            <span class="step-number">3</span>
            <h4>Geld verdienen</h4>
            <p>Erledige den Job und erhalte deine Auszahlung direkt auf dein Konto.</p>
          </div>
        </div>
      </div>
    </section>

  </div>
</template>

<style scoped>
.landing-page {
  width: 100%;
}

/* --- 1. HERO SECTION --- */
.hero-section {
  padding: var(--spacing-xxl) 0;
  background-color: white;
}
.hero-grid {
  display: grid;
  grid-template-columns: 1fr;
  gap: var(--spacing-xl);
  align-items: center;
}
@media (min-width: 992px) {
  .hero-grid {
    grid-template-columns: 1fr 1fr;
  }
}
.hero-headline {
  font-size: 3rem;
  line-height: 1.1;
  margin-top: 0;
  margin-bottom: var(--spacing-md);
}
.hero-subline {
  font-size: 1.2rem;
  color: var(--color-text-light);
  margin-bottom: var(--spacing-xl);
  max-width: 500px;
}

/* Calculator */
.earnings-calculator {
  background-color: white;
  border: 1px solid var(--color-border);
  border-radius: 16px;
  padding: var(--spacing-lg);
  box-shadow: 0 6px 16px rgba(0,0,0,0.08);
  margin-bottom: var(--spacing-xl);
  max-width: 450px;
}
.calculator-header {
  margin-bottom: var(--spacing-md);
}
.earnings-amount {
  font-size: 2.5rem;
  font-weight: 700;
  color: var(--color-primary);
  display: block;
}
.earnings-label {
  font-size: 1rem;
  font-weight: 600;
}
.slider-container {
  margin-bottom: var(--spacing-sm);
}
.slider-container label {
  display: block;
  margin-bottom: var(--spacing-sm);
  font-size: 1rem;
}
.slider {
  width: 100%;
  cursor: pointer;
  accent-color: var(--color-primary); /* CRITICAL: This styles the slider thumb and track */
}
.disclaimer {
  font-size: 0.8rem;
  color: var(--color-text-light);
  margin: 0;
}

.cta-button {
  width: 100%;
  max-width: 450px;
  padding: 16px;
  font-size: 1.1rem;
  background-color: var(--color-primary);
}
.cta-button:hover {
  background-color: var(--color-primary-dark);
}

.hero-visual {
  height: 500px;
  border-radius: 24px;
  overflow: hidden;
  box-shadow: var(--box-shadow);
}
.hero-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}

/* --- 2. BENEFITS SECTION --- */
.benefits-section {
  padding: var(--spacing-xxl) 0;
  background-color: var(--color-background);
}
.section-title {
  font-size: 2rem;
  margin-bottom: var(--spacing-xl);
}
.benefits-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: var(--spacing-xl);
}
.benefit-card {
  padding: var(--spacing-lg);
}
.benefit-card .icon {
  font-size: 2.5rem;
  margin-bottom: var(--spacing-md);
}
.benefit-card h3 {
  font-size: 1.2rem;
  margin-bottom: var(--spacing-sm);
}
.benefit-card p {
  color: var(--color-text-light);
  line-height: 1.6;
}

/* --- 3. HOW IT WORKS SECTION --- */
.how-it-works-section {
  padding: var(--spacing-xxl) 0;
  background-color: white;
}
.steps-row {
  display: flex;
  justify-content: space-between;
  align-items: flex-start;
  gap: var(--spacing-lg);
  flex-wrap: wrap;
}
.step {
  flex: 1;
  min-width: 200px;
  text-align: center;
}
.step-number {
  display: inline-block;
  width: 40px;
  height: 40px;
  line-height: 40px;
  border-radius: 50%;
  background-color: var(--color-text);
  color: white;
  font-weight: 700;
  margin-bottom: var(--spacing-md);
}
.step h4 {
  font-size: 1.2rem;
  margin-bottom: var(--spacing-sm);
}
.step p {
  color: var(--color-text-light);
}
.step-connector {
  flex: 1;
  height: 1px;
  background-color: var(--color-border);
  margin-top: 20px;
  display: none;
}
@media (min-width: 768px) {
  .step-connector {
    display: block;
  }
}
</style>
