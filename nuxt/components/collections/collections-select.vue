<template>
  <div>
    {{collectionNames}}
    <select v-model='selected'>
      <option v-for='i in collectionNames' :key='i'>{{i}}</option>
    </select>
  </div>
</template>

<script>
export default {
  name: 'collections-select',
  data() {
    return {
      selected: this.value
    }
  },
  props: {
    value: {
      type: String,
      default() {
        return undefined
      }
    }
  },
  watch: {
    selected() {
      this.$emit('input', this.selected)
    }
  },
  computed: {
    collectionNames() {
      return Object.keys(this.$store.state.collections.collections)
    }
  }
}
</script>

<style scoped>

</style>
