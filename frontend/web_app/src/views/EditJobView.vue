<script setup>
// --- Imports ---
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import api from '@/api';
import { useToastStore } from '@/stores/toast';

// --- Setup ---
const route = useRoute();
const router = useRouter();
const toastStore = useToastStore();

// --- State ---
const job = ref(null);
const loading = ref(true);
const isSaving = ref(false);
const jobId = route.params.id;

// --- Methods ---

/**
 * Updates the job details via the API.
 * Redirects to the dashboard upon success.
 */
const handleUpdate = async () => {
  isSaving.value = true;
  try {
    await api.updateJob(jobId, job.value);
    toastStore.addToast("Auftrag erfolgreich aktualisiert.", "success");
    router.push({ name: 'Dashboard' });
  } catch (error) {
    toastStore.addToast("Fehler beim Speichern.", "error");
  } finally {
    isSaving.value = false;
  }
};

// --- Lifecycle Hooks ---
onMounted(async () => {
  try {
    const response = await api.getJobDetails(jobId);
    job.value = response.data;
  } catch (error) {
    toastStore.addToast("Auftrag konnte nicht geladen werden.", "error");
  } finally {
    loading.value = false;
  }
});
</script>

<template>
  <div class="container">
    <div v-if="loading">Lade...</div>
    <div v-else-if="job" class="form-wrapper">
      <h1>Auftrag bearbeiten</h1>
      <form @submit.prevent="handleUpdate">
        <div class="form-group">
          <label for="title">Titel</label>
          <input id="title" v-model="job.title" type="text" />
        </div>
        <div class="form-group">
          <label for="description">Beschreibung</label>
          <textarea id="description" v-model="job.description" rows="5"></textarea>
        </div>
        <div class="form-group">
          <label for="price">Preis (€)</label>
          <input id="price" v-model="job.price" type="number" step="0.01" />
        </div>
        <div class="form-actions">
          <router-link :to="{ name: 'Dashboard' }" class="base-button secondary-action">Abbrechen</router-link>
          <button type="submit" class="base-button" :disabled="isSaving">
            {{ isSaving ? 'Speichere...' : 'Änderungen speichern' }}
          </button>
        </div>
      </form>
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
}
.form-group {
  margin-bottom: 16px;
}
.form-actions {
  display: flex;
  justify-content: flex-end;
  gap: 8px;
  margin-top: 24px;
}
</style>
