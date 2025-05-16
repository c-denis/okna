import { mount } from '@vue/test-utils'
import AppInput from '@/components/ui/AppInput.vue'

describe('AppInput', () => {
  it('renders with label', () => {
    const wrapper = mount(AppInput, {
      props: {
        label: 'Test Label',
        modelValue: ''
      }
    })
    expect(wrapper.find('label').text()).toBe('Test Label')
  })

  it('emits update:modelValue on input', async () => {
    const wrapper = mount(AppInput, {
      props: {
        modelValue: ''
      }
    })

    await wrapper.find('input').setValue('test value')
    expect(wrapper.emitted('update:modelValue')).toBeTruthy()
    expect(wrapper.emitted('update:modelValue')?.[0]).toEqual(['test value'])
  })

  it('shows error message when error prop is provided', () => {
    const wrapper = mount(AppInput, {
      props: {
        modelValue: '',
        error: 'Field is required'
      }
    })

    expect(wrapper.find('.error-message').text()).toBe('Field is required')
    expect(wrapper.find('.input-wrapper').classes()).toContain('has-error')
  })

  it('toggles password visibility', async () => {
    const wrapper = mount(AppInput, {
      props: {
        modelValue: '',
        type: 'password'
      }
    })

    expect(wrapper.find('input').attributes('type')).toBe('password')
    await wrapper.find('.toggle-password').trigger('click')
    expect(wrapper.find('input').attributes('type')).toBe('text')
  })

  it('disables input when disabled prop is true', () => {
    const wrapper = mount(AppInput, {
      props: {
        modelValue: '',
        disabled: true
      }
    })

    expect(wrapper.find('input').attributes('disabled')).toBe('')
  })
})
