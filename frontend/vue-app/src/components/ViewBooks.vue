<template>
    <div class="books">
      <h2>Books in Section</h2>
      <button @click="addBook">Add Book</button>
      <div v-for="book in books" :key="book.id" class="book-item">
        <span>{{ book.title }} | {{ book.author }} | {{ book.content }}</span>
      </div>
      <div v-if="showAddBook">
        <h3>Add New Book</h3>
        <form @submit.prevent="createBook">
          <input type="text" v-model="newBook.title" placeholder="Book Title" required>
          <input type="text" v-model="newBook.author" placeholder="Author" required>
          <textarea v-model="newBook.content" placeholder="Content" required></textarea>
          <button type="submit">Add</button>
          <button @click="cancelAddBook">Cancel</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    name: 'ViewBooks',
    data() {
      return {
        books: [],
        showAddBook: false,
        newBook: {
          title: '',
          author: '',
          content: '',
          section_id: this.$route.params.sectionId
        }
      };
    },
    methods: {
      async fetchBooks() {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.get(`/sections/${this.$route.params.sectionId}/books`, {
            headers: { Authorization: `Bearer ${token}` }
          });
          this.books = response.data.books;
        } catch (error) {
          console.error(error);
        }
      },
      addBook() {
        this.showAddBook = true;
      },
      cancelAddBook() {
        this.showAddBook = false;
        this.newBook.title = '';
        this.newBook.author = '';
        this.newBook.content = '';
      },
      async createBook() {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.post('/books', this.newBook, {
            headers: { Authorization: `Bearer ${token}` }
          });
          this.books.push(response.data.book);
          this.cancelAddBook();
        } catch (error) {
          console.error(error);
        }
      }
    },
    mounted() {
      this.fetchBooks();
    }
  };
  </script>
  
  <style>
  .books {
    text-align: center;
  }
  
  .book-item {
    display: flex;
    justify-content: space-between;
    margin: 10px 0;
    padding: 10px;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
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
  