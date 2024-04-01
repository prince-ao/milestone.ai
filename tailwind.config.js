/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.{html,j2}", "./app/**/_*.py"],
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
      backgroundColor: {
	peach: '#fce9d9',
	orange: '#f79546'
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
      },
      fontSize: {
        // clamp(minimum, preferred, maximum)
        'responsive-title': 'max(4.5vw, 5.5vh)',
        'responsive-header': 'max(2vw, 2.5vh)',
        'responsive-subheader': 'max(1.75vw, 2.25vh)',
        'responsive-text': 'max(1vw, 1.5vh)',
      }
    },
  },
  plugins: [],
}

