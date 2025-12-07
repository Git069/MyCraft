<script setup>
import { useRouter } from 'vue-router';

const router = useRouter();

const goToJobs = () => {
  router.push({ name: 'JobMarketplace' });
};

const goToRegister = () => {
  router.push({ name: 'Register' });
};
</script>

<template>
  <div class="home-container">
    <header class="hero-section text-center">
      <div class="hero-content">
        <h1 class="hero-title">Finde die besten Handwerker. Oder die besten Aufträge.</h1>
        <p class="hero-subtitle">MyCraft verbindet talentierte Handwerker mit den passenden Projekten in deiner Nähe.</p>
        <div class="hero-actions">
          <button @click="goToJobs" class="base-button primary-action">Jobs finden</button>
          <button @click="goToRegister" class="base-button secondary-action">Jetzt registrieren</button>
        </div>
      </div>
    </header>

    <!-- You can add more sections here later, e.g., "How it works" or "Featured Artisans" -->
  </div>
</template>

<style scoped>
.home-container {
  width: 100%;
}

.hero-section {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: var(--spacing-xxl) var(--spacing-md);
  background-color: var(--color-background);
  border-bottom: 1px solid var(--color-border);
  min-height: 60vh;
}

.hero-content {
  max-width: 800px;
}

.hero-title {
  font-size: 3.5rem;
  line-height: 1.1;
  margin-top: 0;
  margin-bottom: var(--spacing-lg);
  color: var(--color-text);
}

.hero-subtitle {
  font-size: var(--font-size-lg);
  color: var(--color-text-light);
  margin-bottom: var(--spacing-xl);
}

.hero-actions {
  display: flex;
  justify-content: center;
  gap: var(--spacing-md);
}

.primary-action {
  background-color: var(--color-primary);
}
.primary-action:hover {
  background-color: var(--color-primary-dark);
}

.secondary-action {
  background-color: var(--color-surface);
  color: var(--color-primary);
  border: 1px solid var(--color-primary);
}
.secondary-action:hover {
  background-color: #f0f4ff; /* A very light blue */
}
</style>
