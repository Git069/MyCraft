<script setup>
// No script logic needed for this static view, but keeping the setup for future use.
</script>

<template>
  <div class="home-view">
    <!-- HERO SECTION -->
    <header class="hero-section text-center">
      <div class="container">
        <h1 class="hero-title">Finde die besten Handwerker. Oder die besten Aufträge.</h1>
        <p class="hero-subtitle">MyCraft verbindet talentierte Handwerker mit den passenden Projekten in deiner Nähe.</p>
        <div class="hero-actions">
          <router-link :to="{ name: 'JobMarketplace' }" class="base-button primary-action">
            Aufträge entdecken
          </router-link>
          <router-link :to="{ name: 'Register' }" class="base-button secondary-action">
            Jetzt registrieren
          </router-link>
        </div>
      </div>
    </header>

    <!-- HOW IT WORKS SECTION -->
    <section class="how-it-works-section">
      <div class="container text-center">
        <h2 class="section-title">So einfach funktioniert's</h2>
        <div class="steps-grid">
          <!-- Step 1 -->
          <div class="step-card">
            <div class="step-icon">1</div>
            <h3 class="step-title">Konto erstellen</h3>
            <p>Registriere dich kostenlos als Auftraggeber oder Handwerker.</p>
          </div>
          <!-- Step 2 -->
          <div class="step-card">
            <div class="step-icon">2</div>
            <h3 class="step-title">Auftrag finden oder erstellen</h3>
            <p>Durchsuche den Marktplatz oder stelle dein eigenes Projekt online.</p>
          </div>
          <!-- Step 3 -->
          <div class="step-card">
            <div class="step-icon">3</div>
            <h3 class="step-title">Verbinden & loslegen</h3>
            <p>Nimm Kontakt auf, kläre die Details und starte dein Projekt.</p>
          </div>
        </div>
      </div>
    </section>
  </div>
</template>

<style scoped>
/* --- HERO SECTION --- */
.hero-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xxl) 0;
  background-color: var(--color-surface);
  border-bottom: 1px solid var(--color-border);
  min-height: 50vh;
}

.hero-title {
  font-size: 3.5rem;
  line-height: 1.1;
  margin-top: 0;
  margin-bottom: var(--spacing-lg);
  color: var(--color-text);
  max-width: 800px;
  margin-left: auto;
  margin-right: auto;
}

.hero-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-light);
  margin-bottom: var(--spacing-xl);
  max-width: 650px;
  margin-left: auto;
  margin-right: auto;
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
  flex-wrap: wrap;
}

.primary-action {
  background-color: var(--color-primary);
  font-size: var(--font-size-lg);
  padding: var(--spacing-md) var(--spacing-xl);
}
.primary-action:hover {
  background-color: var(--color-primary-dark);
}

.secondary-action {
  background-color: transparent;
  color: var(--color-primary);
  border: 2px solid var(--color-primary);
  font-size: var(--font-size-lg);
  padding: var(--spacing-md) var(--spacing-xl);
}
.secondary-action:hover {
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
}

/* --- HOW IT WORKS SECTION --- */
.how-it-works-section {
  padding: var(--spacing-xxl) 0;
  background-color: var(--color-background);
}

.section-title {
  margin-top: 0;
  margin-bottom: var(--spacing-xl);
}

.steps-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: var(--spacing-xl);
}

.step-card {
  padding: var(--spacing-lg);
}

.step-icon {
  width: 60px;
  height: 60px;
  margin: 0 auto var(--spacing-lg);
  border-radius: 50%;
  background-color: var(--color-primary);
  color: var(--color-text-inverted);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2rem;
  font-weight: bold;
  font-family: var(--font-family-heading);
}

.step-title {
  font-size: 1.5rem;
  margin-bottom: var(--spacing-sm);
}

@media (max-width: 768px) {
  .hero-title {
    font-size: 2.5rem;
  }
}
</style>
