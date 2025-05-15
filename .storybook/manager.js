import { addons } from '@storybook/addons'
import { create } from '@storybook/theming'

const theme = create({
  base: 'light',
  brandTitle: 'My Component Library',
  brandUrl: 'https://example.com',
})

addons.setConfig({
  theme,
  panelPosition: 'right',
})
