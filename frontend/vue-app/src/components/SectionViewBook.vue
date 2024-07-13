<template>
    <div>
      <h1>Books in Section</h1>
      <div>
        <input v-model="newBookTitle" placeholder="Book Title" />
        <input v-model="newBookAuthor" placeholder="Book Author" />
        <textarea v-model="newBookContent" placeholder="Book Content"></textarea>
        <button @click="addBook">Add Book</button>
      </div>
      <div v-if="books.length">
        <ul>
          <li v-for="book in books" :key="book.id">{{ book.title }} by {{ book.author }}</li>
        </ul>
      </div>
      <div v-else>
        No books available
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    data() {
      return {
        books: [],
        newBookTitle: '',
        newBookAuthor: '',
        newBookContent: '',
      };
    },
    created() {
      this.fetchBooks();
    },
    methods: {
      async fetchBooks() {
        try {
          const sectionId = this.$route.params.sectionId;
          const response = await axios.get(`/sections/${sectionId}/books`);
          this.books = response.data.books;
        } catch (error) {
          console.error(error);
        }
      },
      async addBook() {
        try {
          const sectionId = this.$route.params.sectionId;
          await axios.post('/books', {
            title: this.newBookTitle,
            author: this.newBookAuthor,
            content: this.newBookContent,
            section_id: sectionId,
          });
          this.newBookTitle = '';
          this.newBookAuthor = '';
          this.newBookContent = '';
          this.fetchBooks();
        } catch (error) {
          console.error(error);
        }
      }
    }
  };
  </script>
  