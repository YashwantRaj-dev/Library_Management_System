<template>
    <div class="reviews">
      <button @click="goBack" class="go-back">Go Back</button>
      <h1>Reviews for Book: {{ bookName }}</h1>
      <div v-if="reviews.length === 0">No reviews available.</div>
      <div v-else>
        <div v-for="review in reviews" :key="review.id" class="review-item">
          <!--  <p>{{ review.comment }} </p> --> 
          <span>Review: {{ review.comment }} | Rating: {{ review.rating }}</span>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    name: 'UserReadReview',
    data() {
      return {
        bookId: this.$route.query.bookId,
        bookName: this.$route.query.bookName,
        userId: this.$route.query.userId,
        reviews: []
      };
    },
    methods: {
      goBack() {
        this.$router.go(-1);
      },
      fetchReviews() {
        axios.get(`http://localhost:5000/books/${this.bookId}/reviews`)
          .then(response => {
            this.reviews = response.data;
          })
          .catch(error => {
            console.error(error);
          });
      }
    },
    mounted() {
      this.fetchReviews();
    }
  };
  </script>
  
  <style>
  .reviews {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .reviews h1 {
    margin-bottom: 30px;
    color: #333;
  }
  
  .review-item {
    padding: 10px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
    background-color: #f9f9f9;
    margin-bottom: 10px;
  }
  
  .go-back {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
    position: absolute;
    top: 10px;
    left: 10px;
  }
  
  .go-back:hover {
    background-color: #0056b3;
  }
  </style>
  