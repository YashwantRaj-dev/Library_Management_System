<template>
  <div>
    <button @click="goBack" class="go-back">Go Back</button>
    <h1>Books in Section</h1>
    <div>
      <input v-model="newBookTitle" placeholder="Book Title" required />
      <input v-model="newBookAuthor" placeholder="Book Author" required />
      <textarea v-model="newBookContent" placeholder="Book Description" required></textarea>
      <button @click="addBook">Add Book</button>
    </div>
    <div v-if="books.length">
      <h2>List Of Books in Section {{ sectionName }}</h2>
      <ul>
        <li v-for="book in books" :key="book.id" class="book-item">
          <span>{{ book.title }} by {{ book.author }}</span>
          <div class="book-actions">
            <button @click="modifyBook(book.id)">Modify</button>
            <button @click="readBook(book.id)">Read</button>
            <button @click="deleteBook(book.id)">Delete</button>
          </div>
        </li>
      </ul>
    </div>
    <div v-else>
      <p>No books available</p>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      books: [],
      sectionName: '',
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
        const sectionId = this.$route.query.sectionid;
        const response = await axios.get(`/sections/${sectionId}/books`);
        this.books = response.data.books;
        this.sectionName = response.data.sectionName; // Assuming sectionName is provided
      } catch (error) {
        console.error(error);
      }
    },
    async addBook() {
      if (!this.newBookTitle || !this.newBookAuthor || !this.newBookContent) {
        alert("All fields are required!");
        return;
      }
      try {
        const sectionId = this.$route.query.sectionid;
        await axios.post(`/sections/${sectionId}/books`, {
          title: this.newBookTitle,
          author: this.newBookAuthor,
          content: this.newBookContent
        }, {
          headers: {
            Authorization: `Bearer ${localStorage.getItem('token')}`
          }
        });
        this.newBookTitle = '';
        this.newBookAuthor = '';
        this.newBookContent = '';
        this.fetchBooks();
      } catch (error) {
        console.error(error);
      }
    },
    async deleteBook(bookId) {
      try {
        await axios.delete(`/books/${bookId}`);
        this.fetchBooks();
      } catch (error) {
        console.error(error);
      }
    },
    modifyBook(bookId) {
      this.$router.push({ path: '/modify-book', query: { bookid: bookId } });
    },
    readBook(bookId) {
      this.$router.push({ path: '/read-book', query: { bookid: bookId } });
    },
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>

<style>
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

.book-item {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  background-color: #f9f9f9;
}

.book-actions {
  display: flex;
  gap: 10px;
}

textarea {
  display: block;
  width: 98.5%;
  margin-top: 10px;
  margin-bottom: 10px;
  height: 100px;
  padding: 10px;
  border-radius: 5px;
  border: 1px solid #ccc;
  font-family: inherit;
  font-size: 16px;
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
