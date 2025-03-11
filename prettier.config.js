const config = {
    trailingComma: 'es5',
    semi: false,
    singleQuote: true,
    printWidth: 140,
    proseWrap: 'always',
    tabWidth: 4,
    requireConfig: false,
    useTabs: false,
    bracketSpacing: true,
    jsxBracketSameLine: false,
    plugins: ["prettier-plugin-tailwindcss", "prettier-plugin-jinja-template"],
    overrides: [
        {
            "files": ["*.html"],
            "options": {
                "parser": "jinja-template"
            }
        }
    ],
}

export default config
