<script setup lang="ts">
defineProps<{
  variant?: 'primary' | 'secondary'
}>()
</script>

<template>
  <button :class="['button', variant]">
    <slot />
  </button>
</template>

<style scoped>
.button {
  padding: 0.5rem 1rem;
}
.primary {
  background: blue;
}
.secondary {
  background: gray;
}
</style>
