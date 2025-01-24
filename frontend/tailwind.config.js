/** @type {import('tailwindcss').Config} */
export default {
    content: ['index.html', 'templates/new_slide_modal.html', 'style.css'],
    daisyui: {
        themes: ['corporate', 'business'],
        logs: false,
    },
    plugins: [require('daisyui')],
}
