<template>
    <div class="requests">
      <h2>Requests</h2>
      <div v-for="request in requests" :key="request.id" class="request-item">
        <span>{{ request.book.title }} | Requested by: {{ request.user.username }} | Status: {{ request.status }}</span>
        <button @click="grantRequest(request)">Grant</button>
        <button @click="rejectRequest(request)">Reject</button>
      </div>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    name: 'LibrarianRequests',
    data() {
      return {
        requests: []
      };
    },
    methods: {
      async fetchRequests() {
        try {
          const token = localStorage.getItem('token');
          const response = await axios.get('/requests', {
            headers: { Authorization: `Bearer ${token}` }
          });
          this.requests = response.data.requests;
        } catch (error) {
          console.error(error);
        }
      },
      async grantRequest(request) {
        try {
          const token = localStorage.getItem('token');
          await axios.post(`/requests/${request.id}/grant`, {}, {
            headers: { Authorization: `Bearer ${token}` }
          });
          this.fetchRequests();
        } catch (error) {
          console.error(error);
        }
      },
      async rejectRequest(request) {
        try {
          const token = localStorage.getItem('token');
          await axios.post(`/requests/${request.id}/reject`, {}, {
            headers: { Authorization: `Bearer ${token}` }
          });
          this.fetchRequests();
        } catch (error) {
          console.error(error);
        }
      }
    },
    mounted() {
      this.fetchRequests();
    }
  };
  </script>
  
  <style>
  .requests {
    text-align: center;
  }
  
  .request-item {
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
  