<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    class="icon"
  >
    <path d="M17 7l-1.4 1.4 1.6 1.6H9v2h8.2l-1.6 1.6L17 15l4-4-4-4zM5 5h7V3H5c-1.1 0-2 .9-2 2v14c0 1.1.9 2 2 2h7v-2H5V5z"/>
  </svg>
</template>

<script setup lang="ts">
defineProps({
  size: {
    type: [Number, String],
    default: 20
  }
})
</script>

<style scoped>
.icon {
  width: v-bind('typeof size === "number" ? `${size}px` : size');
  height: v-bind('typeof size === "number" ? `${size}px` : size');
}
</style>
