module.exports = {
  content: [
    "./divine_shop/templates/**/*.html",
    "./divine_shop/**/*.html",
    "./divine_shop/**/*.py",
    "./divine_shop/static/js/**/*.js",
    "./node_modules/flowbite/**/*.js",
  ],
  theme: {
    extend: {},
  },
  plugins: [
    require('flowbite/plugin'),
  ],
};
