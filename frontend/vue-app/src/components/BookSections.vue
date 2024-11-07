<template>
  <div>
    <h1>Book Sections</h1>
    <div>
      <input v-model="newSectionName" placeholder="Section Name" />
      <input v-model="newSectionDescription" placeholder="Section Description" />
      <button @click="addSection">Add Section</button>
    </div>
    <div v-if="sections.length">
      <h2>List of Sections</h2>
      <ul>
        <li v-for="section in sections" :key="section.id">
          <div style="display: flex; justify-content: space-between;">
            <div>{{ section.name }} - {{ section.description }}</div>
            <div>
              <button @click="viewUploadBooks(section.id)">View/Upload Books</button>
              <button @click="modifySection(section.id)">Modify</button>
              <button @click="deleteSection(section.id)">Delete</button>
            </div>
          </div>
        </li>
      </ul>
    </div>
    <div v-else>
      No sections available
    </div>
    <button @click="goBack">Go Back</button>
  </div>
</template>

<script>
import axios from '../axios';

export default {
  data() {
    return {
      sections: [],
      newSectionName: '',
      newSectionDescription: '',
    };
  },
  created() {
    this.fetchSections();
  },
  methods: {
    async fetchSections() {
      try {
        const response = await axios.get('/sections');
        this.sections = response.data;
      } catch (error) {
        console.error(error);
      }
    },
    async addSection() {
      try {
        await axios.post('/sections', {
          name: this.newSectionName,
          description: this.newSectionDescription,
        });
        this.newSectionName = '';
        this.newSectionDescription = '';
        this.fetchSections();
      } catch (error) {
        console.error(error);
      }
    },
    async deleteSection(sectionId) {
      try {
        await axios.delete(`/sections/${sectionId}`);
        this.fetchSections();
      } catch (error) {
        console.error(error);
      }
    },
    viewUploadBooks(sectionId) {
      this.$router.push({ path: '/section/books', query: { sectionid: sectionId } });
    },
    modifySection(sectionId) {
      this.$router.push({ path: '/modify-section', query: { sectionid: sectionId } });
    },
    goBack() {
      this.$router.go(-1);
    }
  }
};
</script>
