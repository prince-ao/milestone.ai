/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./app/templates/**/*.{html,j2}", "./app/**/_*.py"],
  theme: {
    extend: {
      height: {
        header: "80px",
      },
      minHeight: {
        main: "calc(100vh - 160px)",
        title: "calc((100vh - 5rem) / 3)",
        "get-started": "calc(2 * (100vh - 5rem) / 3)",
        body: "calc(100vh - 5rem)",
      },
      animation: {
        appear: "appear 1s ease-in-out forwards",
        "text-gradient": "text-gradient 2.5s linear infinite",
      },
      backgroundColor: {
        peach: "#fce9d9",
        orange: "#f79546",
        bluee: "rgba(52, 163, 232, 0.25)",
      },
      fontFamily: {
        display: ["Lilita One", "sans-serif", "ui-sans-serif"],
      },
      boxShadow: {
        glow: "0 0 50px 10px rgba(30, 31, 32, 0.4)",
        "glow-blue": "0 0 50px 10px rgba(52, 163, 232, 0.4)",
      },
      keyframes: {
        "text-gradient": {
          "0%": { backgroundPosition: "0% center" },
          "100%": { backgroundPosition: "200% center" },
        },
        appear: {
          from: {
            opacity: 0,
          },
          to: {
            opacity: 1,
          },
        },
      },
      fontSize: {
        // clamp(minimum, preferred, maximum)
        "responsive-title": "max(4.5vw, 5.5vh)",
        "responsive-header": "max(2vw, 2.5vh)",
        "responsive-subheader": "max(1.75vw, 2.25vh)",
        "responsive-text": "max(1vw, 1.5vh)",
      },
    },
  },
  plugins: [],
};
