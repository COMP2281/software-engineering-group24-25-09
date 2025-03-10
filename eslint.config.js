import js from '@eslint/js'
import html from 'eslint-plugin-html'
import eslintConfigPrettier from 'eslint-config-prettier'

export default [
    js.configs.recommended,
    {
        files: ['**/*.html'],
        plugins: { html },
        rules: { 'no-console': 'off' },
    },
    eslintConfigPrettier,
]
