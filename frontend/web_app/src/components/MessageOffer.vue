<script setup>
import { computed } from 'vue';
import { useAuthStore } from '@/stores/auth';

const props = defineProps({
  offer: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['accept', 'reject']);

const authStore = useAuthStore();
const currentUser = computed(() => authStore.currentUser);

const isClient = computed(() => {
  // The client is the one who did NOT create the offer
  return currentUser.value?.id !== props.offer.creator;
});

const formatPrice = (price) => {
  return new Intl.NumberFormat('de-DE', { style: 'currency', currency: 'EUR' }).format(price);
};
</script>

<template>
  <div class="offer-bubble">
    <div class="offer-header">
      <span class="offer-title">Verbindliches Angebot</span>
      <span class="offer-price">{{ formatPrice(offer.price) }}</span>
    </div>
    <p v-if="offer.description" class="offer-description">{{ offer.description }}</p>

    <div class="offer-footer">
      <!-- PENDING STATE -->
      <div v-if="offer.status === 'PENDING'">
        <div v-if="isClient" class="action-buttons">
          <button class="base-button secondary-action" @click="$emit('reject', offer.id)">Ablehnen</button>
          <button class="base-button primary-action" @click="$emit('accept', offer.id)">Annehmen</button>
        </div>
        <div v-else class="pending-status">
          Warte auf Antwort...
        </div>
      </div>

      <!-- ACCEPTED STATE -->
      <div v-if="offer.status === 'ACCEPTED'" class="status-badge accepted">
        ✓ Angebot angenommen
      </div>

      <!-- REJECTED STATE -->
      <div v-if="offer.status === 'REJECTED'" class="status-badge rejected">
        ✗ Angebot abgelehnt
      </div>
    </div>
  </div>
</template>

<style scoped>
.offer-bubble {
  border: 1px solid var(--color-border);
  border-radius: 12px;
  padding: 16px;
  background-color: #f8f9fa;
  max-width: 400px;
  margin: 8px 0;
}
.offer-header {
  display: flex;
  justify-content: space-between;
  align-items: baseline;
  border-bottom: 1px solid var(--color-border);
  padding-bottom: 8px;
  margin-bottom: 12px;
}
.offer-title {
  font-weight: 600;
}
.offer-price {
  font-size: 1.2rem;
  font-weight: 700;
  color: var(--color-primary);
}
.offer-description {
  font-size: 0.9rem;
  color: var(--color-text-light);
  margin-bottom: 16px;
}
.offer-footer {
  margin-top: 16px;
}
.action-buttons {
  display: flex;
  gap: 8px;
  justify-content: flex-end;
}
.primary-action {
  background-color: var(--color-success);
}
.secondary-action {
  background-color: #e0e0e0;
  color: var(--color-text);
}
.pending-status {
  font-style: italic;
  color: var(--color-text-light);
  text-align: center;
}
.status-badge {
  text-align: center;
  font-weight: 600;
  padding: 8px;
  border-radius: 8px;
}
.status-badge.accepted {
  color: var(--color-success);
  background-color: #f0fff4;
}
.status-badge.rejected {
  color: var(--color-error);
  background-color: #fff0f0;
}
</style>
