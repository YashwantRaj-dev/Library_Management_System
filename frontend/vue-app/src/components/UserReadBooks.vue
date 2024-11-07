<template>
    <div>
      <h1>{{ bookTitle }}</h1>
      <div>
        <p><strong>Author:</strong> {{ bookAuthor }}</p>
        <p><strong>Content:</strong></p>
        <pre>{{ bookContent }}</pre>
      </div>
      <button @click="goBack">Go Back</button>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    data() {
      return {
        bookId: this.$route.query.bookId,  // Ensure the correct query parameter is used
        bookTitle: '',
        bookAuthor: '',
        bookContent: '',
      };
    },
    created() {
      this.fetchBookDetails();
    },
    methods: {
      async fetchBookDetails() {
        try {
          const response = await axios.get(`http://localhost:5000/userreadbooks/${this.bookId}`);
          const book = response.data.book;
          this.bookTitle = book.title;
          this.bookAuthor = book.author;
          this.bookContent = book.content;
        } catch (error) {
          console.error(error);
        }
      },
      goBack() {
        this.$router.go(-1);
      }
    }
  };
  </script>
  
  <style>
  pre {
    white-space: pre-wrap;
    word-wrap: break-word;
    background-color: #f0f0f0;
    padding: 10px;
    border-radius: 5px;
  }
  
  button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
  }
  
  button:hover {
    background-color: #0056b3;
  }
  </style>
