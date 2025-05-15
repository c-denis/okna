import { test, expect } from '@playwright/test'

test('homepage has title', async ({ page }) => {
  await page.goto('/')
  await expect(page).toHaveTitle(/CRM Okna/)
})

test('login form validation', async ({ page }) => {
  await page.goto('/login')
  await page.getByRole('button', { name: 'Войти' }).click()
  await expect(page.getByText('Поле обязательно для заполнения')).toBeVisible()
})
