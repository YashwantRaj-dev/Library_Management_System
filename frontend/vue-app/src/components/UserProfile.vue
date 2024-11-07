<template>
  <div class="profile">
    <h1>{{ username }}'s Dashboard</h1>
    <nav class="navbar">
      <router-link :to="{ path: '/userdashboard', query: { username: username } }" :class="{ active: isActive('/userdashboard') }">My Books</router-link>
      <router-link :to="{ path: '/userbooks', query: { username: username } }" :class="{ active: isActive('/userbooks') }">Books</router-link>
      <router-link :to="{ path: '/userprofile', query: { username: username } }" :class="{ active: isActive('/userprofile') }">Profile</router-link>
      <a @click="logout">Logout</a>
    </nav>
    <div class="profile-content">
      <h2>Profile Page</h2>
      <div>
        <h3>Number of Books Completed: {{ stats.booksCompleted }}</h3>
        <h3>Number of Books Reviewed: {{ stats.booksReviewed }}</h3>
        <div>
          <h3>Books Read in Different Sections</h3>
          <!-- <img :src="sectionBarChartUrl" alt="Books by Section"> -->
          <!-- <div v-html="sectionBarChartHtml"></div> Render bar chart HTML -->
          <img :src="barchartImageUrl" alt="Books by Section" />
        </div>
        <div>
          <h3>Section Distribution</h3>
          <!-- <img :src="sectionPieChartUrl" alt="Section Distribution"> -->
          <!-- <div v-html="sectionPieChartHtml"></div> Render pie chart HTML -->
          <img :src="piechartImageUrl" alt="Section Distribution" /> 
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'UserProfile',
  data() {
    return {
      username: '',
      stats: {
        booksCompleted: 0,
        booksReviewed: 0,
      },
      sectionBarChartHtml: '',
      sectionPieChartHtml: '',
      piechartImageUrl: 'http://localhost:5000/user/piechart_image',
      barchartImageUrl: 'http://localhost:5000/user/barchart_image',
    };
  },
  methods: {
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      this.$router.push('/');
    },
    isActive(route) {
      return this.$route.path === route;
    },
    fetchStats() {
      axios.get(`http://localhost:5000/user/stats`, { params: { username: this.username } })
      .then(response => {
      this.stats = response.data.stats;
      // Fetch both the bar chart and pie chart data
      return Promise.all([
        axios.get(`http://localhost:5000/user/section_barchart`, { params: { username: this.username }}), // Fetch bar chart data
        axios.get(`http://localhost:5000/user/section_piechart`, { params: { username: this.username } }) // Fetch pie chart data
        ]);
      })
      .then(responses => {
        this.sectionBarChartHtml = responses[0].data.plot_html; // Set HTML for bar chart
        this.sectionPieChartHtml = responses[1].data.plot_html; // Set HTML for pie chart
      })
      .catch(error => {
        console.error(error);
        alert('Failed to fetch stats');
      });
    }
  },
  mounted() {
    this.username = localStorage.getItem('username');
    this.fetchStats();
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
