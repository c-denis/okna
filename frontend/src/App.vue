<template>
  <component :is="layout">
    <router-view />
  </component>
</template>

<script setup lang="ts">
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import MainLayout from '@/layouts/MainLayout.vue'
import AuthLayout from '@/layouts/AuthLayout.vue'
import EmptyLayout from '@/layouts/EmptyLayout.vue'

const route = useRoute()

const layout = computed(() => {
  return route.meta.layout || 'main-layout'
})

const layouts: Record<string, any> = {
  'main-layout': MainLayout,
  'auth-layout': AuthLayout,
  'empty-layout': EmptyLayout
}
</script>

<style>
@import '@/assets/styles/base.css';
@import '@/assets/styles/utilities.css';

#app {
  min-height: 100vh;
  display: flex;
  flex-direction: column;
}
</style>
