import { defineStore } from 'pinia';
import { ref } from 'vue';

/* ==========================================================================
   Toast Store
   ========================================================================== */

/**
 * Pinia store for managing toast notifications.
 * Allows adding and removing temporary alert messages.
 */
export const useToastStore = defineStore('toast', () => {
  const toasts = ref([]);

  /**
   * Removes a toast message by its ID.
   *
   * @param {number} id - The unique ID of the toast to remove.
   */
  const removeToast = (id) => {
    toasts.value = toasts.value.filter((t) => t.id !== id);
  };

  /**
   * Adds a new toast message to the queue.
   * Automatically removes the toast after the specified duration.
   *
   * @param {string} message - The text to display in the toast.
   * @param {string} [type='info'] - The type of toast ('success', 'error', 'info', 'warning').
   * @param {number} [duration=3000] - The duration in milliseconds before the toast disappears.
   */
  const addToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now();
    toasts.value.push({ id, message, type });

    setTimeout(() => {
      removeToast(id);
    }, duration);
  };

  return { toasts, addToast, removeToast };
});
