<template>
    <div class="dashboard">
      <h1>Librarian's Dashboard</h1>
      <nav class="navbar">
        <router-link to="/librarian-booksections" :class="{ active: isActive('/librarian-booksections') }">Sections</router-link>
        <router-link to="/librarian-requests" :class="{ active: isActive('/librarian-requests') }">Requests</router-link>
        <router-link to="/librarian-stats" :class="{ active: isActive('/librarian-stats') }">Stats</router-link>
        <a @click="logout">Logout</a>
      </nav>
      <router-view></router-view>
    </div>
  </template>
  
  <script>
  export default {
    name: 'LibrarianDashboard',
    methods: {
      logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        localStorage.removeItem('role');
        this.$router.push('/');
      },
      isActive(route) {
        return this.$route.path === route;
      }
    }
  };
  </script>
  
  <style>
  .dashboard {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .navbar {
    display: flex;
    justify-content: space-around;
    margin-bottom: 30px;
  }
  
  .navbar a {
    color: black;
    text-decoration: none;
    padding: 10px 20px;
    border-radius: 5px;
  }
  
  .navbar a.active {
    background-color: skyblue;
    color: white;
  }
  </style>
  