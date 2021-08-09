<template>
  <div :class='{
      "p-4": true
    }'>
    <h4>{{ queryNameInternal }}</h4>
    {{ oldQuery }}
    <!--    <pre>{{$store.state.queries[queryObject["hash"]]}}</pre>-->
    <pre>{{ queryObject }}</pre>
    <!--    <query-viewer :code='queryObject.query'></query-viewer>-->
    <queries-add-to-collection :query='queryObject.query' :query-name='queryName' :is-update="isStall"></queries-add-to-collection>
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
      collectionName: ''
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
