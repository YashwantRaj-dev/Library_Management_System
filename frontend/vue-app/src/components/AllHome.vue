<template>
  <div class="home">
    <h1>Welcome to Library Management System</h1>
    <div class="user-options">
      <div class="option">
        <h2>User Login</h2>
        <router-link to="/login"><button>Login</button></router-link>
      </div>
      <div class="option">
        <h2>User Sign Up</h2>
        <router-link to="/signup"><button>Sign Up</button></router-link>
      </div>
    </div>
    <div class="admin-options">
      <div class="option">
        <h2>Librarian</h2>
        <router-link to="/librarian-login"><button>Librarian Login</button></router-link>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'AllHome'
};
</script>

<style>
.home {
  text-align: center;
  margin-top: 50px;
}

.user-options, .admin-options {
  display: flex;
  flex-direction: column;
  justify-content: center;
  margin-top: 20px;
}

.option {
  margin: 0 20px;
}

option h2 {
  margin-bottom: 10px;
}

button {
  padding: 10px 20px;
  border: none;
  border-radius: 5px;
  background-color: skyblue;
  color: white;
  cursor: pointer;
  transition: background-color 0.3s;
}

button:hover {
  background-color: #007bb5;
}
</style>
