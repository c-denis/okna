<script setup lang="ts">
import CounterDisplay from '@/components/CounterDisplay.vue'
</script>

<template>
  <div class="home">
    <h1>Home Page</h1>
    <CounterDisplay />
  </div>
</template>

<style scoped>
.home {
  max-width: 800px;
  margin: 0 auto;
  padding: 2rem;
}
</style>
