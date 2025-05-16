<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    class="icon"
  >
    <path d="M12 5.5c1.1 0 2-.9 2-2s-.9-2-2-2-2 .9-2 2 .9 2 2 2zM16 17v-2c0-1.1-.9-2-2-2h-4c-1.1 0-2 .9-2 2v2h8zm4-9h-2.5v2.5h-7V8H8v8h1.5v-2.5h7V16H20V8z"/>
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
