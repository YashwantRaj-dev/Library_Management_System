<template>
  <div class="dashboard">
    <h1>{{ username }}'s Dashboard</h1>
    <nav class="navbar">
      <router-link :to="{ path: '/userdashboard', query: { username: username } }" :class="{ active: isActive('/userdashboard') }">My Books</router-link>
      <router-link :to="{ path: '/userbooks', query: { username: username } }" :class="{ active: isActive('/userbooks') }">Books</router-link>
      <router-link :to="{ path: '/userprofile', query: { username: username } }" :class="{ active: isActive('/userprofile') }">Profile</router-link>
      <a @click="logout">Logout</a>
    </nav>
    <div v-if="section === 'mybooks'">
      <div class="search-filter">
        <input 
          type="text" 
          :placeholder="`Search by ${searchType}`" 
          v-model="searchQuery"
        >
        <button @click="filterCombinedBooks">Filter</button>
        <div class="dropdown">
          <button class="dropbtn">Search by</button>
          <div class="dropdown-content">
            <a @click="setSearchType('Book Title')">Book Title</a>
            <a @click="setSearchType('Author\'s name')">Author's name</a>
            <a @click="setSearchType('Section/Genre')">Section/Genre</a>
            <!-- <a @click="setSearchType('Rating')">Rating</a> -->
          </div>
        </div>
        <button @click="clearSearch">Clear Result</button>
      </div>
      <div class="search-results" v-if="searchQuery && filteredBooks.length">
        <h2>Search Results</h2>
        <div v-for="book in filteredBooks" :key="book.book_id" class="book-item">
          <span>{{ book.title }} | {{ book.author }} | {{ book.section }}</span>
        </div>
      </div>
      <h2>Books to be Completed</h2>
      <div v-for="book in filteredBooksToBeCompleted" :key="book.book_id" class="book-item">
        <span>{{ book.title }} | {{ book.author }} | {{ book.section }}</span>
        <div>
          <button @click="readBook(book)">Read</button>
          <button @click="markComplete(book)">Mark Complete</button>
        </div>
      </div>
      <h2>Books Completed</h2>
      <div v-for="book in filteredBooksCompleted" :key="book.book_id" class="book-item">
        <span>{{ book.title }} | {{ book.author }} | {{ book.section }}</span>
        <div>
          <button @click="readBook(book)">Read</button>
          <button @click="giveFeedback(book)">Give Feedback</button>
        </div>
      </div>
    </div>
  </div>
</template>

  
  <script>
  import axios from '../axios';
  
  export default {
    name: 'UserDashboard',
    data() {
      return {
        username: '',
        section: 'mybooks',
        searchQuery: '',
        searchType: 'Book Title',
        booksToBeCompleted: [],  // Sample data, replace with API call
        booksCompleted: [],  // Sample data, replace with API call,
        filteredBooks: []
      };
    },
    computed: {
      filteredBooksToBeCompleted() {
        console.log("BTB",this.booksToBeCompleted);
        return this.filterBooks(this.booksToBeCompleted);
      },
      filteredBooksCompleted() {
        console.log("BTB2",this.booksCompleted);
        return this.filterBooks(this.booksCompleted);
      } 
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
      async updateBookRequests() {
        try {
          await axios.put('http://localhost:5000/update_book_requests');
          console.log('Book requests updated successfully');
        } catch (error) {
          console.error('Error updating book requests:', error);
        }
      },
      readBook(book)
      {
        console.log(book.book_id);
        this.$router.push({ path: '/read', query: { bookId: book.book_id, username: this.username } });
      },
      markComplete(book){
        axios.post(`http://localhost:5000/books/${book.book_id}/complete`, { username: this.username })
        .then(() => {
          alert('Book marked as completed');
          this.fetchBooks();
        })
        .catch(error => console.error(error));
      }, 
      giveFeedback(book) {
        this.$router.push({ path: `/userfeedback`, query: { bookId: book.book_id, username: this.username } });
      },
      setSearchType(type) {
        this.searchType = type;
      },
      filterCombinedBooks() {
        if (!this.searchQuery.trim()) {
          this.filteredBooks = [];  // Clear search results if query is empty
          return;
        }

        const combinedBooks = [...this.booksToBeCompleted, ...this.booksCompleted];

        this.filteredBooks = combinedBooks.filter(book => {
          if (this.searchType === 'Book Title') {
            return book.title && book.title.toLowerCase().includes(this.searchQuery.toLowerCase());
          } else if (this.searchType === 'Author\'s name') {
            return book.author && book.author.toLowerCase().includes(this.searchQuery.toLowerCase());
          } else if (this.searchType === 'Section/Genre') {
            return book.section && book.section.toLowerCase().includes(this.searchQuery.toLowerCase());
          } else if (this.searchType === 'Rating') {
            return book.rating && book.rating.toString().includes(this.searchQuery);
          }
          return false;
        });
      },
      filterBooks(books) {
        console.log("Inside", this.booksCompleted); 
        if (!Array.isArray(books)) return []; 
        return books.filter(book => {
      if (this.searchType === 'Book Title') {
        return book.title && book.title.toLowerCase().includes(this.searchQuery.toLowerCase());
      } else if (this.searchType === 'Author\'s name') {
        return book.author && book.author.toLowerCase().includes(this.searchQuery.toLowerCase());
      } else if (this.searchType === 'Section/Genre') {
        return book.section && book.section.toLowerCase().includes(this.searchQuery.toLowerCase());
      } else if (this.searchType === 'Rating') {
        return book.rating && book.rating.toString().includes(this.searchQuery);
      }
      return false;
        });
      },
      fetchBooks() {
        axios.get(`http://localhost:5000/users/books`, { params: { username: this.username } })
        .then(response => {
          this.booksToBeCompleted = response.data.booksToBeCompleted || [];
          console.log("abc",this.booksToBeCompleted); 
          this.booksCompleted = response.data.booksCompleted || [];
          this.filteredBooks = this.filterBooks([...this.booksToBeCompleted, ...this.booksCompleted]);
        })
        .catch(error => console.error(error));
      },
      clearSearch() {
        this.searchQuery = '';
        this.filteredBooks = [];
        this.fetchBooks();
        },
    },  
    mounted() {
      this.username = localStorage.getItem('username');
      this.fetchBooks();
      this.updateBookRequests(); 
    }
  };
  </script>
  
  <style>
  .dashboard {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
  }
  
  .dashboard h1 {
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
  </style>
  