import { createRouter, createWebHistory } from 'vue-router'
import { useAuthStore } from '@/stores/auth'
import HomeView from '@/views/HomeView.vue'
import LoginView from '@/views/LoginView.vue'
import RegisterView from '@/views/RegisterView.vue'
import CreateJobView from '@/views/CreateJobView.vue'
import JobMarketplaceView from '@/views/JobMarketplaceView.vue'
import BecomeCraftsmanView from '@/views/BecomeCraftsmanView.vue'
import JobDetailView from '@/views/JobDetailView.vue'
import InboxView from '@/views/InboxView.vue'
import ProfileView from '@/views/ProfileView.vue'
import DashboardView from '@/views/DashboardView.vue'
import EditServiceView from '@/views/EditServiceView.vue'
import CraftsmanProfileView from '@/views/CraftsmanProfileView.vue'
import MyBookingsView from '@/views/MyBookingsView.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    { path: '/', name: 'Home', component: HomeView },
    { path: '/login', name: 'Login', component: LoginView },
    { path: '/register', name: 'Register', component: RegisterView },
    { path: '/marketplace', name: 'JobMarketplace', component: JobMarketplaceView },
    { path: '/my-bookings', name: 'MyBookings', component: MyBookingsView, meta: { requiresAuth: true }
    },
    
    // Corrected Service Routes
    { path: '/services/:id', name: 'ServiceDetail', component: JobDetailView },
    { 
      path: '/services/:id/edit',
      name: 'ServiceEdit', 
      component: EditServiceView, 
      meta: { requiresAuth: true, requiresCraftsman: true } 
    },

    { 
      path: '/create-service', // Renamed from create-job
      name: 'CreateService', 
      component: CreateJobView, // The view component can be renamed later
      meta: { requiresAuth: true, requiresCraftsman: true } 
    },

    // Other routes
    { path: '/craftsman/:id', name: 'CraftsmanProfile', component: CraftsmanProfileView },
    { path: '/become-craftsman', name: 'BecomeCraftsman', component: BecomeCraftsmanView, meta: { requiresAuth: true } },
    { path: '/inbox', name: 'Inbox', component: InboxView, meta: { requiresAuth: true } },
    { path: '/profile', name: 'Profile', component: ProfileView, meta: { requiresAuth: true } },
    { path: '/dashboard', name: 'Dashboard', component: DashboardView, meta: { requiresAuth: true } },
  ],
})

router.beforeEach((to, from, next) => {
  const authStore = useAuthStore();
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const requiresCraftsman = to.matched.some(record => record.meta.requiresCraftsman);

  if (requiresAuth && !authStore.isLoggedIn) {
    next({ name: 'Login' });
  } else if (requiresAuth && !authStore.isCraftsman && to.meta.requiresCraftsman) {
    next({ name: 'BecomeCraftsman' });
  } else {
    next();
  }
});

export default router
