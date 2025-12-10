<script setup>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';

const email = ref('');
const password = ref('');
const errorMessage = ref('');
const successMessage = ref('');
const isLoading = ref(false);

const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();

onMounted(() => {
  if (route.query.registered === 'true') {
    successMessage.value = 'Registrierung erfolgreich! Bitte melde dich an.';
  }
});

const handleLogin = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  isLoading.value = true;

  if (!email.value || !password.value) {
    errorMessage.value = 'Bitte füllen Sie beide Felder aus.';
    isLoading.value = false;
    return;
  }

  try {
    // Call the login action from the auth store
    await authStore.login({
      username: email.value,
      password: password.value,
    });

    // Redirect on success
    router.push({ name: 'JobMarketplace' });

  } catch (error) {
    // The store action throws an error on failure, which we catch here
    if (error.response && error.response.status === 400) {
      errorMessage.value = 'Anmeldedaten sind ungültig. Bitte versuchen Sie es erneut.';
    } else {
      errorMessage.value = 'Ein Server-Fehler ist aufgetreten. Bitte versuchen Sie es später erneut.';
    }
    console.error('Login failed:', error);
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <header class="form-header text-center">
        <h1>Willkommen zurück!</h1>
        <p>Melde dich an, um deine Projekte zu verwalten.</p>
      </header>

      <form @submit.prevent="handleLogin" class="login-form">
        <div v-if="successMessage" class="success-message">
          {{ successMessage }}
        </div>
        <div v-if="errorMessage" class="error-message">
          {{ errorMessage }}
        </div>

        <div class="form-group">
          <label for="email">E-Mail-Adresse</label>
          <input
            id="email"
            v-model="email"
            type="email"
            placeholder="deine.email@beispiel.com"
            required
          />
        </div>

        <div class="form-group">
          <label for="password">Passwort</label>
          <input
            id="password"
            v-model="password"
            type="password"
            placeholder="Dein sicheres Passwort"
            required
          />
        </div>

        <button type="submit" class="base-button login-button" :disabled="isLoading">
          {{ isLoading ? 'Melde an...' : 'Anmelden' }}
        </button>
      </form>

      <footer class="form-footer">
        <a href="#" class="forgot-password-link">Passwort vergessen?</a>
        <p>
          Noch kein Konto?
          <router-link to="/register" class="register-link">Jetzt registrieren</router-link>
        </p>
      </footer>
    </div>
  </div>
</template>

<style scoped>
/* Styles remain the same */
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  min-height: 80vh;
  padding: var(--spacing-lg);
}

.login-form-wrapper {
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

.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}

.login-button {
  width: 100%;
  background-color: var(--color-primary);
  padding-top: var(--spacing-sm);
  padding-bottom: var(--spacing-sm);
}
.login-button:hover {
  background-color: var(--color-primary-dark);
}

.error-message, .success-message {
  color: var(--color-text-inverted);
  padding: var(--spacing-sm) var(--spacing-md);
  border-radius: var(--border-radius);
  text-align: center;
}
.error-message {
  background-color: var(--color-error);
}
.success-message {
  background-color: var(--color-success);
}

.form-footer {
  margin-top: var(--spacing-xl);
  text-align: center;
  font-size: var(--font-size-sm);
}

.forgot-password-link {
  display: block;
  margin-bottom: var(--spacing-md);
  color: var(--color-text-light);
}

.register-link {
  font-weight: 600;
  color: var(--color-primary);
}
</style>
