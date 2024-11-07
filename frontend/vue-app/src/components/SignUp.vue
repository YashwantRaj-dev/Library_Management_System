<template>
    <div class="register">
      <h1>Sign Up</h1>
      <form @submit.prevent="signUp">
        <input type="text" v-model="username" placeholder="Username" required>
        <input type="email" v-model="email" placeholder="Email" required>
        <input type="password" v-model="password" placeholder="Password" required>
        <input type="password" v-model="confirmPassword" placeholder="Confirm Password" required>
        <button type="submit">Sign Up</button>
      </form>
      <button @click="$router.go(-1)" style="background-color: lightgreen; color: white;">Go Back</button>
    </div>
  </template>
  
  <script>
  import axios from '../axios';  // Use the configured Axios instance
  
  export default {
    name: 'SignUp',
    data() {
      return {
        username: '',
        email: '',
        password: '',
        confirmPassword: ''
      };
    },
    methods: {
      async signUp() {
        if (this.password !== this.confirmPassword) {
          alert('Passwords do not match');
          return;
        }
        try {
          const response = await axios.post('/register', {
            username: this.username,
            email: this.email,
            password: this.password,
            confirm_password: this.confirmPassword
          });
          alert('User created: ' + response.data.message);
          // Redirect to login page
          this.$router.push('/');
        } catch (error) {
          console.error(error);
          alert('Error: ' + error.response.data.message);
        }
      }
    }
  };
  </script>
  
  <style>
  .register {
    max-width: 400px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .register h1 {
    margin-bottom: 30px;
    color: #333;
  }
  
  .register input {
    width: 100%;
    height: 40px;
    padding-left: 20px;
    margin-bottom: 20px;
    border: 1px solid skyblue;
    border-radius: 5px;
    box-sizing: border-box;
  }
  
  .register button {
    width: 100%;
    height: 40px;
    border: 1px solid skyblue;
    border-radius: 5px;
    color: #fff;
    background-color: skyblue;
    cursor: pointer;
    transition: background-color 0.3s;
  }
  
  .register button:hover {
    background-color: #007bb5;
  }
  
  .register input:focus {
    outline: none;
    border-color: #007bb5;
  }
  </style>
  