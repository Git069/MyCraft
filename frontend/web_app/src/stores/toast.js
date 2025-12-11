import { defineStore } from 'pinia';
import { ref } from 'vue';

export const useToastStore = defineStore('toast', () => {
  const toasts = ref([]);

  /**
   * Adds a new toast message.
   * @param {string} message - The text to display.
   * @param {string} type - 'success', 'error', 'info', 'warning'. Default: 'info'.
   * @param {number} duration - Duration in ms. Default: 3000.
   */
  const addToast = (message, type = 'info', duration = 3000) => {
    const id = Date.now();
    toasts.value.push({ id, message, type });

    setTimeout(() => {
      removeToast(id);
    }, duration);
  };

  const removeToast = (id) => {
    toasts.value = toasts.value.filter(t => t.id !== id);
  };

  return { toasts, addToast, removeToast };
});
