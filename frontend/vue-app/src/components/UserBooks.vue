<template>
  <div class="books">
    <button @click="goBack" class="go-back">Go Back</button>
    <h1>{{ username }}'s Dashboard</h1>
    <nav class="navbar">
      <router-link :to="{ path: '/userdashboard', query: { username: username } }" :class="{ active: isActive('/userdashboard') }">My Books</router-link>
      <router-link :to="{ path: '/userbooks', query: { username: username } }" :class="{ active: isActive('/userbooks') }">Books</router-link>
      <router-link :to="{ path: '/userprofile', query: { username: username } }" :class="{ active: isActive('/userprofile') }">Profile</router-link>
      <a @click="logout">Logout</a>
    </nav>
    <div class="search-filter">
      <input 
        type="text" 
        :placeholder="`Search by ${searchType}`" 
        v-model="searchQuery"
      >
      <button @click="searchBooks">Filter</button>
      <div class="dropdown">
        <button class="dropbtn">Search by</button>
        <div class="dropdown-content">
          <a @click="setSearchType('Book Title')">Book Title</a>
          <a @click="setSearchType('Author\'s name')">Author's name</a>
          <a @click="setSearchType('Section/Genre')">Section/Genre</a>
          <a @click="setSearchType('Rating')">Rating</a>
        </div>
      </div>
      <button @click="clearSearch">Clear Search</button>
    </div>
    
    <div v-if="searchResultsVisible">
      <h2>Search Results</h2>
      <div v-if="searchResults.length > 0">
        <div v-for="book in searchResults" :key="book.id" class="book-item">
          <span>{{ book.title }} | {{ book.author }} | {{ book.section_name }} | {{ book.rating }}</span>
          <!-- Buttons for book actions -->
        </div>
      </div>
      <div v-else>
        <p>No Such Books</p>
      </div>
    </div>

    <h2>List Of Books</h2>
    <div class="books-list">
      <div v-for="book in filteredBooks" :key="book.id" class="book-item">
        <span>{{ book.title }} | {{ book.author }} | {{ book.section_name }} | {{ book.rating }}</span>
        <div>
          <!-- <button v-if="book.userHasAccess" @click="returnBook(book)">Return</button>
          <button v-else-if="book.requestPending" @click="cancelRequest(book)">Pending/Cancel Request</button>
          <button v-else @click="requestBook(book)">Request</button> -->
          <button @click="readReview(book.id)">Read Reviews</button>
          <button v-if="book.userHasAccess && !book.requestPending" @click="returnBook(book)">Return</button>
          <button v-else-if="book.requestPending" @click="cancelRequest(book)">Pending/Cancel Request</button>
          <button v-else @click="requestBook(book)">Request</button>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  name: 'UserBooks',
  data() {
    return {
      username: '',
      searchQuery: '',
      searchType: 'Book Title',
      books: [],
      booksToBeCompleted: [],
      booksCompleted: [],
      booksPending: [],
      userBookIds: [],
      requestPendingBookIds: [],
      searchResultsVisible: false, // Add this line
      searchResults: [],
    };
  },
  computed: {
    filteredBooks() {
      return this.filterBooks(this.books); 
    }, 
  }, 
  methods: {
    goBack() {
      this.$router.go(-1);
    },
    logout() {
      localStorage.removeItem('token');
      localStorage.removeItem('username');
      this.$router.push('/');
    },
    isActive(route) {
      return this.$route.path === route;
    },
    setSearchType(type) {
      this.searchType = type;
    },
    filterBooks(books) {
      const filteredBooks = books.filter(book => {
        if (this.searchType === 'Book Title') {
          return book.title?.toLowerCase().includes(this.searchQuery.toLowerCase()) || false;
        } else if (this.searchType === 'Author\'s name') {
          return book.author?.toLowerCase().includes(this.searchQuery.toLowerCase()) || false;
        } else if (this.searchType === 'Section/Genre') {
          return book.section_name?.toLowerCase().includes(this.searchQuery.toLowerCase()) || false;
        } else if (this.searchType === 'Rating') {
          return book.rating && book.rating.toString().includes(this.searchQuery);
        }
        return false;
      });

      const booksToBeCompleted = filteredBooks.filter(book =>
        this.userBookIds.includes(book.id) &&
        !this.booksCompleted.some(b => b.id === book.book_id)
      ).map(book => ({
        ...book,
        userHasAccess: true,
        requestPending: false
      }));

      const booksCompleted = filteredBooks.filter(book =>
        this.booksCompleted.some(b => b.id === book.book_id)
      ).map(book => ({
        ...book,
        userHasAccess: true,
        requestPending: false
      }));

      const booksRequested = filteredBooks.filter(book =>
        this.requestPendingBookIds.includes(book.id)
      ).map(book => ({
        ...book,
        userHasAccess: false,
        requestPending: true
      }));

      const booksAvailable = filteredBooks.filter(book =>
        !this.userBookIds.includes(book.id) &&
        !this.requestPendingBookIds.includes(book.id)
      ).map(book => ({
        ...book,
        userHasAccess: false,
        requestPending: false
      }));

      return [...booksToBeCompleted, ...booksCompleted, ...booksRequested, ...booksAvailable];
    },
    searchBooks() {
      this.searchResults = this.filterBooks(this.books); // Use the filterBooks method
      this.searchResultsVisible = this.searchResults.length > 0; // Show results only if there are any
    },
    requestBook(book) {
      if (this.userBookIds.length >= 5) {
        alert("You can't access more than 5 e-books at a time");
        return;
      }

      let days = prompt("Access Duration (Days):");
      if (!days) return;
      
      const validDays = [1, 3, 5, 7];
      if (!validDays.includes(parseInt(days))) {
        alert("Please select a valid duration from 1, 3, 5, or 7 days.");
        return;
      }

      axios.post(`http://localhost:5000/books/${book.id}/request`, {
        username: this.username,
        days_requested: days
      }).then(() => {
        alert("Request sent to Librarian");
        this.requestPendingBookIds.push(book.book_id);
        console.log("Request Pending", this.requestPendingBookIds); 
        this.fetchBooks(); 
        this.fetchUserBooks()
      }).catch(error => {
        console.error(error);
        alert("Failed to send request");
      });
    },
    cancelRequest(book) {
      axios.post(`http://localhost:5000/books/${book.id}/cancel_request`, {
        username: this.username
      }).then(() => {
        const index = this.requestPendingBookIds.indexOf(book.book_id);
        if (index > -1) {
          this.requestPendingBookIds.splice(index, 1);
        }
        alert("Request cancelled successfully");
        this.fetchBooks(); // Refetch the books to update the list
        this.fetchUserBooks()
      }).catch(error => {
        console.error(error);
        alert("Failed to cancel request");
      });
    },
    returnBook(book) {
      if (confirm("Are you sure you want to return the book?")) {
        axios.post(`http://localhost:5000/books/${book.id}/return`, {
          username: this.username
        }).then(() => {
          const index = this.userBookIds.indexOf(book.book_id);
          if (index > -1) {
            this.userBookIds.splice(index, 1);
          }
          alert("Book returned successfully");
          this.fetchBooks(); // Refetch the books to update the list
          this.fetchUserBooks()
        }).catch(error => {
          console.error(error);
          alert("Failed to return book");
        });
      } 
    },
    fetchBooks() {
      axios.get('http://localhost:5000/books').then(response => {
        this.books = response.data.books;
        console.log("Books", this.books);
      }).catch(error => {
        console.error(error);
      });
    },
    fetchUserBooks() {
      axios.get('http://localhost:5000/users/books', {
        params: { username: this.username }
      }).then(response => {
        console.log("Fetched Data:", response.data);
        this.booksToBeCompleted = response.data.booksToBeCompleted;
        this.booksCompleted = response.data.booksCompleted;
        this.requestPendingBookIds = response.data.booksPending.map(book => book.book_id);
        this.userBookIds = this.booksToBeCompleted.map(book => book.book_id).concat(this.booksCompleted.map(book => book.book_id));
        console.log("User Book IDs:", this.userBookIds);
        console.log("Request Pending Book IDs:", this.requestPendingBookIds);
      }).catch(error => {
        console.error(error);
      });
    },
    readReview(bookId) {
      this.$router.push({ path: '/userreadreview', query: { bookId, userId: this.username } });
    },
    clearSearch() {
      this.searchQuery = ''; // Clear the search query
      this.searchResults = []; // Clear the search results
      this.searchResultsVisible = false;
    } 
  },
  mounted() {
    this.username = localStorage.getItem('username');
    this.fetchBooks();
    this.fetchUserBooks();
  }
};
</script>

<style>
.books {
  max-width: 800px;
  margin: 50px auto;
  padding: 20px;
  border: 1px solid #e0e0e0;
  border-radius: 10px;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
  text-align: center;
}

.books h1 {
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

.book-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin: 10px 0;
  padding: 10px;
  border: 1px solid #e0e0e0;
  border-radius: 5px;
  background-color: #f9f9f9;
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

.search-filter {
  display: flex;
  justify-content: center;
  margin-bottom: 20px;
  position: relative;
}

.search-filter input {
  width: 60%;
  height: 40px;
  padding-left: 20px;
  margin-right: 10px;
  border: 1px solid skyblue;
  border-radius: 5px;
  box-sizing: border-box;
}

.search-filter button {
  height: 40px;
}

.dropdown {
  position: relative;
  display: inline-block;
}

.dropdown-content {
  display: none;
  position: absolute;
  background-color: #f9f9f9;
  min-width: 160px;
  box-shadow: 0px 8px 16px 0px rgba(0,0,0,0.2);
  z-index: 1;
}

.dropdown-content a {
  color: black;
  padding: 12px 16px;
  text-decoration: none;
  display: block;
}

.dropdown-content a:hover {background-color: #f1f1f1}

.dropdown:hover .dropdown-content {
  display: block;
}

.dropdown:hover .dropbtn {
  background-color: skyblue;
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
