<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
@use "@/assets/styles/globals";
// @font-face{
//   src: url("@/assets/fonts/sans-serif/Quicksand-VariableFont_wght.ttf") format("truetype");
//   font-family: CartedepoeziiFont;
// }

// @font-face{
//   src: url("@/assets/fonts/serif/ZenAntique-Regular.ttf") format("truetype");
//   font-family: CartedepoeziiSerifFont;
// }

:root {
  --primary-color-light: #537494;
  --primary-color: #2c3e50;
}

html, body {
  margin: 0;
  height: 100%;
  overscroll-behavior: auto none;
}

* {
  font-family: globals.$Sans-Serif-Font;
}

h1, h2, h3, h4, h5, h6 {
  font-family: globals.$Serif-Font;
  margin: 0;
}

h1 {
  font-size: clamp(12px, 1.2em, 15px);
}

h2 {
  font-size: clamp(12px, 1.2em, 15px);
}

#app {
  display: contents;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  color: var(--primary-color);
  min-height: 100%;

  > .content-container {
    display: contents;
    min-height: 100%;
  }
}

.btn-link {
  display: inline-flex;
  align-items: center;
  justify-content: center;
  padding: 4px 12px;
  border: 1px solid gray;
  border-radius: 16px;
  text-decoration: none;
  cursor: pointer;
}

.btn-link.bold {
  color: white;
  background: #2c3e50;
}

.btn-link:hover {
  opacity: 0.8;
}
</style>
