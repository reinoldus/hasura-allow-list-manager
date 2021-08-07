<template>
  <div class='my-4'>

  <pre class='max-h-60 overflow-y-scroll overflow-x-hidden'>{{ dedent(code) }}</pre>
  </div>
</template>

<script>
import dedent from 'dedent'

export default {
  name: 'QueryViewer',
  props: {
    code: {
      type: String,
      required: true
    }
  },
  methods: {
    dedent,
    onCmCursorActivity(codemirror) {
      console.debug('onCmCursorActivity', codemirror)
    },
    onCmReady(codemirror) {
      console.debug('onCmReady', codemirror)
    },
    onCmFocus(codemirror) {
      console.debug('onCmFocus', codemirror)
    },
    onCmBlur(codemirror) {
      console.debug('onCmBlur', codemirror)
    }
  }
}
</script>

<style lang='scss' scoped>
.example {
  display: flex;
  height: 100%;

  .codemirror,
  .pre {
    width: 50%;
    height: 100%;
    margin: 0;
    overflow: auto;
  }

  .pre {
    display: block;
    padding: 1rem;
    line-height: 1.6;
    word-break: break-all;
    word-wrap: break-word;
  }
}
</style>
