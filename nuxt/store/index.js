export const state = () => ({
  collections: {}
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
  setCollections(state, payload) {
    state.collections = payload
  }
}


export const actions = {
  async getCollections(context) {
    const collections = await this.$axios.$get('http://127.0.0.1:5151/collections/list')
    context.commit('setCollections', collections)
  }
}
