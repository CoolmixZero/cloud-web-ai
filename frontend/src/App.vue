<template>
  <div class="w-full h-full flex flex-col">
    <Notifications position="bottom right" />
    <HeaderComponent />
    <RouterView />
  </div>
</template>

<script>
import { RouterView } from 'vue-router'
import HeaderComponent from './components/HeaderComponent.vue'
import { useUserStore } from '@/stores/user'
import { useCookies } from 'vue3-cookies'
import { mapState } from 'pinia'

export default {
  name: 'App',
  components: {
    RouterView,
    HeaderComponent
  },

  mounted() {
    this.userStore.$patch({
      token: this.cookies.get('api_token')
    })
  },

  setup() {
    const userStore = useUserStore()
    const { cookies } = useCookies()

    return { userStore, cookies }
  },

  computed: {
    ...mapState(useUserStore, {
      token: (state) => state.token
    })
  }
}
</script>

<style scoped lang="scss"></style>
