<template>
  <div v-if='!$fetchState.pending'>
    <div v-for="(value, key) in queries" :key='key'>
      <div v-if='allowList["hashes"].includes(value["hash"])' style='width: 100px;height:199px;background-color: green;'>dd</div>
      <div v-else-if='key in queries' style='width: 100px;height:199px;background-color: orange;'>dd</div>
      {{key}}
      <div>{{value.raw}}</div>
      <div>{{value.hash}}</div>
      <button @click='addToHasura(key, value.raw)'>Add to hasura</button>
    </div>
    <pre>{{allowList}}</pre>
  </div>
</template>

<script>
export default {
  data() {
    return {
      queries: undefined,
      allowList: undefined
    }
  },
  async fetch() {
    this.queries = await this.$axios.$get('http://127.0.0.1:5151/')
    this.allowList = await this.$axios.$get('http://127.0.0.1:5151/allow-list')
  },
  methods: {
    addToHasura(name, query) {
      this.$axios.$post('http://127.0.0.1:5151/add-to-hasura', {
        name,
        query
      })
    }
  }
}
</script>
