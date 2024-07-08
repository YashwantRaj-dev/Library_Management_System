<template>
    <div class="login">
      <h1>Login</h1>
      <form @submit.prevent="login">
        <input type="text" v-model="username" placeholder="Username" required>
        <input type="password" v-model="password" placeholder="Password" required>
        <button type="submit">Login</button>
      </form>
      <p>New User? <router-link to="/signup">Go to Sign Up Page</router-link></p>
    </div>
  </template>
  
  <script>
  import axios from '../axios';  // Use the configured Axios instance
  
  export default {
    name: 'UserLogin',
    data() {
      return {
        username: '',
        password: ''
      };
    },
    methods: {
      async login() {
        try {
          const response = await axios.post('/login', {
            username: this.username,
            password: this.password
          });
          // Store the JWT token and username
          localStorage.setItem('token', response.data.token);
          localStorage.setItem('username', this.username);
          // Redirect to UserDashboard
          this.$router.push('/userdashboard');
        } catch (error) {
          console.error(error);
          alert('Error: ' + error.response.data.message);
        }
      }
    }
  };
  </script>
  
  <style>
  .login {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .login h1 {
    margin-bottom: 30px;
    color: #333;
  }
  
  .login input {
    width: 100%;
    height: 40px;
    padding-left: 20px;
    margin-bottom: 20px;
    border: 1px solid skyblue;
    border-radius: 5px;
    box-sizing: border-box;
  }
  
  .login button {
    width: 100%;
    height: 40px;
    border: 1px solid skyblue;
    border-radius: 5px;
    color: #fff;
    background-color: skyblue;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .login button:hover {
    background-color: #007bb5;
  }
  
  .login input:focus {
    outline: none;
    border-color: #007bb5;
  }
  </style>
  