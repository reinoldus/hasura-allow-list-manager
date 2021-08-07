<template>
  <div>
    <collections-create></collections-create>
    <h3>Collections on allow list</h3>
    {{ $store.state.collectionsOnAllowList }}
    <hr class='my-3'>
    <div v-for='(collection, name) of $store.state.collections' :key='name'>
      <h4 :class='{
          "bg-green-700 text-white": $store.state.collectionsOnAllowList.includes(name),
          "p-2": true
        }'>{{ name }}</h4>
      <button class='btn'
              @click='addCollectionToAllowList(name)'>
        Add Collection to allow list
      </button>
      <button class='btn' @click='deleteCollection(name)'>Delete collection</button>
      <pre>
        {{ collection }}
        </pre>
    </div>
  </div>
</template>

<script>

import CollectionsCreate from '../components/collections/collections-create'
import { apiRequest } from '../utils/utils'

export default {
  name: 'Collections',
  components: { CollectionsCreate },
  data() {
    return {
      queries: undefined,
      collections: undefined
    }
  },
  async fetch() {
    this.queries = await this.$axios.$get('http://127.0.0.1:5151/')
    this.collections = await this.$axios.$get('http://127.0.0.1:5151/collections/list')
  },
  computed: {
    hashes() {
      return Object.keys(this.allowList.hash_to_query_name_map)
    }
  },
  mounted() {
    this.$store.dispatch('getCollections')
  },
  methods: {
    deleteCollection(name) {
      apiRequest(this, '/collections/delete', {
        name
      })
    },
    addCollectionToAllowList(name) {
      this.$axios.$post('http://127.0.0.1:5151/collections/add-to-allow-list', {
        name
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
