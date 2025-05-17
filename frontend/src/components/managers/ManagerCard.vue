<template>
  <div
    class="manager-card"
    :class="statusClass"
    @click="handleClick"
  >
    <div class="manager-info">
      <h3>{{ manager.name }}</h3>
      <p>{{ manager.position }}</p>
    </div>
    <div class="manager-stats">
      <span class="completed">✓ {{ stats.completed }}</span>
      <span class="rejected">× {{ stats.rejected }}</span>
    </div>
    <div class="manager-status">
      {{ statusText }}
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  manager: {
    type: Object,
    required: true
  },
  stats: {
    type: Object,
    default: () => ({ completed: 0, rejected: 0 })
  }
});

const emit = defineEmits(['select']);

const statusMap = {
  free: { class: 'status-free', text: 'Свободен' },
  busy: { class: 'status-busy', text: 'На заявке' },
  vacation: { class: 'status-neutral', text: 'Выходной' },
  training: { class: 'status-neutral', text: 'Обучение' },
  pair: { class: 'status-neutral', text: 'В паре' }
};

const statusClass = computed(() => statusMap[props.manager.status]?.class || 'status-neutral');
const statusText = computed(() => statusMap[props.manager.status]?.text || '');

const handleClick = () => {
  emit('select', props.manager.id);
};
</script>

<style scoped>
.manager-card {
  border-radius: 8px;
  padding: 16px;
  margin: 8px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.status-free {
  background-color: #ffebee;
  border-left: 4px solid #f44336;
}

.status-busy {
  background-color: #e8f5e9;
  border-left: 4px solid #4caf50;
}

.status-neutral {
  background-color: #f5f5f5;
  border-left: 4px solid #9e9e9e;
}

.manager-info h3 {
  margin: 0;
  font-size: 1.1rem;
}

.manager-stats {
  display: flex;
  gap: 16px;
}

.completed {
  color: #4caf50;
}

.rejected {
  color: #f44336;
}

.manager-status {
  font-size: 0.9rem;
  color: #616161;
}
</style>
