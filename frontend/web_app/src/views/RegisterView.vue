<script setup>
import { ref } from 'vue';
import { useRouter } from 'vue-router';
import api from '@/api';
import { useToastStore } from '@/stores/toast';

const router = useRouter();
const toastStore = useToastStore();

const email = ref('');
const password = ref('');
const password2 = ref('');
const isLoading = ref(false);

const handleRegister = async () => {
  if (password.value !== password2.value) {
    toastStore.addToast('Die Passwörter stimmen nicht überein.', 'error');
    return;
  }

  isLoading.value = true;
  try {
    await api.register({
      username: email.value,
      email: email.value,
      password: password.value,
      re_password: password2.value,
    });
    router.push({ name: 'Login', query: { registered: 'true' } });
  } catch (error) {
    if (error.response && error.response.data) {
      const errors = error.response.data;
      const firstErrorKey = Object.keys(errors)[0];
      const errorMessage = errors[firstErrorKey][0];
      toastStore.addToast(errorMessage, 'error');
    } else {
      toastStore.addToast('Ein unbekannter Fehler ist aufgetreten.', 'error');
    }
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
/* Styles are simplified as error messages are removed */
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
.register-form {
  display: flex;
  flex-direction: column;
  gap: var(--spacing-md);
}
.register-button {
  width: 100%;
  margin-top: var(--spacing-sm);
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
