export const state = () => ({
  collections: {},
  collectionsOnAllowList: {},
  queries: {},
  sessionQueries: {},
  modalContent: ''
})

export const mutations = {
  add(state, text) {
    state.list.push({
      text,
      done: false
    })
  },
  remove(state, { todo }) {
    state.list.splice(state.list.indexOf(todo), 1)
  },
  setGeneric(state, payload) {
    const { key, value } = payload
    state[key] = value
  }
}


export const actions = {
  async getCollections(context) {
    const collections = await this.$axios.$get('http://127.0.0.1:5151/collections/list')
    context.commit('setGeneric', { key: 'collections', value: collections.collections })
    context.commit('setGeneric', { key: 'collectionsOnAllowList', value: collections.on_allow })
    const queries = await this.$axios.$get('http://127.0.0.1:5151/queries/list')
    context.commit('setGeneric', { key: 'queries', value: queries })
    const sessionQueries = await this.$axios.$get('http://127.0.0.1:5151/queries/session/list')
    context.commit('setGeneric', { key: 'sessionQueries', value: sessionQueries })

  },
  nuxtServerInit({ commit, dispatch }) {
    dispatch('getCollections')
  }
}
