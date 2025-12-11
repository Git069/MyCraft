<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import api from '@/api';

const authStore = useAuthStore();
const router = useRouter();
const isLoading = ref(false);
const errorMessage = ref('');

const profileData = ref({
  company_name: '',
  street_address: '',
  zip_code: '',
  city: '',
  bio: '',
});

const handleBecomeCraftsman = async () => {
  isLoading.value = true;
  errorMessage.value = '';
  try {
    await api.becomeCraftsman(profileData.value);
    // Refresh user data to get the new status
    await authStore.fetchUser();
    router.push({ name: 'JobMarketplace' });
  } catch (error) {
    if (error.response && error.response.data) {
      const errors = error.response.data;
      const firstErrorKey = Object.keys(errors)[0];
      errorMessage.value = `${firstErrorKey}: ${errors[firstErrorKey][0]}`;
    } else {
      errorMessage.value = 'Ein Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.';
    }
    console.error('Failed to become a craftsman:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="form-container">
    <div class="form-wrapper">
      <header class="form-header text-center">
        <h1>Werde zum Handwerker</h1>
        <p>Vervollständige dein Profil, um Aufträge zu erhalten.</p>
      </header>

      <form @submit.prevent="handleBecomeCraftsman" class="craftsman-form">
        <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>

        <div class="form-group">
          <label for="company">Firmenname</label>
          <input id="company" v-model="profileData.company_name" type="text" required />
        </div>

        <div class="form-group">
          <label for="address">Straße & Hausnummer</label>
          <input id="address" v-model="profileData.street_address" type="text" required />
        </div>

        <div class="form-row">
          <div class="form-group">
            <label for="zip">Postleitzahl</label>
            <input id="zip" v-model="profileData.zip_code" type="text" required />
          </div>
          <div class="form-group">
            <label for="city">Stadt</label>
            <input id="city" v-model="profileData.city" type="text" required />
          </div>
        </div>

        <div class="form-group">
          <label for="bio">Kurze Beschreibung über dich/dein Unternehmen</label>
          <textarea id="bio" v-model="profileData.bio" rows="4"></textarea>
        </div>

        <button type="submit" class="base-button cta-button" :disabled="isLoading">
          {{ isLoading ? 'Wird gespeichert...' : 'Profil abschließen & Handwerker werden' }}
        </button>
      </form>
    </div>
  </div>
</template>

<style scoped>
.form-container {
  display: flex;
  justify-content: center;
  padding: var(--spacing-xl) var(--spacing-md);
  background-color: var(--color-background);
}
.form-wrapper {
  width: 100%;
  max-width: 600px;
  padding: var(--spacing-xl);
  background-color: white;
  border-radius: 12px;
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
.craftsman-form {
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
.cta-button {
  width: 100%;
  padding: 16px;
  font-size: 1.1rem;
  margin-top: var(--spacing-md);
}
.error-message {
  background-color: #fff0f0;
  color: var(--color-error);
  padding: 12px;
  border-radius: 8px;
  text-align: center;
}
</style>
