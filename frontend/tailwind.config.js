/** @type {import('tailwindcss').Config} */
export default {
    content: ['./index.html', 'templates/*.html', 'style.css', 'test.css'],
    daisyui: {
        themes: ['corporate', 'business'],
        logs: false,
    },
    plugins: [require('daisyui')],
}
