<template>
  <div v-if='!$fetchState.pending'>
    <div v-for='(value, key) in queries' :key='key' :class='{
      "bg-danger": !allowList["hashes"].includes(value["hash"]) && key in allowList.queries,
      "bg-success": allowList["hashes"].includes(value["hash"]),
      "bg-warning": !allowList["hashes"].includes(value["hash"]) && !(key in allowList.queries),
      "p-4": true
    }'>
      {{ key }}
      <div>{{ value.raw }}</div>
      <div>{{ value.hash }}</div>
      <button v-if='!allowList["hashes"].includes(value["hash"]) && !(key in allowList.queries)'
              @click='addQuery(key, value.raw)'>Add to hasura
      </button>
      <button v-else-if='!allowList["hashes"].includes(value["hash"]) && key in allowList.queries'
              @click='updateQuery(key, value.raw)'>Update
      </button>
      <button v-else @click='deleteQuery(key, value.raw)'>Delete</button>
    </div>
    <pre>{{ allowList }}</pre>
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
    addQuery(name, query) {
      this.$axios.$post('http://127.0.0.1:5151/add-query', {
        name,
        query
      }).then((data) => {
        console.log(data)
        this.$fetch()
      })
    },
    deleteQuery(name, query) {
      this.$axios.$post('http://127.0.0.1:5151/delete-query', {
        name,
        query
      }).then((data) => {
        console.log(data)
        this.$fetch()
      })
    },
    updateQuery(name, query) {
      this.$axios.$post('http://127.0.0.1:5151/update-query', {
        name,
        query
      }).then((data) => {
        console.log(data)
        this.$fetch()
      })
    }
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
