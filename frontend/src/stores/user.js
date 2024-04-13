import { defineStore } from 'pinia'

export const useUserStore = defineStore('userData', {
  state: () => {
    return {
      token: null
    }
  }
})
