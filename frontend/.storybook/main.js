const path = require('path')

module.exports = {
  stories: [
    '../src/**/*.stories.@(js|jsx|ts|tsx|mdx)',
    '../src/**/*.mdx'
  ],
  addons: [
    '@storybook/addon-links',
    '@storybook/addon-essentials',
    '@storybook/addon-interactions',
    '@storybook/addon-a11y',
    '@storybook/addon-postcss',
  ],
  framework: {
    name: '@storybook/vue3-vite',
    options: {}
  },
  features: {
    storyStoreV7: true,
    interactionsDebugger: true,
  },
  viteFinal: async (config) => {
    config.resolve.alias = {
      ...config.resolve.alias,
      '@': path.resolve(__dirname, '../src'),
    }
    return config
  },
  docs: {
    autodocs: 'tag',
  },
}
