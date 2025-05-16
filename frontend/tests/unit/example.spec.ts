import { describe, it, expect } from 'vitest'
import { mount } from '@vue/test-utils'
import AppButton from '@/components/ui/AppButton.vue'

describe('AppButton', () => {
  it('renders button text', () => {
    const wrapper = mount(AppButton, {
      slots: {
        default: 'Click me'
      }
    })
    expect(wrapper.text()).toContain('Click me')
  })

  it('emits click event', async () => {
    const wrapper = mount(AppButton)
    await wrapper.trigger('click')
    expect(wrapper.emitted('click')).toBeTruthy()
  })

  it('applies primary variant', () => {
    const wrapper = mount(AppButton, {
      props: {
        type: 'primary'
      }
    })
    expect(wrapper.classes()).toContain('button--primary')
  })
})
