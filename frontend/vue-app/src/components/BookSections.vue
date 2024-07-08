<template>
    <div class="sections">
      <h2>Sections</h2>
      <button @click="addSection">Add Section</button>
      <div v-for="section in sections" :key="section.id" class="section-item">
        <span>{{ section.name }} | {{ section.date_created }} | {{ section.description }}</span>
        <button @click="viewBooks(section)">View Books</button>
      </div>
      <div v-if="showAddSection">
        <h3>Add New Section</h3>
        <form @submit.prevent="createSection">
          <input type="text" v-model="newSection.name" placeholder="Section Name" required>
          <input type="text" v-model="newSection.description" placeholder="Description" required>
          <button type="submit">Add</button>
          <button @click="cancelAddSection">Cancel</button>
        </form>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    name: 'BookSections',
    data() {
      return {
        sections: [],
        showAddSection: false,
        newSection: {
          name: '',
          description: ''
        }
      };
    },
    methods: {
      async fetchSections() {
        try {
          const token = localStorage.getItem('token');
          console.log('Token:', token); // Debug log
          const response = await axios.get('/sections');
          console.log('Response:', response); // Debug log
          // this.sections = response.data.sections;
        } catch (error) {
          console.error('Error fetching sections:', error);
        }
      },
      addSection() {
        this.showAddSection = true;
      },
      cancelAddSection() {
        this.showAddSection = false;
        this.newSection.name = '';
        this.newSection.description = '';
      },
      async createSection() {
        try {
          const token = localStorage.getItem('token');
          console.log('Token:', token); // Debug log
          const mockResponse = {
            data: {
              section: {
                id: Date.now(),
                name: this.newSection.name,
                description: this.newSection.description,
                date_created: new Date().toISOString()
              }
            }
          };
          console.log('Mock response:', mockResponse);
          this.sections.push(mockResponse.data.section);
          this.cancelAddSection();
        } catch (error) {
          console.error('Error creating section:', error);
        }
      },
      viewBooks(section) {
        this.$router.push({ name: 'viewBooks', params: { sectionId: section.id } });
      }
    },
    mounted() {
      this.fetchSections();
    }
  };
  </script>
  
  <style>
  .sections {
    text-align: center;
  }
  
  .section-item {
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
  