<template>
  <main
    class="main-container flex flex-col w-full h-full flex items-center p-8"
    :class="result === true ? 'bad' : result === false ? 'good' : ''"
  >
    <h2>AI Cancer Detector</h2>
    <p>This application uses AI to understand whether you have cancer or not</p>

    <FilePickerComponent v-if="token" @updateResult="updateResult" />
    <p v-else>
      <b>You need to be authorized to use the AI!</b>
    </p>
  </main>
</template>

<script>
import FilePickerComponent from '@/components/FilePickerComponent.vue'
import { mapState } from 'pinia'
import { useUserStore } from '@/stores/user'

export default {
  name: 'HomeView',
  components: {
    FilePickerComponent
  },
  data() {
    return {
      result: null
    }
  },
  computed: {
    ...mapState(useUserStore, {
      token: (state) => state.token
    })
  },
  methods: {
    updateResult(value) {
      this.result = value
    }
  },
  watch: {
    token() {
      this.result = null
    }
  }
}
</script>

<style scoped lang="scss">
.main-container {
  transition: background-color ease 0.2s;

  &.good {
    background-color: rgba(green, 0.4);
  }

  &.bad {
    background-color: rgba(tomato, 0.4);
  }
}
</style>
