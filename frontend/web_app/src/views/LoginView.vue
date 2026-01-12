<script setup>
// --- Imports ---
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/auth';
import { useToastStore } from '@/stores/toast';

// --- Setup ---
const router = useRouter();
const route = useRoute();
const authStore = useAuthStore();
const toastStore = useToastStore();

// --- State ---
const email = ref('');
const password = ref('');
const isLoading = ref(false);

// --- Methods ---

/**
 * Handles the login process.
 * Calls the auth store to login and redirects to the dashboard on success.
 */
const handleLogin = async () => {
  isLoading.value = true;
  try {
    await authStore.login({
      username: email.value,
      password: password.value,
    });

    // Always redirect to Home, regardless of user type
    router.push({ name: 'Home' });
  } catch (error) {
    toastStore.addToast('Anmeldedaten sind ungültig. Bitte versuchen Sie es erneut.', 'error');
  } finally {
    isLoading.value = false;
  }
};

// --- Lifecycle Hooks ---
onMounted(() => {
  if (route.query.registered === 'true') {
    toastStore.addToast('Registrierung erfolgreich! Bitte melde dich an.', 'success');
  }
});
</script>

<template>
  <div class="login-container">
    <div class="login-form-wrapper">
      <header class="form-header text-center">
        <h1>Willkommen zurück!</h1>
        <p>Melde dich an, um deine Projekte zu verwalten.</p>
      </header>

      <form @submit.prevent="handleLogin" class="login-form">
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
.login-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}
.login-button {
  width: 100%;
  margin-top: var(--spacing-sm);
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
