<template>
  <select v-model='selected'>
    <option v-for='i in collectionNames' :key='i'>{{ i }}</option>
  </select>
</template>

<script>
export default {
  name: 'CollectionsSelect',
  props: {
    value: {
      type: String,
      default() {
        return undefined
      }
    }
  },
  data() {
    return {
      selected: this.value
    }
  },
  computed: {
    collectionNames() {
      return Object.keys(this.$store.state.collections)
    }
  },
  watch: {
    selected() {
      this.$emit('input', this.selected)
    }
  }
}
</script>

<style scoped>

</style>
