<template>
  <header class="bg-[var(--primary-color)] text-white py-2 px-7 flex justify-between items-center">
    <RouterLink to="/">
      <div class="text-lg font-bold text-white">Cancer Detector AI</div>
    </RouterLink>

    <div class="flex flex-row items-center gap-3">
      <template v-if="!token">
        <RouterLink to="/login">
          <ButtonPrime
            label="Login"
            class="p-button-text px-3 text-white py-2 hover:bg-zinc-600 text-sm"
          />
        </RouterLink>

        <RouterLink to="/register">
          <ButtonPrime
            label="Register"
            class="p-button-text px-3 text-white py-2 hover:bg-zinc-600 text-sm"
          />
        </RouterLink>
      </template>

      <template v-else>
        <RouterLink to="/profile">
          <ButtonPrime
            class="p-button-rounded p-button-success w-8 h-8 hover:bg-zinc-600 bg-transparent border-none"
            icon="pi pi-user"
            @click="onProfileClick"
          />
        </RouterLink>

        <ButtonPrime
          label="Log out"
          class="p-button-text px-3 text-white py-2 hover:bg-zinc-600 text-sm"
          @click="logOut"
        />
      </template>
    </div>
  </header>
</template>

<script>
import ButtonPrime from 'primevue/button'
import { RouterLink } from 'vue-router'
import { useCookies } from 'vue3-cookies'
import { mapState } from 'pinia'
import { useUserStore } from '@/stores/user'

export default {
  name: 'HeaderComponent',
  setup() {
    const userStore = useUserStore()
    const { cookies } = useCookies()
    return { cookies, userStore }
  },
  data() {
    return {}
  },
  components: {
    ButtonPrime,
    RouterLink
  },
  methods: {
    onProfileClick() {
      console.log('Profile icon clicked')
    },
    logOut() {
      this.cookies.remove('api_token')
      this.userStore.$patch({ token: null })

      this.$notify({
        title: 'Success',
        text: 'Successfully logged out!',
        type: 'success'
      })

      this.$router.push({ name: 'home' })
    }
  },
  computed: {
    ...mapState(useUserStore, {
      token: (store) => store.token
    })
  }
}
</script>

<style scoped></style>
