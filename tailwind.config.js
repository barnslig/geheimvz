/** @type {import('tailwindcss').Config} */
export default {
  content: ["*/templates/**/*.html", "*/assets/**/*.{js,ts,jsx,tsx}"],
  theme: {
    extend: {},
  },
  plugins: [require("@tailwindcss/typography")],
};
