import axios from 'axios';
import { useAuthStore } from '@/stores/auth';

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_URL,
  headers: { 'Content-Type': 'application/json' },
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response && error.response.status === 401) {
      const authStore = useAuthStore();
      authStore.logout();
      window.location.href = '/login'; 
    }
    return Promise.reject(error);
  }
);


// Helper to transform GeoJSON to flat objects for UI components
const flattenFeature = (feature) => {
  if (!feature || !feature.properties) return feature;
  return {
    ...feature.properties,
    id: feature.id,        // ID von der obersten Ebene holen
    location: feature.geometry // Geometrie sichern
  };
};

const transformGeoJSON = (response) => {
  const data = response.data;

  // FALL 1: API liefert direkt ein GeoJSON FeatureCollection
  if (data && data.type === 'FeatureCollection' && Array.isArray(data.features)) {
    return {
        ...response,
        data: { results: data.features.map(flattenFeature) }
    };
  }

  // FALL 2: API liefert Pagination, und 'results' ist eine FeatureCollection (Standard DRF GIS)
  if (data && data.results && data.results.type === 'FeatureCollection' && Array.isArray(data.results.features)) {
      return {
          ...response,
          data: {
              ...data,
              results: data.results.features.map(flattenFeature)
          }
      };
  }

  // FALL 3: API liefert Pagination, aber 'results' ist direkt ein Array von Features
  // (Sicherheitsnetz, falls die Struktur leicht abweicht)
  if (data && Array.isArray(data.results) && data.results.length > 0 && data.results[0].properties) {
      return {
          ...response,
          data: {
              ...data,
              results: data.results.map(flattenFeature)
          }
      };
  }

  // Kein GeoJSON erkannt -> Original zurückgeben
  return response;
};
export default {
  // ... (Auth & User functions remain same)
  register(userData) { return apiClient.post('/auth/users/', userData); },
  login(credentials) { return apiClient.post('/auth/token/login/', credentials); },
  fetchCurrentUser() { return apiClient.get('/auth/users/me/'); },
  updateUser(userData) { return apiClient.patch('/auth/users/me/', userData); },
  getUserDetails(userId) { return apiClient.get(`/auth/users/${userId}/`); },
  uploadProfilePicture(formData) { return apiClient.patch('/auth/upload-profile-picture/', formData, { headers: { 'Content-Type': 'multipart/form-data' } }); },
  becomeCraftsman(profileData) { return apiClient.post('/auth/become-craftsman/', profileData); },

    // Füge diese Funktion hinzu:
  suggestAddresses(query) {
    return apiClient.get('/services/suggest_address/', { params: { q: query } });
  },

  // --- SERVICES (GeoJSON aware) ---
  createService(serviceData) { 
    if (serviceData instanceof FormData) {
      return apiClient.post('/services/', serviceData, { headers: { 'Content-Type': 'multipart/form-data' } });
    }
    return apiClient.post('/services/', serviceData); 
  },
  
  // Modified getServices to handle GeoJSON
  async getServices(params) { 
    const response = await apiClient.get('/services/', { params });
    return transformGeoJSON(response);
  },
  
  async getServiceDetails(serviceId) { 
    const response = await apiClient.get(`/services/${serviceId}/`);
    // Single Feature handling
    if (response.data && response.data.type === 'Feature') {
        return { ...response, data: { ...response.data.properties, id: response.data.id, location: response.data.geometry } };
    }
    return response;
  },

// Holt die Liste der belegten Tage (Array von Strings "YYYY-MM-DD")
  getServiceAvailability(serviceId) {
    return apiClient.get(`/services/${serviceId}/availability/`);
  },

  // Erstellt eine verbindliche Buchung
  createBooking(bookingData) {
    return apiClient.post('/bookings/', bookingData);
  },

  updateService(serviceId, serviceData) { return apiClient.patch(`/services/${serviceId}/`, serviceData); },
  deleteService(serviceId) { return apiClient.delete(`/services/${serviceId}/`); },
  
  async getMyServices() { 
    const response = await apiClient.get('/services/my-jobs/');
    return transformGeoJSON(response);
  },


  // ... (Aliases and other functions remain same)
  createJob(jobData) { return this.createService(jobData); },
  getJobs(params) { return this.getServices(params); },
  getJobDetails(jobId) { return this.getServiceDetails(jobId); },
  updateJob(jobId, jobData) { return this.updateService(jobId, jobData); },
  deleteJob(jobId) { return this.deleteService(jobId); },
  
  getMyBookings() { return apiClient.get('/bookings/my_bookings/'); },
  getMyOrders() { return apiClient.get('/bookings/my_orders/'); },
  markBookingAsCompleted(bookingId) { return apiClient.post(`/bookings/${bookingId}/mark_completed/`); },
  cancelBooking(bookingId) { return apiClient.post(`/bookings/${bookingId}/cancel/`); },

  getConversations() { return apiClient.get('/conversations/'); },
  getConversationDetails(convoId) { return apiClient.get(`/conversations/${convoId}/`); },
  startConversation(serviceId, message) { return apiClient.post('/conversations/', { job_id: serviceId, message: message }); },
  postMessage(convoId, content) { return apiClient.post(`/conversations/${convoId}/post_message/`, { content: content }); },
  createOffer(offerData) { return apiClient.post('/offers/', offerData); },
  acceptOffer(offerId) { return apiClient.post(`/offers/${offerId}/accept/`); },
  rejectOffer(offerId) { return apiClient.post(`/offers/${offerId}/reject/`); },
  createReview(reviewData) { return apiClient.post('/reviews/', reviewData); },
  
  setAuthToken(token) { if (token) apiClient.defaults.headers.common['Authorization'] = `Token ${token}`; },
  clearAuthToken() { delete apiClient.defaults.headers.common['Authorization']; },
};
