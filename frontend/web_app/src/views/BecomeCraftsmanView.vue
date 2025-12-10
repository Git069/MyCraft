<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const authStore = useAuthStore();
const router = useRouter();
const isLoading = ref(false);
const errorMessage = ref('');

const handleBecomeCraftsman = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    await authStore.becomeCraftsman();
    // Redirect to a page that is relevant for craftsmen, e.g., create job
    router.push({ name: 'CreateJob' });
  } catch (error) {
    errorMessage.value = 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.';
    console.error('Failed to become a craftsman:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="become-craftsman-container">
    <div class="form-wrapper">
      <header class="form-header text-center">
        <h1>Werde zum Handwerker</h1>
        <p>Schalte die Möglichkeit frei, Aufträge zu erstellen und dein Handwerk anzubieten.</p>
      </header>

      <div class="confirmation-text">
        <p>
          Als Handwerker kannst du deine Dienstleistungen auf unserer Plattform anbieten,
          detaillierte Aufträge erstellen und dich mit potenziellen Kunden vernetzen.
        </p>
        <p>
          Bist du bereit, dein Können zu zeigen?
        </p>
      </div>

      <div v-if="errorMessage" class="error-message">
        {{ errorMessage }}
      </div>

      <button @click="handleBecomeCraftsman" class="base-button submit-button" :disabled="isLoading">
        {{ isLoading ? 'Wird bearbeitet...' : 'Ja, ich bin ein Handwerker' }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.become-craftsman-container {
  display: flex;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-md);
}

.form-wrapper {
  width: 100%;
  max-width: 600px;
  padding: var(--spacing-xl);
  background-color: var(--color-surface);
  border-radius: var(--border-radius);
  box-shadow: var(--box-shadow);
  text-align: center;
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

.confirmation-text {
  margin-bottom: var(--spacing-xl);
  line-height: 1.7;
}

.submit-button {
  width: 100%;
  background-color: var(--color-accent);
  padding: var(--spacing-sm) var(--spacing-md);
}
.submit-button:hover {
  background-color: #3e8e41;
}

.error-message {
  background-color: var(--color-error);
  color: var(--color-text-inverted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  text-align: center;
  margin-bottom: var(--spacing-md);
}
</style>
