<template>
  <div>
    <div>
      <h1 style="text-align: center; margin-top: 20px;">Librarian Stats</h1>
    </div>

    <div>
      <p>Total Unique Users: {{ totalUsers }}</p>
      <p>Total Books on Platform: {{ totalBooks }}</p>
    </div>
    
    <div v-if="pieChartHtml" v-html="pieChartHtml"></div> <!-- Render pie chart HTML -->
    
    <div v-if="userBooks && Object.keys(userBooks).length">
      <h2>Users and Granted Books</h2>
      <ul>
        <li v-for="(books, user) in userBooks" :key="user">
          <strong>{{ user }}:</strong> {{ books.join(', ') }}
        </li>
      </ul>
    </div>
    <button @click="goBack" style="float: center;">Go Back</button>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      pieChartHtml: '',
      totalUsers: 0,
      totalBooks: 0,
      userBooks: {},
    };
  },
  created() {
    this.fetchStats();
  },
  methods: {
    async fetchStats() {
      try {
        const response = await axios.get('http://localhost:5000/librarian/data'); // Updated route
        this.totalUsers = response.data.total_users; // Set total users
        this.totalBooks = response.data.total_books; // Set total books
        this.userBooks = response.data.user_books;
        const response1 = await axios.get('http://localhost:5000/librarian/stats'); // Adjust the route as needed
        this.pieChartHtml = `<img src="http://localhost:5000/librarian/piechart_image" alt="Section Wise Distribution of Books" />`; // Set HTML for pie chart image
        console.log(response1.data); 
      } catch (error) {
        console.error(error);
        alert('Failed to fetch librarian stats');
      }
    },
    goBack() {
      this.$router.go(-1);
    },
  },
};
</script>
 
