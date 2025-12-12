<script setup>
import { ref } from 'vue';
import StarRating from './StarRating.vue';

const props = defineProps({
  job: { type: Object, required: true },
  isOpen: { type: Boolean, required: true }
});

const emit = defineEmits(['close', 'submit']);

const rating = ref(0);
const comment = ref('');
const isSubmitting = ref(false);

const handleSubmit = () => {
  if (rating.value === 0) return; // Validation
  isSubmitting.value = true;
  emit('submit', {
    job: props.job.id,
    rating: rating.value,
    comment: comment.value
  });
  // Reset after emit, parent handles closing
  isSubmitting.value = false;
};

const handleClose = () => {
  emit('close');
  // Reset fields
  rating.value = 0;
  comment.value = '';
};
</script>

<template>
  <div v-if="isOpen" class="modal-overlay" @click.self="handleClose">
    <div class="modal-card">
      <header class="modal-header">
        <h3>Bewertung abgeben</h3>
        <button class="close-btn" @click="handleClose">×</button>
      </header>

      <div class="modal-body">
        <p class="intro-text">Wie zufrieden warst du mit der Arbeit bei <strong>{{ job.title }}</strong>?</p>

        <div class="rating-wrapper">
          <StarRating v-model="rating" />
        </div>

        <div class="form-group">
          <label for="comment">Dein Kommentar (Optional)</label>
          <textarea
            id="comment"
            v-model="comment"
            rows="4"
            placeholder="Was hat dir besonders gut gefallen?"
          ></textarea>
        </div>
      </div>

      <footer class="modal-footer">
        <button class="base-button secondary-action" @click="handleClose">Abbrechen</button>
        <button
          class="base-button primary-action"
          @click="handleSubmit"
          :disabled="rating === 0 || isSubmitting"
        >
          {{ isSubmitting ? 'Sende...' : 'Bewertung senden' }}
        </button>
      </footer>
    </div>
  </div>
</template>

<style scoped>
.modal-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background-color: rgba(0,0,0,0.5);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 2000; /* High z-index to be on top of everything */
}

.modal-card {
  background: white;
  width: 90%;
  max-width: 500px;
  border-radius: 12px;
  box-shadow: 0 8px 24px rgba(0,0,0,0.2);
  overflow: hidden;
  display: flex;
  flex-direction: column;
}

.modal-header {
  padding: 20px 24px;
  border-bottom: 1px solid var(--color-border);
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.modal-header h3 { margin: 0; font-size: 1.2rem; }
.close-btn { background: none; border: none; font-size: 1.5rem; cursor: pointer; color: var(--color-text-light); }

.modal-body {
  padding: 24px;
}
.intro-text { margin-bottom: 16px; color: var(--color-text); }
.rating-wrapper { margin-bottom: 24px; text-align: center; }

.form-group label { display: block; margin-bottom: 8px; font-weight: 600; font-size: 0.9rem; }
.form-group textarea { width: 100%; padding: 12px; border: 1px solid #ccc; border-radius: 8px; font-family: inherit; resize: vertical; }

.modal-footer {
  padding: 16px 24px;
  border-top: 1px solid var(--color-border);
  display: flex;
  justify-content: flex-end;
  gap: 12px;
  background-color: #fcfcfc;
}

.secondary-action { background-color: #f1f1f1; color: var(--color-text); }
.primary-action:disabled { opacity: 0.6; cursor: not-allowed; }
</style>
