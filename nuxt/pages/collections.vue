<template>
  <div>
    <collections-create></collections-create>
    <pre>
    {{$store.state.collections}}
    </pre>
  </div>
</template>

<script>

import CollectionsCreate from '../components/collections/collections-create'
export default {
  name: 'Collections',
  components: { CollectionsCreate },
  data() {
    return {
      queries: undefined,
      collections: undefined
    }
  },
  computed: {
    hashes() {
      return Object.keys(this.allowList.hash_to_query_name_map)
    }
  },
  mounted() {
    this.$store.dispatch('getCollections')
  },
  async fetch() {
    this.queries = await this.$axios.$get('http://127.0.0.1:5151/')
    this.collections = await this.$axios.$get('http://127.0.0.1:5151/collections/list')
  }
}
</script>

<style scoped>

</style>
