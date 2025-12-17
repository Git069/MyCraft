<script setup>
// ... (script setup remains the same)
</script>

<template>
  <div class="container-fluid dashboard-container">
    <!-- ... (header and tabs remain the same) ... -->
    <main class="tab-content">
      <div v-if="loading" class="dashboard-grid">
        <JobCardSkeleton v-for="n in 4" :key="n" />
      </div>
      <template v-else>
        <div v-if="activeTab === 'my-services'">
          <div v-if="myServices.length === 0" class="empty-state">
            <!-- ... -->
          </div>
          <div v-else class="dashboard-grid">
            <!-- FIX: Pass 'service' prop instead of 'job' -->
            <JobCard
              v-for="service in myServices"
              :key="service.id"
              :service="service"
              :show-controls="true"
            />
          </div>
        </div>
        <!-- ... (other tabs remain the same) ... -->
      </template>
    </main>
    <!-- ... (modal remains the same) ... -->
  </div>
</template>

<style scoped>
/* ... (styles remain the same) ... */
</style>
