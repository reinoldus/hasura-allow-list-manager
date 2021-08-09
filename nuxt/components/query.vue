<template>
  <div :class='{
      "p-4": true
    }'>
    <h1>{{ queryNameInternal }}</h1>
    {{ oldQuery }}
    <!--    <pre>{{$store.state.queries[queryObject["hash"]]}}</pre>-->
    <pre class="overflow-x-scroll">{{ queryObject }}</pre>
    <h5>This query is in the following collections:</h5>
    <ul>
      <li v-for="name in queryObject.collections_by_hash" :key="name">{{name}}</li>
    </ul>
    <!--    <query-viewer :code='queryObject.query'></query-viewer>-->
    <queries-add-to-collection :readonly='true' :query='queryObject.query' :query-name='queryName' :is-update="isStall"></queries-add-to-collection>
    <ClientOnly>
      <CodeEditor v-if="queryObject.query" :code="queryObject.query.slice(0, codeSlice)"/>
      <button v-if="codeSlice" class="btn" @click="codeSlice = undefined">Show more than 200 characters</button>
      <button v-else class="btn" @click="codeSlice = 200">Show ONLY 200 characters</button>
    </ClientOnly>
    <button v-if='isStall' class='btn'
            @click='updateQuery(queryName, queryObject.raw)'>Update
    </button>

    <queries-delete-from-collection v-if='isAdded'
                                    :query-name='queryNameInternal'
                                    :collections='queryObject.collections_by_hash'></queries-delete-from-collection>
  </div>
</template>

<script>
import QueriesAddToCollection from './queries/queries-add-to-collection'
import QueriesDeleteFromCollection from './queries/queries-delete-from-collection'

export default {
  name: 'Query',
  components: { QueriesDeleteFromCollection, QueriesAddToCollection },
  props: {
    queryName: {
      type: String,
      required: true
    },
    queryObject: {
      type: Object,
      required: true
    },
    state: {
      type: String,
      required: true
    },
    oldQuery: {
      type: String,
      default() {
        return 'No old query'
      }
    },
    allowList: {
      type: Object,
      required: true
    }
  },
  data() {
    return {
      queryNameInternal: this.queryName,
      collectionName: '',
      codeSlice: 200
    }
  },
  computed: {
    isAdded() {
      return this.state === 'onList'
    },
    isNotAdded() {
      return this.state === 'notOnList'
    },
    isStall() {
      return this.state === 'stall'
    }
  },
  methods: {
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
