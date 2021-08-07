<template>
  <div class='flex flex-col col p-4 '>
    <collections-select v-model='collection' class='my-4'></collections-select>
    <button class='btn my-4' @click='addToCollection'>Add to collection</button>
    {{ collection }}
  </div>
</template>

<script>
import CollectionsSelect from '../collections/collections-select'

export default {
  name: 'QueriesAddToCollection',
  components: { CollectionsSelect },
  props: {
    query: {
      type: String,
      required: true
    },
    queryName: {
      type: String,
      required: true
    }
  },
  data() {
    return {
      collection: null
    }
  },
  methods: {
    addToCollection() {
      if (this.collection === null) {
        return
      }
      this.$axios.$post('http://127.0.0.1:5151/queries/add', {
        name: this.queryName,
        query: this.query,
        collection_name: this.collection
      }).then((data) => {
        console.log(data)
        this.$emit('updated')
      })
    }
  }
}
</script>

<style scoped>

</style>
