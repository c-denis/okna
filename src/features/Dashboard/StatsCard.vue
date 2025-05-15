<template>
  <div class="stats-card" :class="variant">
    <div class="stats-icon">
      <slot name="icon">
        <div class="default-icon">{{ icon }}</div>
      </slot>
    </div>
    <div class="stats-content">
      <div class="stats-value">{{ value }}</div>
      <div class="stats-title">{{ title }}</div>
      <div v-if="trend !== null" class="stats-trend" :class="trendClass">
        <span v-if="trend > 0">+</span>{{ trend }}%
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { computed } from 'vue';

const props = defineProps({
  title: {
    type: String,
    required: true
  },
  value: {
    type: [String, Number],
    required: true
  },
  icon: {
    type: String,
    default: '📊'
  },
  trend: {
    type: Number,
    default: null
  },
  variant: {
    type: String,
    default: 'primary',
    validator: (value: string) =>
      ['primary', 'secondary', 'success', 'warning', 'danger'].includes(value)
  }
});

const trendClass = computed(() => {
  if (props.trend === null) return '';
  return props.trend >= 0 ? 'positive' : 'negative';
});
</script>

<style scoped>
.stats-card {
  display: flex;
  align-items: center;
  padding: 16px;
  border-radius: 8px;
  background-color: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.stats-icon {
  margin-right: 16px;
  font-size: 1.5rem;
}

.default-icon {
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 50%;
  background-color: #f5f5f5;
}

.stats-content {
  flex: 1;
}

.stats-value {
  font-size: 1.5rem;
  font-weight: 600;
  margin-bottom: 4px;
}

.stats-title {
  color: #666;
  font-size: 0.9rem;
}

.stats-trend {
  font-size: 0.8rem;
  margin-top: 4px;
}

.stats-trend.positive {
  color: #4caf50;
}

.stats-trend.negative {
  color: #f44336;
}

/* Variant styles */
.stats-card.primary .stats-value {
  color: #2196f3;
}

.stats-card.secondary .stats-value {
  color: #9c27b0;
}

.stats-card.success .stats-value {
  color: #4caf50;
}

.stats-card.warning .stats-value {
  color: #ff9800;
}

.stats-card.danger .stats-value {
  color: #f44336;
}
</style>
