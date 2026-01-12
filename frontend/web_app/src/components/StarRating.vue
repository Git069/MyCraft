<script setup>
/**
 * StarRating.vue
 *
 * A reusable star rating component.
 * Supports both interactive rating selection and read-only display.
 */

// --- Imports ---
import { ref, watch } from 'vue';

// --- Props & Emits ---

/**
 * Props definition.
 * @property {number} modelValue - The current rating value (v-model).
 * @property {boolean} readonly - Whether the rating is read-only (default: false).
 */
const props = defineProps({
  modelValue: { type: Number, default: 0 },
  readonly: { type: Boolean, default: false }
});

/**
 * Emits definition.
 * @emits update:modelValue - Emitted when the rating changes.
 */
const emit = defineEmits(['update:modelValue']);

// --- Reactive State ---

/** @type {import('vue').Ref<number>} Internal rating state */
const rating = ref(props.modelValue);

/** @type {import('vue').Ref<number>} Temporary rating state on hover */
const hoverRating = ref(0);

// --- Watchers ---

/**
 * Sync internal state with prop changes.
 */
watch(() => props.modelValue, (newValue) => {
  rating.value = newValue;
});

// --- Methods ---

/**
 * Sets the rating and emits the update event.
 * @param {number} value - The selected rating (1-5).
 */
const setRating = (value) => {
  if (props.readonly) return;
  rating.value = value;
  emit('update:modelValue', value);
};

/**
 * Sets the temporary hover rating.
 * @param {number} value - The star being hovered over.
 */
const setHoverRating = (value) => {
  if (props.readonly) return;
  hoverRating.value = value;
};
</script>

<template>
  <div class="star-rating" @mouseleave="setHoverRating(0)">
    <span
      v-for="star in 5"
      :key="star"
      class="star"
      :class="{
        'filled': star <= (hoverRating || rating),
        'readonly': readonly
      }"
      @mouseover="setHoverRating(star)"
      @click="setRating(star)"
    >
      ★
    </span>
  </div>
</template>

<style scoped>
.star-rating {
  display: inline-flex;
  gap: 4px;
}
.star {
  font-size: 2rem;
  color: #d1d1d1; /* Empty star color */
  cursor: pointer;
  transition: color 0.2s;
}
.star.filled {
  color: #ffc107; /* Filled star color */
}
.star.readonly {
  cursor: default;
}
</style>