<script setup>
/**
 * ToastContainer.vue
 *
 * A container component that displays toast notifications.
 * Subscribes to the ToastStore to render active toasts with animations.
 */

// --- Imports ---
import { useToastStore } from '@/stores/toast';

// --- Reactive State ---
const toastStore = useToastStore();
</script>

<template>
  <div class="toast-container">
    <TransitionGroup name="list" tag="div">
      <div
        v-for="toast in toastStore.toasts"
        :key="toast.id"
        class="toast"
        :class="`toast-${toast.type}`"
      >
        {{ toast.message }}
      </div>
    </TransitionGroup>
  </div>
</template>

<style scoped>
.toast-container {
  position: fixed;
  bottom: 20px;
  right: 20px;
  z-index: 1000;
  display: flex;
  flex-direction: column;
  gap: 10px;
}

.toast {
  padding: 16px 24px;
  border-radius: 8px;
  color: white;
  font-weight: 600;
  box-shadow: 0 4px 12px rgba(0,0,0,0.15);
  transition: all 0.5s ease;
}

.toast-success {
  background-color: var(--color-success);
}
.toast-error {
  background-color: var(--color-error);
}
.toast-info {
  background-color: var(--color-primary);
}
.toast-warning {
  background-color: var(--color-warning);
  color: var(--color-text);
}

/* --- Transition Animations --- */
.list-enter-active,
.list-leave-active {
  transition: all 0.5s ease;
}
.list-enter-from,
.list-leave-to {
  opacity: 0;
  transform: translateX(30px);
}
</style>