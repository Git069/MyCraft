<script setup>
/**
 * EditProfileModal.vue
 *
 * A modal component for editing user profile information.
 * Supports updating text fields (bio, address, etc.) and uploading a profile picture.
 */

// --- Imports ---
import { ref, reactive, onMounted } from 'vue';
import api from '@/api';
import { useToastStore } from '@/stores/toast';

// --- Props & Emits ---

/**
 * Props definition.
 * @property {Object} user - The user object containing current profile data.
 * @property {boolean} isOpen - Whether the modal is currently visible.
 */
const props = defineProps({
  user: {
    type: Object,
    required: true
  },
  isOpen: {
    type: Boolean,
    required: true
  }
});

/**
 * Emits definition.
 * @emits close - Emitted when the modal should be closed.
 * @emits updated - Emitted when the profile has been successfully updated.
 */
const emit = defineEmits(['close', 'updated']);

// --- Reactive State ---

const toast = useToastStore();

/** @type {import('vue').Ref<boolean>} Loading state for form submission */
const isLoading = ref(false);

/** @type {import('vue').Ref<HTMLInputElement|null>} Reference to the hidden file input */
const fileInput = ref(null);

/** @type {import('vue').Ref<File|null>} The selected file for upload */
const selectedFile = ref(null);

/** @type {import('vue').Ref<string|null>} URL for the image preview */
const previewImage = ref(null);

/**
 * Reactive form data object.
 */
const formData = reactive({
  company_name: '',
  bio: '',
  street_address: '',
  city: '',
  zip_code: ''
});

// --- Lifecycle Hooks ---

/**
 * Initialize form data with user props on mount.
 */
onMounted(() => {
  if (props.user) {
    formData.company_name = props.user.company_name || '';
    formData.bio = props.user.bio || '';
    formData.street_address = props.user.street_address || ''; // Comes from updated serializer
    formData.city = props.user.city || '';
    formData.zip_code = props.user.zip_code || '';
  }
});

// --- Methods ---

/**
 * Constructs the full URL for an image path.
 * @param {string} url - The relative image URL.
 * @returns {string|null} The full URL or null.
 */
const fullImageUrl = (url) => url ? `http://localhost:8000${url}` : null;

/**
 * Handles file selection change event.
 * Updates the selected file and generates a preview URL.
 * @param {Event} event - The input change event.
 */
const handleFileChange = (event) => {
  const file = event.target.files[0];
  if (file) {
    selectedFile.value = file;
    previewImage.value = URL.createObjectURL(file);
  }
};

/**
 * Triggers the hidden file input click.
 */
const triggerFileInput = () => {
  fileInput.value.click();
};

/**
 * Submits the form data to the API.
 * Updates text profile data first, then uploads the profile picture if changed.
 */
const submitForm = async () => {
  isLoading.value = true;
  try {
    // 1. Update text data
    await api.updateUserProfile(formData);

    // 2. Update image (if changed)
    if (selectedFile.value) {
      const imageFormData = new FormData();
      imageFormData.append('profile_picture', selectedFile.value);
      await api.uploadProfilePicture(imageFormData);
    }

    toast.addToast('Profil gespeichert!', 'success');
    emit('updated');
    emit('close');
  } catch (error) {
    console.error("Error saving profile:", error);
    toast.addToast('Fehler beim Speichern.', 'error');
  } finally {
    isLoading.value = false;
  }
};
</script>

<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="$emit('close')">
    <div class="modal-content">
      <header class="modal-header">
        <h3>Profil bearbeiten</h3>
        <button class="close-btn" @click="$emit('close')">&times;</button>
      </header>

      <div class="modal-body">

        <div class="avatar-section">
          <div class="avatar-wrapper" @click="triggerFileInput">
            <img v-if="previewImage" :src="previewImage" class="avatar-img" />
            <img v-else-if="user.profile_picture" :src="fullImageUrl(user.profile_picture)" class="avatar-img" />
            <div v-else class="avatar-placeholder">{{ user.username?.[0]?.toUpperCase() }}</div>
            <div class="avatar-overlay">📷</div>
          </div>
          <input type="file" ref="fileInput" @change="handleFileChange" accept="image/*" hidden />
        </div>

        <form @submit.prevent="submitForm" class="edit-form">

          <div v-if="user.is_craftsman" class="form-group">
            <label>Name der Firma</label>
            <input type="text" v-model="formData.company_name" placeholder="Firmenname" />
          </div>

          <div class="form-group">
            <label>Kurzbeschreibung {{ user.is_craftsman ? 'der Firma' : '(Bio)' }}</label>
            <textarea v-model="formData.bio" rows="4" placeholder="Beschreibe dein Angebot oder dich selbst..."></textarea>
          </div>

          <div class="form-group">
            <label>Adresse (Straße & Hausnummer)</label>
            <input type="text" v-model="formData.street_address" placeholder="Musterstraße 123" />
          </div>

          <div class="form-group">
            <label>Stadt</label>
            <input type="text" v-model="formData.city" placeholder="Musterstadt" />
          </div>

          <div class="form-group">
            <label>Postleitzahl</label>
            <input type="text" v-model="formData.zip_code" placeholder="12345" />
          </div>

        </form>
      </div>

      <footer class="modal-footer">
        <button class="base-button secondary" @click="$emit('close')">Abbrechen</button>
        <button class="base-button primary" @click="submitForm" :disabled="isLoading">
          {{ isLoading ? 'Speichern...' : 'Speichern' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed; inset: 0; background: rgba(0,0,0,0.5);
  display: flex; justify-content: center; align-items: center; z-index: 1000;
}
.modal-content {
  background: white; width: 90%; max-width: 500px; border-radius: 12px;
  display: flex; flex-direction: column; max-height: 90vh;
}
.modal-header {
  padding: 16px 24px; border-bottom: 1px solid #eee; display: flex; justify-content: space-between; align-items: center;
}
.modal-body { padding: 24px; overflow-y: auto; }
.modal-footer {
  padding: 16px 24px; border-top: 1px solid #eee; display: flex; justify-content: flex-end; gap: 12px;
}

/* Avatar Styles */
.avatar-section { display: flex; justify-content: center; margin-bottom: 24px; }
.avatar-wrapper {
  width: 100px; height: 100px; border-radius: 50%; overflow: hidden; position: relative; cursor: pointer; background: #f0f0f0; border: 2px solid #fff; box-shadow: 0 2px 8px rgba(0,0,0,0.1);
}
.avatar-img { width: 100%; height: 100%; object-fit: cover; }
.avatar-placeholder { width: 100%; height: 100%; display: flex; align-items: center; justify-content: center; font-size: 2.5rem; color: #aaa; font-weight: bold; }
.avatar-overlay {
  position: absolute; inset: 0; background: rgba(0,0,0,0.4); display: flex; align-items: center; justify-content: center;
  opacity: 0; transition: opacity 0.2s; color: white; font-size: 1.5rem;
}
.avatar-wrapper:hover .avatar-overlay { opacity: 1; }

/* Form Styles */
.form-group { margin-bottom: 20px; }
.form-group label { display: block; margin-bottom: 8px; font-weight: 600; font-size: 0.9rem; color: #333; }
.form-group input, .form-group textarea {
  width: 100%; padding: 12px; border: 1px solid #ddd; border-radius: 8px; font-family: inherit; font-size: 0.95rem; transition: border-color 0.2s;
}
.form-group input:focus, .form-group textarea:focus { outline: none; border-color: #000; }

.close-btn { background: none; border: none; font-size: 1.8rem; cursor: pointer; color: #666; }

/* Buttons */
.base-button { padding: 12px 24px; border-radius: 8px; cursor: pointer; border: none; font-weight: 600; font-size: 0.95rem; transition: opacity 0.2s; }
.base-button:hover { opacity: 0.9; }
.base-button.primary { background-color: #000; color: white; }
.base-button.secondary { background-color: #f5f5f5; color: #333; }
</style>