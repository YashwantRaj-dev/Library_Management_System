<template>
  <div class="requests">
    <button @click="goBack" class="go-back">Go Back</button>
    <h2>List Of Requests</h2>
    <div v-for="request in requests" :key="request.id" class="request-item">
      <span>{{ request.book_title }} | {{ request.book_author }} | {{ request.book_section }} | Requested by: {{ request.username }} | Status: {{ request.status }}</span>
      <div>
        <button @click="grantRequest(request)">Grant</button>
        <button @click="rejectRequest(request)">Reject</button>
      </div>
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
        const response = await axios.get('http://localhost:5000/requests', {
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
        alert(`Access granted to ${request.username}`);
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
    },
    goBack() {
      this.$router.go(-1);
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
  align-items: center;
}

.request-item div {
  display: flex;
  gap: 10px;
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
