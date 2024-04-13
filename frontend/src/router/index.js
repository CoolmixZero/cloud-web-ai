import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

import HomeViewVue from '@/views/HomeView.vue'
import LoginViewVue from '@/views/LoginView.vue'
import RegisterViewVue from '@/views/RegisterView.vue'
import ProfileViewVue from '@/views/ProfileView.vue'

const authGuard = (to, from, next) => {
  const userStore = useUserStore()
  if (userStore.token) return next({ name: 'home' })
  return next()
}

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'home',
      component: HomeViewVue
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginViewVue,
      beforeEnter: authGuard
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterViewVue
    },
    {
      path: '/profile',
      name: 'Profile',
      component: ProfileViewVue
    }
  ]
})

export default router
