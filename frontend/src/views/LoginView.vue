<template>
  <div class="flex justify-center items-center h-full bg-gray-100">
    <form
      @submit.prevent="submitForm"
      class="flex flex-col items-center w-full max-w-sm bg-white p-7 rounded-lg gap-4"
    >
      <span class="text-2xl font-bold">Login Form</span>

      <div class="flex flex-col gap-2 w-full">
        <label for="login" class="block text-gray-700 text-base font-bold">Login:</label>
        <InputText
          id="login"
          v-model="v$.login.$model"
          placeholder="Enter your login"
          class="p-inputtext-sm w-full text-base"
          :class="{ 'border-red-500': v$.login.$error }"
          size="large"
          @blur="v$.login.$validate()"
        />
        <template v-if="v$.login.$error">
          <span v-if="v$.login.required.$invalid" class="text-red-500 text-xs">{{
            v$.login.required.$message
          }}</span>
          <span v-else-if="v$.login.alphaNum.$invalid" class="text-red-500 text-xs">{{
            v$.login.alphaNum.$message
          }}</span>
        </template>
      </div>

      <div class="flex flex-col gap-2 w-full">
        <label for="password" class="block text-gray-700 text-base font-bold">Password:</label>
        <InputText
          id="password"
          v-model="password"
          placeholder="Enter your password"
          type="password"
          class="p-inputtext-sm w-full text-base"
          :class="{ 'border-red-500': v$.password.$error }"
          size="large"
          @blur="v$.password.$validate()"
        />
        <template v-if="v$.password.$error">
          <span v-if="v$.password.required.$invalid" class="text-red-500 text-xs">{{
            v$.password.required.$message
          }}</span>
          <span v-else-if="v$.password.alphaNum.$invalid" class="text-red-500 text-xs">{{
            v$.password.alphaNum.$message
          }}</span>
        </template>
      </div>

      <div class="flex items-center justify-between">
        <ProgressSpinner v-if="loading" style="width: 35px; height: 35px" />
        <ButtonPrime
          v-else
          label="Submit"
          type="submit"
          class="p-button-sm text-base"
          size="large"
        />
      </div>
    </form>
  </div>
</template>

<script>
import ProgressSpinner from 'primevue/progressspinner'
import InputText from 'primevue/inputtext'
import ButtonPrime from 'primevue/button'
import { required, alphaNum } from '@vuelidate/validators'
import useVuelidate from '@vuelidate/core'
import { useCookies } from 'vue3-cookies'
import { useUserStore } from '@/stores/user'

export default {
  components: {
    InputText,
    ProgressSpinner,
    ButtonPrime
  },
  data() {
    return {
      login: '',
      password: '',
      loading: false
    }
  },
  validations() {
    return {
      login: { required, alphaNum },
      password: { required, alphaNum }
    }
  },
  setup() {
    const userStore = useUserStore()
    const { cookies } = useCookies()
    return { v$: useVuelidate(), cookies, userStore }
  },
  methods: {
    submitForm() {
      this.v$.$validate()
      if (this.v$.$error) return

      this.loading = true

      this.axios(`${import.meta.env.VITE_API_URL}/auth/login`, {
        method: 'POST',
        data: {
          username: this.login,
          password: this.password
        }
      })
        .then(({ data }) => {
          if (!data?.result?.access_token) return

          this.cookies.set('api_token', data?.result?.access_token)
          this.userStore.$patch({ token: data?.result?.access_token })

          this.$notify({
            title: 'Success',
            text: `Successfully logged in as ${this.login}!`,
            type: 'success'
          })

          this.$router.push({ name: 'home' })
        })
        .catch((error) => {
          console.error(error)
          this.loading = false

          this.$notify({
            title: 'Login Error',
            text: error?.response?.data?.detail,
            type: 'error'
          })
        })
    }
  }
}
</script>

<style scoped lang="scss">
.border-red-500 {
  border-color: #f87171;
}
</style>
