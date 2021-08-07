export function apiRequest(ctx, path, data, callback) {
  console.log(data)
  ctx.$axios.$post('http://127.0.0.1:5151/' + path, data).then((data) => {
    console.log(data)
    ctx.$emit('updated')
    ctx.$store.commit('setGeneric', {
      key: 'modalContent',
      value: data
    })
    ctx.$store.dispatch('nuxtServerInit')
    ctx.$modal.show('modal')
    if (callback) {
      callback(data)
    }
  })
}
