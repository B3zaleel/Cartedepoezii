<template>
  <article class='app-about'>
    <h1>About</h1>
    <p>
      Lorem ipsum dolor sit, amet consectetur adipisicing elit. Optio quibusdam soluta id molestias
      nam ipsa ipsam assumenda quis voluptates totam tenetur cupiditate repellendus doloribus,
      incidunt harum cum commodi ex impedit!
    </p>
    <pre>
The MIT License (MIT)

Copyright (c) 2013 Mike Gehard, Exercism

Permission is hereby granted, free of charge, to any person obtaining a copy of
this software and associated documentation files (the "Software"), to deal in
the Software without restriction, including without limitation the rights to
use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of
the Software, and to permit persons to whom the Software is furnished to do so,
subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS
FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR
COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER
IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.

    </pre>
  </article>
</template>

<script lang='ts'>
import { Component, Vue } from 'vue-property-decorator';

@Component({
  name: 'AboutContent',
})
export default class AboutContent extends Vue {}
</script>

<style lang='scss'>
p {
  padding: 10px;
}
</style>
