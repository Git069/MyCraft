<script setup>
/**
 * DetailHighlight.vue
 *
 * A simple component to display a highlighted feature with an icon, title, and subtitle.
 */

// --- Props ---

/**
 * Props definition.
 * @property {string} icon - The icon to display (emoji or character).
 * @property {string} title - The main title text.
 * @property {string} subtitle - The subtitle or description text.
 */
defineProps({
  icon: String,
  title: String,
  subtitle: String,
});
</script>

<template>
  <div class="highlight-item">
    <div class="icon-wrapper">
      <!-- Using emoji as placeholder, can be replaced with SVG -->
      <span v-if="icon">{{ icon }}</span>
    </div>
    <div class="text-group">
      <span class="title">{{ title }}</span>
      <span class="subtitle">{{ subtitle }}</span>
    </div>
  </div>
</template>

<style scoped>
.highlight-item {
  display: flex;
  align-items: center;
  gap: 16px;
}
.icon-wrapper {
  font-size: 1.5rem;
  flex-shrink: 0;
}
.text-group {
  display: flex;
  flex-direction: column;
}
.title {
  font-weight: 600;
  color: var(--color-text);
}
.subtitle {
  font-size: 0.9rem;
  color: var(--color-text-light);
}
</style>