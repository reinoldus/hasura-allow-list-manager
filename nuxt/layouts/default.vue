<template>
  <div class='container px-4 mx-auto'>
    <nav class='bg-white shadow max-w-screen-md z-10 mx-auto inset-x-0 top-0 flex justify-between items-center'>

      <nuxt-link to='/'>Queries</nuxt-link>
      <nuxt-link to='/collections'>Collections</nuxt-link>

    </nav>
    <Nuxt />
  </div>
</template>

<script>
export default {
  mounted() {
    this.$store.dispatch('getCollections')
  }
}
</script>
