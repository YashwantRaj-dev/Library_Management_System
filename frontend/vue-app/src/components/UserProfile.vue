<template>
    <div class="profile">
      <h1>{{ username }}'s Dashboard</h1>
      <nav class="navbar">
        <router-link to="/userdashboard">My Books</router-link>
        <router-link to="/userbooks">Books</router-link>
        <router-link to="/userprofile" class="active">Profile</router-link>
        <a @click="logout">Logout</a>
      </nav>
      <div class="profile-content">
        <h2>Profile Page (Logging out...)</h2>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserProfile',
    data() {
      return {
        username: ''
      };
    },
    methods: {
      logout() {
        localStorage.removeItem('token');
        localStorage.removeItem('username');
        this.$router.push('/');
      }
    },
    mounted() {
      this.username = localStorage.getItem('username');
      this.logout();
    }
  };
  </script>
  
  <style>
  .profile {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .profile h1 {
    margin-bottom: 30px;
    color: #333;
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
  
  .profile-content {
    text-align: center;
  }
  
  button {
    border: 1px solid skyblue;
    border-radius: 5px;
    color: #fff;
    background-color: skyblue;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  button:hover {
    background-color: #007bb5;
  }
  </style>
  