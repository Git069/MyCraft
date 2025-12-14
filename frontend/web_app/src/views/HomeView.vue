<script setup>
import { ref, onMounted } from 'vue';
import api from '@/api';
import JobSearch from '@/components/JobSearch.vue';
import JobCard from '@/components/JobCard.vue';

const recentServices = ref([]);
const loading = ref(true);

const fetchRecentServices = async () => {
  loading.value = true;
  try {
    const response = await api.getServices({ page_size: 8 });
    recentServices.value = response.data.results;
  } catch (error) {
    console.error("Failed to fetch recent services:", error);
  } finally {
    loading.value = false;
  }
};

onMounted(fetchRecentServices);
</script>

<template>
  <div class="home-view">
    <header class="hero-section text-center">
      <div class="container">
        <h1 class="hero-title">Finde die besten Handwerker. Oder die besten Aufträge.</h1>
        <p class="hero-subtitle">MyCraft verbindet talentierte Handwerker mit den passenden Projekten in deiner Nähe.</p>
        <JobSearch />
      </div>
    </header>

    <section class="recent-jobs-section">
      <div class="container">
        <h2 class="section-title">Aktuelle Angebote in deiner Umgebung</h2>
        <div v-if="loading" class="loading-state">Lade Angebote...</div>
        <div v-else class="jobs-grid">
          <JobCard
            v-for="service in recentServices"
            :key="service.id"
            :job="service"
          />
        </div>
      </div>
    </section>

    <section class="how-it-works-section">
      <div class="container text-center">
        <h2 class="section-title">So einfach funktioniert's</h2>
        <div class="steps-grid">
          <div class="step-card">
            <div class="step-icon">1</div>
            <h3 class="step-title">Konto erstellen</h3>
            <p>Registriere dich kostenlos als Auftraggeber oder Handwerker.</p>
          </div>
          <div class="step-card">
            <div class="step-icon">2</div>
            <h3 class="step-title">Auftrag finden oder erstellen</h3>
            <p>Durchsuche den Marktplatz oder stelle dein eigenes Projekt online.</p>
          </div>
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
.hero-section { padding: var(--spacing-xxl) 0; background-color: var(--color-surface); border-bottom: 1px solid var(--color-border); }
.hero-title { font-size: 3.5rem; line-height: 1.1; margin-top: 0; margin-bottom: var(--spacing-lg); max-width: 800px; margin-left: auto; margin-right: auto; }
.hero-subtitle { font-size: var(--font-size-lg); color: var(--color-text-light); margin-bottom: var(--spacing-xl); max-width: 650px; margin-left: auto; margin-right: auto; }
.recent-jobs-section { padding: var(--spacing-xxl) 0; }
.section-title { font-size: 2rem; font-weight: 700; margin-top: 0; margin-bottom: var(--spacing-xl); text-align: left; }
.jobs-grid { display: grid; gap: 24px; grid-template-columns: repeat(1, 1fr); }
@media (min-width: 768px) { .jobs-grid { grid-template-columns: repeat(2, 1fr); } }
@media (min-width: 1024px) { .jobs-grid { grid-template-columns: repeat(4, 1fr); } }
.how-it-works-section { padding: var(--spacing-xxl) 0; background-color: var(--color-surface); border-top: 1px solid var(--color-border); }
.steps-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: var(--spacing-xl); }
.step-card { padding: var(--spacing-lg); }
.step-icon { width: 60px; height: 60px; margin: 0 auto var(--spacing-lg); border-radius: 50%; background-color: var(--color-primary); color: var(--color-text-inverted); display: flex; align-items: center; justify-content: center; font-size: 2rem; font-weight: bold; }
.step-title { font-size: 1.5rem; margin-bottom: var(--spacing-sm); }
</style>
