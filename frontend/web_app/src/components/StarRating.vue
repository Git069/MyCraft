<script setup>
import { ref, watch } from 'vue';

const props = defineProps({
  modelValue: { type: Number, default: 0 },
  readonly: { type: Boolean, default: false }
});

const emit = defineEmits(['update:modelValue']);

const rating = ref(props.modelValue);
const hoverRating = ref(0);

watch(() => props.modelValue, (newValue) => {
  rating.value = newValue;
});

const setRating = (value) => {
  if (props.readonly) return;
  rating.value = value;
  emit('update:modelValue', value);
};

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
