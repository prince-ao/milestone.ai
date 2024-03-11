/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.html", "./app/**/_*.py"],
  theme: {
    extend: {
      height: {
        'header': '80px'
      },
      minHeight: {
        'main': 'calc(100vh - 160px)'
      },
      animation: {
        appear: 'appear 1s ease-in-out forwards'
      },
      keyframes: {
        appear: {
          'from': {
            opacity: 0
          },
          'to': {
            opacity: 1
          }
        }
      }
    },
  },
  plugins: [],
}

