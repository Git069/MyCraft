<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';

const email = ref('');
const password = ref('');
const password2 = ref('');
const errorMessage = ref('');
const isLoading = ref(false);

const router = useRouter();

const handleRegister = async () => {
  errorMessage.value = '';
  isLoading.value = true;

  if (!email.value || !password.value || !password2.value) {
    errorMessage.value = 'Bitte füllen Sie alle Felder aus.';
    isLoading.value = false;
    return;
  }
  if (password.value !== password2.value) {
    errorMessage.value = 'Die Passwörter stimmen nicht überein.';
    isLoading.value = false;
    return;
  }

  try {
    // --- API Call: Add re_password to the payload ---
    await api.register({
      username: email.value,
      email: email.value,
      password: password.value,
      re_password: password2.value, // This is what Djoser expects
    });

    router.push({ name: 'Login', query: { registered: 'true' } });

  } catch (error) {
    if (error.response && error.response.data) {
      const errors = error.response.data;
      const firstErrorKey = Object.keys(errors)[0];
      if (firstErrorKey === 'username') {
        errorMessage.value = 'Ein Benutzer mit dieser E-Mail-Adresse existiert bereits.';
      } else if (firstErrorKey === 'password' || firstErrorKey === 're_password') {
        errorMessage.value = `Passwort-Fehler: ${errors[firstErrorKey][0]}`;
      } else {
        errorMessage.value = `${firstErrorKey}: ${errors[firstErrorKey][0]}`;
      }
    } else {
      errorMessage.value = 'Ein unbekannter Fehler ist aufgetreten.';
    }
    console.error('Registration failed:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="register-container">
    <div class="register-form-wrapper">
      <header class="form-header text-center">
        <h1>Konto erstellen</h1>
        <p>Werde Teil der MyCraft-Community.</p>
      </header>

      <form @submit.prevent="handleRegister" class="register-form">
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label for="email">E-Mail-Adresse</label>
          <input id="email" v-model="email" type="email" required />
        </div>

        <div class="form-group">
          <label for="password">Passwort</label>
          <input id="password" v-model="password" type="password" required />
        </div>

        <div class="form-group">
          <label for="password2">Passwort bestätigen</label>
          <input id="password2" v-model="password2" type="password" required />
        </div>

        <button type="submit" class="base-button register-button" :disabled="isLoading">
          {{ isLoading ? 'Registriere...' : 'Konto erstellen' }}
        </button>
      </form>

      <footer class="form-footer">
        <p>
          Du hast bereits ein Konto?
          <router-link to="/login" class="login-link">Jetzt anmelden</router-link>
        </p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
/* Styles remain the same */
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: var(--spacing-lg);
}

.register-form-wrapper {
  width: 100%;
  max-width: 450px;
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

.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.register-button {
  width: 100%;
  background-color: var(--color-primary);
  padding-top: var(--spacing-sm);
  padding-bottom: var(--spacing-sm);
}
.register-button:hover {
  background-color: var(--color-primary-dark);
}

.error-message {
  background-color: var(--color-error);
  color: var(--color-text-inverted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  text-align: center;
}

.form-footer {
  margin-top: var(--spacing-xl);
  text-align: center;
  font-size: var(--font-size-sm);
}

.login-link {
  font-weight: 600;
  color: var(--color-primary);
}
</style>
