/** @type {import('tailwindcss').Config} */
export default {
    content: ['index.html', 'style.css'],
    daisyui: {
        themes: ['corporate', 'business'],
        logs: false,
    },
    plugins: [require('daisyui')],
}
