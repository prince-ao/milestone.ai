/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html"],
  theme: {
    extend: {
      height: {
        'header': '80px'
      },
      minHeight: {
        'main': 'calc(100vh - 160px)'
      }
    },
  },
  plugins: [],
}

