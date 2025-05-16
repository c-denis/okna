// src/components/__tests__/AppButton.spec.ts
import { render, screen, fireEvent } from '@testing-library/vue'
import AppButton from '../../../src/components/ui/AppButton.vue'

test('emits click event when clicked', async () => {
  const { emitted } = render(AppButton)
  await fireEvent.click(screen.getByRole('button'))
  expect(emitted().click).toHaveLength(1)
})

test('renders with custom class', () => {
  render(AppButton, {
    props: {
      class: 'custom-class'
    }
  })
  expect(screen.getByRole('button')).toHaveClass('custom-class')
})
