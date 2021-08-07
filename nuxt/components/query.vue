<template>
  <div :class='{
      "bg-danger": isStall,
      "bg-success": isAdded,
      "bg-warning": isNotAdded,
      "p-4": true
    }'>
    <input v-if='isNotAdded' v-model='queryNameInternal' />
    <h4 v-else>{{ queryNameInternal }} ({{allowList.hash_to_query_name_map[queryObject.hash]}})</h4>
    <collections-select v-model='collectionName'></collections-select>
    {{collectionName}}
    <div>{{ queryObject.raw }}</div>
    <div>{{ queryObject.hash }}</div>
    <button v-if='!allowList["hashes"].includes(queryObject["hash"]) && !(queryName in allowList.queries)'
            @click='addQuery(queryNameInternal, queryObject.raw)'>Add to hasura
    </button>
    <button v-else-if='!allowList["hashes"].includes(queryObject["hash"]) && queryName in allowList.queries'
            @click='updateQuery(queryName, queryObject.raw)'>Update
    </button>
    <button v-else @click='deleteQuery(queryName, queryObject.raw)'>Delete</button>
  </div>
</template>

<script>
import CollectionsSelect from './collections/collections-select'
export default {
  name: 'Query',
  components: { CollectionsSelect },
  props: {
    queryName: {
      type: String,
      required: true
    },
    queryObject: {
      type: Object,
      required: true
    },
    allowList: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      queryNameInternal: this.queryName,
      collectionName: ''
    }
  },
  computed: {
    isAdded() {
      return this.allowList.hashes.includes(this.queryObject.hash)
    },
    isNotAdded() {
      return !this.allowList.hashes.includes(this.queryObject.hash) && !(this.queryName in this.allowList.queries)
    },
    isStall() {
      return !this.allowList.hashes.includes(this.queryObject.hash) && this.queryName in this.allowList.queries
    }
  },
  methods: {
    addQuery(name, query) {
      this.$axios.$post('http://127.0.0.1:5151/add-query', {
        name,
        query,
        collectionName: this.collectionName
      }).then((data) => {
        console.log(data)
        this.$emit('updated')
      })
    },
    deleteQuery(name, query) {
      this.$axios.$post('http://127.0.0.1:5151/delete-query', {
        name,
        query
      }).then((data) => {
        console.log(data)
        this.$emit('updated')
      })
    },
    updateQuery(name, query) {
      this.$axios.$post('http://127.0.0.1:5151/update-query', {
        name,
        query
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
