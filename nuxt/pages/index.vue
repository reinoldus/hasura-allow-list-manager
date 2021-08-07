<template>
  <div v-if='!$fetchState.pending'>
    <div style='display: flex; flex-direction: column;'>

      <query v-for='(value, key) in queries' :key='key' :query-name='key' :query-object='value' :allow-list='allowList'
             @updated='$fetch()'>

      </query>
    </div>
    <pre style='max-width: 100%;overflow-x: scroll;'>{{ allowList }}</pre>
  </div>
</template>

<script>
import Query from '../components/query'

export default {
  components: { Query },
  data() {
    return {
      queries: undefined,
      allowList: undefined
    }
  },
  computed: {
    hashes() {
      return Object.keys(this.allowList.hash_to_query_name_map)
    }
  },
  async fetch() {
    this.queries = await this.$axios.$get('http://127.0.0.1:5151/')
    this.allowList = await this.$axios.$get('http://127.0.0.1:5151/allow-list')
  }
}
</script>

<style>
.bg-success {
  background-color: lightgreen;
}

.bg-warning {
  background-color: rgba(255, 165, 0, 0.5);
}

.bg-danger {
  background-color: lightcoral;
}

.p-4 {
  padding: 1rem;
}
</style>
