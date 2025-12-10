import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import CreateJobView from '@/views/CreateJobView.vue'
import JobMarketplaceView from '@/views/JobMarketplaceView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: '/',
      name: 'Home',
      component: HomeView
    },
    {
      path: '/login',
      name: 'Login',
      component: LoginView
    },
    {
      path: '/register',
      name: 'Register',
      component: RegisterView
    },
    {
      path: '/create-job',
      name: 'CreateJob',
      component: CreateJobView,
      meta: { requiresAuth: true } // Mark this route as protected
    },
    {
      path: '/marketplace',
      name: 'JobMarketplace',
      component: JobMarketplaceView
    }
  ],
})

// --- Navigation Guard ---
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);

  // If the route requires authentication and the user is not logged in
  if (requiresAuth && !authStore.isLoggedIn) {
    // Redirect to the login page
    next({ name: 'Login' });
  } else {
    // Otherwise, allow the navigation
    next();
  }
});

export default router
