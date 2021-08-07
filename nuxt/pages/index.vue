<template>
  <div v-if='!$fetchState.pending'>
    <!--    {{ queriesOnAllowList }}-->
    <!--    {{ queriesOutdated }}-->
    {{ queriesNotOnAllowList }}
    <div class='flex flex-col'>
      <query v-for='{hash, savedQuery} in queriesOutdated'
             :key='hash'
             state='stall'
             class='bg-danger' :query-name='$store.state.sessionQueries[hash].name' :old-query='savedQuery'
             :query-object='$store.state.sessionQueries[hash]'
             :allow-list='allowList'
             @updated='$fetch()'>

      </query>
    </div>
    xx
    <div class='flex flex-col mt-5'>
      <query v-for='hash in queriesNotOnAllowList'
             :key='hash'
             state='notOnList'
             class='bg-warning my-2' :query-name='$store.state.sessionQueries[hash].name'
             :query-object='$store.state.sessionQueries[hash]'
             :allow-list='allowList'
             @updated='$fetch()'>

      </query>
    </div>
    <div class='flex flex-col mt-5'>
      <query v-for='hash in queriesOnAllowList'
             :key='hash'
             state='onList'
             class='bg-success my-2' :query-name='$store.state.sessionQueries[hash].name'
             :query-object='$store.state.sessionQueries[hash]'
             :allow-list='allowList'
             @updated='$fetch()'>

      </query>
    </div>
    <div style='display: flex; flex-direction: column;'>

      <!--      <query v-for='(value, key) in queries' :key='key' :query-name='key' :query-object='value' :allow-list='allowList'-->
      <!--             @updated='$fetch()'>-->

      <!--      </query>-->
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
  async fetch() {
    this.queries = await this.$axios.$get('http://127.0.0.1:5151/')
    this.allowList = await this.$axios.$get('http://127.0.0.1:5151/allow-list')
  },
  computed: {
    hashes() {
      return Object.keys(this.allowList.hash_to_query_name_map)
    },
    queriesOnAllowList() {
      const sessionQueries = Object.keys(this.$store.state.sessionQueries)
      const queries = Object.keys(this.$store.state.queries)

      const onAllow = sessionQueries.filter((v) => {
        return queries.includes(v)
      })

      return onAllow
    },
    queriesNotOnAllowList() {
      const sessionQueries = Object.keys(this.$store.state.sessionQueries)
      const queries = Object.keys(this.$store.state.queries)

      return sessionQueries.filter((v) => {
        return !queries.includes(v)
      })

    },
    queriesOutdated() {
      const outdatedQueries = []
      const queryNames = []
      const queriesByName = {}

      // let's collect all the query names that we know
      // Maybe we hav eto consider collections here at some point
      for (const [, value] of Object.entries(this.$store.state.queries)) {
        queryNames.push(...value.names)
        for (const name of value.names) {
          console.log(name)
          queriesByName[name] = value.query
        }
      }

      console.log(queriesByName)
      // iterating over the queries in the current session
      for (const [key, value] of Object.entries(this.$store.state.sessionQueries)) {

        if (!this.queriesOnAllowList.includes(key)) {
          if (value.queryName === name) {
            outdatedQueries.push({
              hash: key,
              savedQuery: queriesByName[name]
            })
          }
        }
      }


      return outdatedQueries
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
