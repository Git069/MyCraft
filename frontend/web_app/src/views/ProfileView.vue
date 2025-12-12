<script setup>
import { ref, computed } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useRouter } from 'vue-router';
import api from '@/api';

const authStore = useAuthStore();
const router = useRouter();
const user = computed(() => authStore.currentUser);

const isEditMode = ref(false);
const editableUser = ref({});
const errorMessage = ref('');
const successMessage = ref('');
const fileInput = ref(null);

const toggleEditMode = () => {
  if (!isEditMode.value) {
    editableUser.value = { ...user.value };
  }
  isEditMode.value = !isEditMode.value;
  errorMessage.value = '';
  successMessage.value = '';
};

const handleProfileUpdate = async () => {
  errorMessage.value = '';
  successMessage.value = '';
  try {
    await api.updateUser(editableUser.value);
    await authStore.fetchUser();
    successMessage.value = 'Profil erfolgreich aktualisiert!';
    isEditMode.value = false;
  } catch (error) {
    errorMessage.value = 'Fehler beim Aktualisieren des Profils.';
  }
};

const triggerFileInput = () => {
  fileInput.value.click();
};

const handlePictureUpload = async (event) => {
  const file = event.target.files[0];
  if (!file) return;
  const formData = new FormData();
  formData.append('profile_picture', file);
  try {
    await api.uploadProfilePicture(formData);
    await authStore.fetchUser();
    successMessage.value = 'Profilbild erfolgreich hochgeladen!';
  } catch (error) {
    errorMessage.value = 'Fehler beim Hochladen des Bildes.';
  }
};

const fullImageUrl = computed(() => {
  if (user.value?.profile_picture) {
    return `http://localhost:8000${user.value.profile_picture}`;
  }
  return null;
});
</script>

<template>
  <div class="container profile-container">
    <header class="profile-header">
      <h1>Dein Profil</h1>
      <router-link v-if="user?.is_craftsman" :to="{ name: 'CraftsmanProfile', params: { id: user.id } }" class="base-button secondary-action">
        Öffentliches Profil ansehen
      </router-link>
    </header>

    <div v-if="user" class="profile-card">
      <div v-if="!isEditMode" class="profile-view">
        <div class="avatar-section">
          <img v-if="fullImageUrl" :src="fullImageUrl" alt="Profile Picture" class="avatar-large" />
          <div v-else class="avatar-placeholder-large"></div>
          <button @click="triggerFileInput" class="edit-picture-btn">Bild ändern</button>
          <input type="file" ref="fileInput" @change="handlePictureUpload" style="display: none;" accept="image/*" />
        </div>
        <div class="details-section">
          <p><strong>Benutzername:</strong> {{ user.username }}</p>
          <p><strong>E-Mail:</strong> {{ user.email }}</p>
          <p v-if="user.is_craftsman"><strong>Status:</strong> Handwerker</p>
          <button @click="toggleEditMode" class="base-button">Profil bearbeiten</button>
        </div>
      </div>

      <div v-else class="profile-edit">
        <form @submit.prevent="handleProfileUpdate">
          <div class="form-group">
            <label for="username">Benutzername</label>
            <input id="username" v-model="editableUser.username" type="text" />
          </div>
          <div class="form-group">
            <label for="email">E-Mail</label>
            <input id="email" v-model="editableUser.email" type="email" />
          </div>

          <div v-if="errorMessage" class="error-message">{{ errorMessage }}</div>
          <div v-if="successMessage" class="success-message">{{ successMessage }}</div>

          <div class="edit-actions">
            <button type="button" @click="toggleEditMode" class="base-button secondary-action">Abbrechen</button>
            <button type="submit" class="base-button primary-action">Speichern</button>
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<style scoped>
.profile-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1rem;
}
.profile-header h1 {
  margin: 0;
}
.profile-card {
  background: white;
  padding: var(--spacing-xl);
  border-radius: 12px;
  box-shadow: var(--box-shadow);
}
.profile-view {
  display: flex;
  gap: var(--spacing-xl);
  align-items: flex-start;
}
.avatar-section {
  text-align: center;
}
.avatar-placeholder-large, .avatar-large {
  width: 120px;
  height: 120px;
  border-radius: 50%;
  background-color: #f1f1f1;
  margin-bottom: var(--spacing-md);
  object-fit: cover;
}
.edit-picture-btn {
  background: none;
  border: none;
  color: var(--color-primary);
  cursor: pointer;
  font-weight: 600;
}
.details-section p {
  font-size: 1.1rem;
  margin-bottom: var(--spacing-md);
}
.edit-actions {
  display: flex;
  gap: var(--spacing-sm);
  margin-top: var(--spacing-lg);
}
</style>
