/** @type {import('tailwindcss').Config} */
import daisyui from 'daisyui'
export default {
    content: ['./index.html', 'templates/*.html', 'style.css', 'test.css'],
    daisyui: {
        themes: ['corporate', 'business'],
        logs: false,
    },
    plugins: [daisyui],
}
