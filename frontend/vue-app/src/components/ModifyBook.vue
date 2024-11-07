<template>
    <div>
      <h1>Modify Book</h1>
      <div>
        <input v-model="bookTitle" placeholder="Book Title" />
        <input v-model="bookAuthor" placeholder="Book Author" />
        <textarea v-model="bookContent" placeholder="Book Content" rows="10"></textarea>
        <button @click="modifyBook">Modify Book</button>
      </div>
      <button @click="goBack">Go Back</button>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    data() {
      return {
        bookTitle: '',
        bookAuthor: '',
        bookContent: '',
        bookId: this.$route.query.bookid
      };
    },
    created() {
      this.fetchBookDetails();
    },
    methods: {
      async fetchBookDetails() {
        try {
          const response = await axios.get(`/books/${this.bookId}`);
          const book = response.data.book;
          this.bookTitle = book.title;
          this.bookAuthor = book.author;
          this.bookContent = book.content;
        } catch (error) {
          console.error(error);
        }
      },
      async modifyBook() {
        try {
          await axios.put(`/books/${this.bookId}`, {
            title: this.bookTitle,
            author: this.bookAuthor,
            content: this.bookContent
          });
          alert("Book Modified Successfully");
          this.$router.go(-1);
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
  