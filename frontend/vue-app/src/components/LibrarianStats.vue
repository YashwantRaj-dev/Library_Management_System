<template>
    <div class="stats">
      <h2>Statistics</h2>
      <div>
        <h3>Books Read</h3>
        <canvas id="booksReadChart"></canvas>
      </div>
      <div>
        <h3>Section Distribution</h3>
        <canvas id="sectionDistributionChart"></canvas>
      </div>
    </div>
  </template>
  
  <script>
  import { Chart } from 'chart.js';
  
  export default {
    name: 'LibrarianStats',
    data() {
      return {
        booksReadData: [12, 19, 3, 5, 2, 3],
        sectionDistributionData: [3, 10, 5, 2, 20]
      };
    },
    methods: {
      renderCharts() {
        const ctxBooksRead = document.getElementById('booksReadChart').getContext('2d');
        const ctxSectionDistribution = document.getElementById('sectionDistributionChart').getContext('2d');
  
        new Chart(ctxBooksRead, {
          type: 'bar',
          data: {
            labels: ['January', 'February', 'March', 'April', 'May', 'June'],
            datasets: [{
              label: 'Books Read',
              data: this.booksReadData,
              backgroundColor: 'skyblue'
            }]
          }
        });
  
        new Chart(ctxSectionDistribution, {
          type: 'doughnut',
          data: {
            labels: ['History', 'Science', 'Math', 'Literature', 'Art'],
            datasets: [{
              label: 'Section Distribution',
              data: this.sectionDistributionData,
              backgroundColor: ['red', 'blue', 'green', 'yellow', 'purple']
            }]
          }
        });
      }
    },
    mounted() {
      this.renderCharts();
    }
  };
  </script>
  
  <style>
  .stats {
    text-align: center;
  }
  
  canvas {
    max-width: 600px;
    margin: 20px auto;
  }
  </style>
  