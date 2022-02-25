<template>
  <div id="app">
    <router-view/>
  </div>
</template>

<style lang="scss">
@use "@/assets/styles/globals";
@use "@/assets/styles/buttons";

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

</style>
