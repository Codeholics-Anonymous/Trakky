/** @type {import('tailwindcss').Config} */
module.exports = {
  content: ["./App.{js,jsx,ts,tsx}", "./screens/**/*.{js,jsx,ts,tsx}",  "./components/**/*.{js,jsx,ts,tsx}"],
  theme: {
    extend: {
      colors: {
        "light-green" : "#00897b",
        "light-gray" : "#969696",
        "lgt-gray" : "#cccccc",
        "gray": "#aaaaaa",
        "dark-green" : "#00564d",
        "dark-dark-gray" : "#282828",
        "dark-gray" : "#363636"
      }
    },
  },
  plugins: [],
}

