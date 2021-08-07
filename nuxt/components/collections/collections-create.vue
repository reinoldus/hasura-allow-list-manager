<template>
  <div>
    <h4>Create new collection</h4>
    <input v-model='name'
           class='bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500' />
    <textarea v-model='comment'
              class='mt-1 bg-gray-200 appearance-none border-2 border-gray-200 rounded w-full py-2 px-4 text-gray-700 leading-tight focus:outline-none focus:bg-white focus:border-purple-500'></textarea>
    <button class='btn' @click='saveCollection'>Save</button>
  </div>
</template>

<script>
export default {
  name: 'CollectionsCreate',
  data() {
    return {
      name: '',
      comment: ''
    }
  },
  methods: {
    saveCollection() {
      this.$axios.$post('http://127.0.0.1:5151/collections/add', {
        name: this.name,
        comment: this.comment
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
