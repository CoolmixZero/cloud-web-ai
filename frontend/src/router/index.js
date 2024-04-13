import { createRouter, createWebHistory } from 'vue-router'
import { useUserStore } from '@/stores/user'

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
      component: import('@/views/HomeView.vue')
    },
    {
      path: '/login',
      name: 'Login',
      component: import('@/views/LoginView.vue'),
      beforeEnter: authGuard
    },
    {
      path: '/register',
      name: 'Register',
      component: import('@/views/RegisterView.vue')
    },
    {
      path: '/profile',
      name: 'Profile',
      component: import('@/views/ProfileView.vue')
    }
  ]
})

export default router
