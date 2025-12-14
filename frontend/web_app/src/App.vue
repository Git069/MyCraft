<script setup>
import { RouterLink, RouterView } from 'vue-router'
// NEU: Importieren Sie Ihr Logo direkt. Der Alias @ steht für den 'src/' Ordner.
import AppLogo from '@/assets/logo.svg' 
</script>

<template>
  <!-- Die gesamte Navigation wird in den <header> verlagert -->
  <header>
    <div class="nav-container">
      
      <!-- 1. Logo-Bereich (ersetzt den "Home"-Link) -->
      <!-- <RouterLink> sorgt dafür, dass ein Klick zur Startseite navigiert -->
      <RouterLink :to="{ name: 'home' }" class="logo-link"> 
        <img  :src="AppLogo" alt="App Logo" class="logo-image" />
      </RouterLink>
      
      <!-- 2. Navigations-Links (rechtsbündig) -->
      <nav class="nav-links">
        <!-- Der "Home"-Link wurde entfernt -->
        <!--<RouterLink to="/login">Login</RouterLink>--> 
        <!--<RouterLink to="/register">Registrieren</RouterLink>-->
        <RouterLink :to="{ name: 'login' }">Login</RouterLink>
        <RouterLink :to="{ name: 'register' }">Registrieren</RouterLink>
      </nav>
      
    </div>
  </header>

  <!-- Der RouterView, der den Inhalt der aktuellen Seite anzeigt -->
  <RouterView />
</template>

<style scoped>
/* -------------------------------------------------------------------------- */
/* 1. LAYOUT DES CONTAINERS (Flexbox)                                         */
/* -------------------------------------------------------------------------- */
header {
  /* Stellt sicher, dass die Kopfzeile die volle Breite einnimmt */
  width: 100%;
  /* Optional: Hintergrundfarbe für die Navigationsleiste */
  background-color: #ffffff; 
  /* Optional: Leichte Trennlinie unten */
  border-bottom: 1px solid #eeeeee;
}

/* Der innere Container, der die linke und rechte Seite steuert */
.nav-container {
  /* Verwendet Flexbox für die Aufteilung */
  display: flex;
  
  /* Ordnet Logo links und Links rechts an (wichtigste Regel!) */
  justify-content: space-between; 
  
  /* Zentriert die Elemente vertikal */
  align-items: center; 
  
  /* Fügt vertikales Padding hinzu (Abstand oben/unten) */
  padding: 10px 0;
  
  /* Wichtig: Nutzt den globalen Rand-Abstand nur intern */
  /* Wir nutzen hier die gleiche Logik wie in PublicStyles.css für den body, 
     aber limitieren die Breite, falls Sie den Inhalt zentrieren möchten. */
  max-width: 1200px; /* Maximale Breite des Navigationsinhalts */
  margin: 0 auto;    /* Zentrierung des Navigationsinhalts */
}

/* -------------------------------------------------------------------------- */
/* 2. LOGO-STYLING (NEU)                                                      */
/* -------------------------------------------------------------------------- */
.logo-link {
  text-decoration: none; 
  /* Stellt sicher, dass das Logo und der Link flexibel sind */
  display: flex; 
  align-items: center;
}

.logo-image {
  /* NEU: Definieren Sie eine feste Höhe, damit das Logo im Nav-Bereich Platz hat */
  height: clamp(30px, 5vw, 45pxpx); /* Skaliert zwischen 30px und 45px je nach Viewport-Breite */
  width: auto;
}

/* -------------------------------------------------------------------------- */
/* 3. NAVIGATIONS-LINKS STYLING                                               */
/* -------------------------------------------------------------------------- */
.nav-links {
  display: flex;
  gap: 15px; /* Abstand zwischen den Links */
}

.nav-links a {
  /* Entfernt die Unterstreichung */
  text-decoration: none; 
  color: #495057;
  font-weight: 500;
  padding: 5px 10px; /* Kleiner Innenabstand für Hover-Effekt */
  transition: color 0.2s;
}

.nav-links a:hover,
.nav-links a.router-link-exact-active {
  color: #007bff; /* Farbe bei Hover oder aktiver Route */
}

/* Entfernt den alten .wrapper, da wir .nav-container verwenden */
.wrapper {
  display: none;
}
</style>