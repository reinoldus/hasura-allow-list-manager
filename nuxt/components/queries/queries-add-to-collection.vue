<template>
  <div class='flex flex-col col p-4 '>
    <collections-select v-model='collection' class='my-4'></collections-select>
    <button v-if="!isUpdate" class='btn my-4' @click='addToCollection'>Add to collection</button>
    <button v-else class='btn my-4' @click='updateInCollection'>Update collection</button>
    {{ collection }}
  </div>
</template>

<script>
import CollectionsSelect from '../collections/collections-select'
import {apiRequest} from "~/utils/utils";

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
    },
    isUpdate: {
      type: Boolean,
      default: false
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
      apiRequest(this, '/queries/add', {
        name: this.queryName,
        query: this.query,
        collection_name: this.collection
      })
    },
    updateInCollection() {
      if (this.collection === null) {
        return
      }
      apiRequest(this, '/queries/update', {
        name: this.queryName,
        query: this.query,
        collection_name: this.collection
      })
    }
  }
}
</script>

<style scoped>

</style>
