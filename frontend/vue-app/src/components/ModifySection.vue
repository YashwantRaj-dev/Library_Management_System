<template>
    <div>
      <h1>Modify Section</h1>
      <div>
        <input v-model="sectionName" placeholder="Section Name" />
        <input v-model="sectionDescription" placeholder="Section Description" />
        <button @click="modifySection">Modify Section</button>
      </div>
      <button @click="goBack">Go Back</button>
    </div>
  </template>
  
  <script>
  import axios from '../axios';
  
  export default {
    data() {
      return {
        sectionName: '',
        sectionDescription: '',
        sectionId: this.$route.query.sectionid
      };
    },
    created() {
      this.fetchSectionDetails();
    },
    methods: {
      async fetchSectionDetails() {
        try {
          const response = await axios.get(`/sections/${this.sectionId}`);
          const section = response.data.section;
          this.sectionName = section.name;
          this.sectionDescription = section.description;
        } catch (error) {
          console.error(error);
        }
      },
      async modifySection() {
        try {
          await axios.put(`/sections/${this.sectionId}`, {
            name: this.sectionName,
            description: this.sectionDescription
          });
          alert("Section Modified Successfully");
          this.$router.go(-1);
        } catch (error) {
          console.error(error);
        }
      },
      goBack() {
        this.$router.go(-1);
      }
    }
  };
  </script>
