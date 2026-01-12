<script setup>
/**
 * BaseSkeleton.vue
 *
 * A reusable skeleton loader component to display placeholders while content is loading.
 */

// --- Props ---

/**
 * Props definition.
 * @property {string} width - The width of the skeleton element (default: '100%').
 * @property {string} height - The height of the skeleton element (default: '1em').
 * @property {string} borderRadius - The border radius of the skeleton element (default: '4px').
 */
defineProps({
  width: {
    type: String,
    default: '100%'
  },
  height: {
    type: String,
    default: '1em'
  },
  borderRadius: {
    type: String,
    default: '4px'
  }
});
</script>

<template>
  <div
    class="skeleton"
    :style="{ width, height, borderRadius }"
  ></div>
</template>

<style scoped>
.skeleton {
  background-color: #e0e0e0;
  animation: pulse 1.5s infinite ease-in-out;
}

@keyframes pulse {
  0% {
    opacity: 0.6;
  }
  50% {
    opacity: 1;
  }
  100% {
    opacity: 0.6;
  }
}
</style>