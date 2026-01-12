<script setup>
/**
 * JobCardSkeleton.vue
 *
 * A skeleton loader component specifically designed to mimic the layout of JobCard.vue.
 * Used to display a loading state while job data is being fetched.
 */

// --- Imports ---
import BaseSkeleton from './BaseSkeleton.vue';
</script>

<template>
  <div class="job-card-skeleton">
    <!-- Image Skeleton -->
    <BaseSkeleton height="180px" border-radius="16px" />

    <!-- Info Skeleton -->
    <div class="info-container">
      <BaseSkeleton height="1.2em" width="80%" border-radius="4px" />
      <BaseSkeleton height="0.9em" width="50%" border-radius="4px" />
      <BaseSkeleton height="1em" width="30%" border-radius="4px" style="margin-top: 8px;" />
    </div>
  </div>
</template>

<style scoped>
.job-card-skeleton {
  display: flex;
  flex-direction: column;
  gap: 12px;
}

.info-container {
  display: flex;
  flex-direction: column;
  gap: 8px; /* Spacing between skeleton lines */
}
</style>