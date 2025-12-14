<script setup>
import { computed } from 'vue';

const props = defineProps({
  src: { type: String, default: null },
  name: { type: String, default: '' },
  size: { type: [String, Number], default: 40 }
});

const initials = computed(() => {
  if (!props.name) return '??';
  const parts = props.name.split(' ');
  if (parts.length > 1) {
    return (parts[0][0] + parts[parts.length - 1][0]).toUpperCase();
  }
  return props.name.substring(0, 2).toUpperCase();
});

const avatarStyle = computed(() => ({
  width: `${props.size}px`,
  height: `${props.size}px`,
  fontSize: `${props.size * 0.4}px` // Scale font size with avatar size
}));
</script>

<template>
  <div class="avatar-wrapper" :style="avatarStyle">
    <img v-if="src" :src="src" :alt="name" class="avatar-image" />
    <div v-else-if="name" class="avatar-initials">
      {{ initials }}
    </div>
    <div v-else class="avatar-placeholder">
      <svg viewBox="0 0 32 32" fill="currentColor"><path d="m16 .7c-8.437 0-15.3 6.863-15.3 15.3 0 8.437 6.863 15.3 15.3 15.3 8.437 0 15.3-6.863 15.3-15.3 0-8.437-6.863-15.3-15.3-15.3zm0 28c-4.021 0-7.605-1.884-9.933-4.81a12.425 12.425 0 0 1 6.451-4.4 6.507 6.507 0 0 1 -3.018-5.49c0-3.584 2.916-6.5 6.5-6.5s6.5 2.916 6.5 6.5a6.513 6.513 0 0 1 -3.019 5.491 12.42 12.42 0 0 1 6.452 4.4c-2.328 2.925-5.912 4.809-9.933 4.809z"></path></svg>
    </div>
  </div>
</template>

<style scoped>
.avatar-wrapper {
  border-radius: 50%;
  overflow: hidden;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}
.avatar-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
}
.avatar-initials {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: var(--color-text);
  color: white;
  font-weight: 600;
}
.avatar-placeholder {
  width: 100%;
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #e0e0e0;
  color: #717171;
}
</style>
