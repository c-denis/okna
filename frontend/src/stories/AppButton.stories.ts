import AppButton from './AppButton.vue'
import type { StoryFn, Meta } from '@storybook/vue3'

export default {
  title: 'UI/AppButton',
  component: AppButton,
  argTypes: {
    variant: {
      control: { type: 'select' },
      options: ['primary', 'secondary'],
    },
    onClick: { action: 'clicked' },
  },
} as Meta<typeof AppButton>

const Template: StoryFn<typeof AppButton> = (args) => ({
  components: { AppButton },
  setup() { return { args } },
  template: '<AppButton v-bind="args">Click me</AppButton>',
})

export const Primary = Template.bind({})
Primary.args = { variant: 'primary' }

export const Secondary = Template.bind({})
Secondary.args = { variant: 'secondary' }

export const Disabled = Template.bind({})
Disabled.args = { disabled: true }
