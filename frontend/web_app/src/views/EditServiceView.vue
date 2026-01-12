<script setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { useToastStore } from '@/stores/toast';
import api from '@/api';

/* ==========================================================================
   State & Setup
   ========================================================================== */

const route = useRoute();
const router = useRouter();
const toastStore = useToastStore();

const service = ref(null);
const loading = ref(true);
const isSaving = ref(false);
const serviceId = route.params.id;

/* ==========================================================================
   Lifecycle Hooks
   ========================================================================== */

/**
 * Fetches the service details when the component is mounted.
 * Redirects to dashboard if loading fails.
 */
onMounted(async () => {
  try {
    const response = await api.getServiceDetails(serviceId);
    service.value = response.data;
  } catch (error) {
    toastStore.addToast('Inserat konnte nicht geladen werden.', 'error');
    router.push({ name: 'Dashboard' });
  } finally {
    loading.value = false;
  }
});

/* ==========================================================================
   Methods
   ========================================================================== */

/**
 * Updates the service details via the API.
 * Redirects to the dashboard upon success or displays an error toast on failure.
 */
const handleUpdate = async () => {
  isSaving.value = true;
  try {
    await api.updateService(serviceId, service.value);
    toastStore.addToast('Inserat erfolgreich aktualisiert.', 'success');
    router.push({ name: 'Dashboard' });
  } catch (error) {
    toastStore.addToast('Fehler beim Speichern.', 'error');
  } finally {
    isSaving.value = false;
  }
};
</script>

<template>
  <div class="container">
    <div v-if="loading">Lade Inserat...</div>
    <div v-else-if="service" class="form-wrapper">
      <h1>Inserat bearbeiten</h1>
      <form @submit.prevent="handleUpdate">
        <div class="form-group">
          <label for="title">Titel</label>
          <input id="title" v-model="service.title" type="text" />
        </div>
        <div class="form-group">
          <label for="description">Beschreibung</label>
          <textarea id="description" v-model="service.description" rows="5"></textarea>
        </div>
        <div class="form-group">
          <label for="price">Preis (€)</label>
          <input id="price" v-model="service.price" type="number" step="0.01" />
        </div>
        <div class="form-actions">
          <router-link :to="{ name: 'Dashboard' }" class="base-button secondary-action">Abbrechen</router-link>
          <button type="submit" class="base-button" :disabled="isSaving">
            {{ isSaving ? 'Speichere...' : 'Änderungen speichern' }}
          </button>
        </div>
      </form>
    </div>
    <div v-else>
      <p>Inserat nicht gefunden.</p>
    </div>
  </div>
</template>

<style scoped>
.form-wrapper {
  max-width: 700px;
  margin: 40px auto;
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: var(--box-shadow);
}

.form-group {
  margin-bottom: 16px;
}

.form-group label {
  display: block;
  margin-bottom: 8px;
  font-weight: 600;
}

.form-group input, .form-group textarea {
  width: 100%;
  padding: 12px;
  border: 1px solid #ccc;
  border-radius: 8px;
}

.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 24px;
}

.secondary-action {
  background-color: #f1f1f1;
  color: var(--color-text);
}
</style>
