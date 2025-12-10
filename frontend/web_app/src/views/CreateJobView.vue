<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const router = useRouter();

// Form data for the new job
const jobData = ref({
  title: '',
  description: '',
  trade: 'OTHER', // Default value
  zip_code: '',
  city: '',
  price: null,
});

const errorMessage = ref('');
const isLoading = ref(false);

// Trade options for the select dropdown
const tradeOptions = [
  { value: 'PLUMBER', text: 'Sanitär & Heizung' },
  { value: 'ELECTRICIAN', text: 'Elektrik' },
  { value: 'PAINTER', text: 'Maler & Lackierer' },
  { value: 'CARPENTER', text: 'Tischler & Schreiner' },
  { value: 'GARDENER', text: 'Garten & Landschaftsbau' },
  { value: 'OTHER', text: 'Sonstiges' },
];

const handleCreateJob = async () => {
  errorMessage.value = '';
  isLoading.value = true;

  try {
    // The API service will automatically send the auth token
    const response = await api.createJob(jobData.value);

    // On success, redirect to the marketplace
    // In the future, you might redirect to the new job's detail page
    router.push({ name: 'JobMarketplace' });

  } catch (error) {
    if (error.response && error.response.data) {
      const errors = error.response.data;
      const firstErrorKey = Object.keys(errors)[0];
      errorMessage.value = `${firstErrorKey}: ${errors[firstErrorKey][0]}`;
    } else {
      errorMessage.value = 'Ein unbekannter Fehler ist aufgetreten.';
    }
    console.error('Job creation failed:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="create-job-container">
    <div class="form-wrapper">
      <header class="form-header text-center">
        <h1>Neuen Auftrag erstellen</h1>
        <p>Beschreibe dein Projekt, um passende Angebote zu erhalten.</p>
      </header>

      <form @submit.prevent="handleCreateJob" class="create-job-form">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label for="title">Titel des Auftrags</label>
          <input id="title" v-model="jobData.title" type="text" required placeholder="z.B. Badezimmer renovieren" />
        </div>

        <div class="form-group">
          <label for="description">Beschreibung</label>
          <textarea id="description" v-model="jobData.description" rows="5" required placeholder="Beschreibe die Arbeit so detailliert wie möglich..."></textarea>
        </div>

        <div class="form-group">
          <label for="trade">Gewerk</label>
          <select id="trade" v-model="jobData.trade">
            <option v-for="option in tradeOptions" :key="option.value" :value="option.value">
              {{ option.text }}
            </option>
          </select>
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="zip_code">Postleitzahl</label>
            <input id="zip_code" v-model="jobData.zip_code" type="text" required pattern="[0-9]{5}" />
          </div>
          <div class="form-group">
            <label for="city">Stadt</label>
            <input id="city" v-model="jobData.city" type="text" required />
          </div>
        </div>

        <div class="form-group">
          <label for="price">Preisvorstellung (€, optional)</label>
          <input id="price" v-model="jobData.price" type="number" step="0.01" placeholder="z.B. 500.00" />
        </div>

        <button type="submit" class="base-button submit-button" :disabled="isLoading">
          {{ isLoading ? 'Erstelle...' : 'Auftrag veröffentlichen' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.create-job-container {
  display: flex;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-md);
}

.form-wrapper {
  width: 100%;
  max-width: 700px; /* Wider form for more content */
  padding: var(--spacing-xl);
  background-color: var(--color-surface);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
}

.form-header {
  margin-bottom: var(--spacing-lg);
}
.form-header h1 {
  margin-top: 0;
}
.form-header p {
  color: var(--color-text-light);
}

.create-job-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.form-row {
  display: flex;
  gap: var(--spacing-md);
}
.form-row .form-group {
  flex: 1;
}

/* Make textarea styles consistent with input */
textarea {
  width: 100%;
  padding: var(--spacing-sm) var(--spacing-md);
  border: 1px solid var(--color-border);
  border-radius: var(--border-radius);
  font: inherit;
  transition: border-color var(--transition-speed), box-shadow var(--transition-speed);
}
textarea:focus {
  border-color: var(--color-primary);
  outline: 0;
  box-shadow: 0 0 0 0.2rem rgba(77, 107, 221, 0.25);
}

.submit-button {
  width: 100%;
  background-color: var(--color-primary);
  padding-top: var(--spacing-sm);
  padding-bottom: var(--spacing-sm);
  margin-top: var(--spacing-md);
}
.submit-button:hover {
  background-color: var(--color-primary-dark);
}

.error-message {
  background-color: var(--color-error);
  color: var(--color-text-inverted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  text-align: center;
}
</style>
