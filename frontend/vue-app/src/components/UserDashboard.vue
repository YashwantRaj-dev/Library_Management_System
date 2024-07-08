<template>
    <div class="dashboard">
      <h1>{{ username }}'s Dashboard</h1>
      <nav class="navbar">
        <router-link to="/userdashboard" :class="{ active: isActive('/userdashboard') }">My Books</router-link>
        <router-link to="/userbooks" :class="{ active: isActive('/userbooks') }">Books</router-link>
        <router-link to="/userprofile">Profile</router-link>
        <a @click="logout">Logout</a>
      </nav>
      <div v-if="section === 'mybooks'">
        <div class="search-filter">
          <input 
            type="text" 
            :placeholder="`Search by ${searchType}`" 
            v-model="searchQuery"
          >
          <button @click="filterBooks">Filter</button>
          <div class="dropdown">
            <button class="dropbtn">Search by</button>
            <div class="dropdown-content">
              <a @click="setSearchType('Book Title')">Book Title</a>
              <a @click="setSearchType('Author\'s name')">Author's name</a>
              <a @click="setSearchType('Section/Genre')">Section/Genre</a>
              <a @click="setSearchType('Rating')">Rating</a>
            </div>
          </div>
        </div>
        <h2>Current Books</h2>
        <div v-for="book in filteredCurrentBooks" :key="book.id" class="book-item">
          <span>{{ book.title }} | {{ book.author }} | {{ book.section }}</span>
          <button @click="confirmReturn(book)">Return</button>
        </div>
        <h2>Completed Books</h2>
        <div v-for="book in filteredCompletedBooks" :key="book.id" class="book-item">
          <span>{{ book.title }} | {{ book.author }} | {{ book.section }}</span>
          <button @click="viewBook(book)">View</button>
        </div>
        <h2>Historical Books</h2>
        <div v-for="book in filteredHistoricalBooks" :key="book.id" class="book-item">
          <span>{{ book.title }} | {{ book.author }} | {{ book.section }}</span>
          <button @click="giveFeedback(book)">Feedback</button>
        </div>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: 'UserDashboard',
    data() {
      return {
        username: '',
        section: 'mybooks',
        searchQuery: '',
        searchType: 'Book Title',
        currentBooks: [],  // Sample data, replace with API call
        completedBooks: [],  // Sample data, replace with API call
        historicalBooks: []  // Sample data, replace with API call
      };
    },
    computed: {
      filteredCurrentBooks() {
        return this.filterBooks(this.currentBooks);
      },
      filteredCompletedBooks() {
        return this.filterBooks(this.completedBooks);
      },
      filteredHistoricalBooks() {
        return this.filterBooks(this.historicalBooks);
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
      confirmReturn(book) {
        if (confirm('Do you want to return this book?')) {
          this.currentBooks = this.currentBooks.filter(b => b.id !== book.id);
          console.log(`Returned book: ${book.title}`);
        }
      },
      viewBook(book) {
        console.log(`Viewing book: ${book.title}`);
      },
      giveFeedback(book) {
        console.log(`Giving feedback for book: ${book.title}`);
      },
      setSearchType(type) {
        this.searchType = type;
      },
      filterBooks(books) {
        return books.filter(book => {
          if (this.searchType === 'Book Title') {
            return book.title.toLowerCase().includes(this.searchQuery.toLowerCase());
          } else if (this.searchType === 'Author\'s name') {
            return book.author.toLowerCase().includes(this.searchQuery.toLowerCase());
          } else if (this.searchType === 'Section/Genre') {
            return book.section.toLowerCase().includes(this.searchQuery.toLowerCase());
          } else if (this.searchType === 'Rating') {
            return book.rating && book.rating.toString().includes(this.searchQuery);
          }
          return false;
        });
      }
    },
    mounted() {
      this.username = localStorage.getItem('username');
      // Fetch books from API
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
  