<script setup>
import { RouterLink, RouterView } from 'vue-router'
// Die importierten Komponenten, die von Vite im <template> nicht mehr benötigt werden,
// wurden hier entfernt.

 /*< img alt="Vue logo" class="logo" src="@/assets/logo.svg" width="125" height="125" /> */
</script>

<template>
  <header>
   
    <div class="wrapper">
      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/login">Login</RouterLink>
        <RouterLink to="/register">Registrieren</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

