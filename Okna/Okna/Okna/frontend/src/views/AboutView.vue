<script setup lang="ts">
import CounterDisplay from '@/components/CounterDisplay.vue'
</script>

<template>
  <div class="about">
    <h1>About Page</h1>
    <CounterDisplay />
  </div>
</template>

<style scoped>
.about {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
