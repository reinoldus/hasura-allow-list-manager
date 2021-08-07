<template>
  <button class='bg-blue-500 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded' @click='$emit("click", $event)'>
    <slot></slot>
  </button>
</template>

<script>
export default {
  name: 'Button'
}
</script>

<style scoped>

</style>
