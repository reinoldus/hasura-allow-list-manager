<template>
  <div class='p-4 ml-2'>
    <button v-for='collection in collections' :key='collection' class='btn my-4'
            @click='deleteQuery(collection)'>
      Delete from {{ collection }}
    </button>
  </div>
</template>

<script>

export default {
  name: 'QueriesDeleteFromCollection',
  props: {
    queryName: {
      type: String,
      required: true
    },
    collections: {
      type: Array,
      required: true
    }
  },
  methods: {
    deleteQuery(collection) {
      this.$axios.$post('http://127.0.0.1:5151/queries/delete', {
        name: this.queryName,
        collection_name: collection
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
