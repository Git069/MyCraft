import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import CreateJobView from '@/views/CreateJobView.vue'
import JobMarketplaceView from '@/views/JobMarketplaceView.vue'
import BecomeCraftsmanView from '@/views/BecomeCraftsmanView.vue'
import JobDetailView from '@/views/JobDetailView.vue'
import InboxView from '@/views/InboxView.vue' // Import the new view

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: HomeView },
    { path: '/login', name: 'Login', component: LoginView },
    { path: '/register', name: 'Register', component: RegisterView },
    { path: '/marketplace', name: 'JobMarketplace', component: JobMarketplaceView },
    { path: '/jobs/:id', name: 'JobDetail', component: JobDetailView },
    { 
      path: '/create-job', 
      name: 'CreateJob', 
      component: CreateJobView, 
      meta: { requiresAuth: true, requiresCraftsman: true } 
    },
    { 
      path: '/become-craftsman', 
      name: 'BecomeCraftsman', 
      component: BecomeCraftsmanView, 
      meta: { requiresAuth: true } 
    },
    // New Inbox route
    { 
      path: '/inbox', 
      name: 'Inbox', 
      component: InboxView, 
      meta: { requiresAuth: true } 
    },
  ],
})

// Navigation Guard
router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresCraftsman = to.matched.some(record => record.meta.requiresCraftsman);

  if (requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'Login' });
  } else if (requiresCraftsman && !authStore.isCraftsman) {
    next({ name: 'BecomeCraftsman' });
  } else {
    next();
  }
});

export default router
