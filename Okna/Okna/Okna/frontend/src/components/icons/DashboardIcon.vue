<template>
  <svg
    xmlns="http://www.w3.org/2000/svg"
    viewBox="0 0 24 24"
    fill="currentColor"
    class="icon"
  >
    <path d="M11 3v8H3V3h8zm10 0v8h-8V3h8zm-10 10v8H3v-8h8zm10 0v8h-8v-8h8z"/>
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
