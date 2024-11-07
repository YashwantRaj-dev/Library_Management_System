<template>
    <div class="feedback-form">
        <button @click="goBack" class="go-back">Go Back</button>
        <h2>Give Feedback for {{ bookTitle }}</h2>
        <div>
            <label>Rating:</label>
            <select v-model="rating">
                <option v-for="n in 5" :key="n" :value="n">{{ n }}</option>
            </select>
        </div>
        <div>
            <label>Enter Your Review:</label>
            <textarea v-model="review"></textarea>
        </div>
        <button @click="submitFeedback">Submit</button>
    </div>
</template>

<script>
import axios from '../axios';

export default {
    data() {
        return {
            bookId: this.$route.query.bookId,
            username: this.$route.query.username,
            bookTitle: '',
            rating: null,
            review: '',
        };
    },
    methods: {
        goBack() {
            this.$router.go(-1);
        },
        async fetchBookDetails() {
            try {
                const response = await axios.get(`/books/${this.bookId}`);
                const book = response.data.book;
                this.bookTitle = book.title;
            } catch (error) {
                console.error(error);
            }
        },
        async submitFeedback() {
            try {
                await axios.post(`/books/${this.bookId}/feedback`, {
                    username: this.username,
                    rating: this.rating,
                    review: this.review
                });
                alert('Feedback submitted successfully!');
                this.goBack();
            } catch (error) {
                console.error(error);
            }
        }
    },
    mounted() {
        this.fetchBookDetails();
    }
};
</script>

<style>
.feedback-form {
    max-width: 800px;
    margin: 50px auto;
    padding: 20px;
    border: 1px solid #e0e0e0;
    border-radius: 10px;
    box-shadow: 0 2px 10px rgba(0, 0, 0, 0.1);
    text-align: center;
}

.feedback-form h2 {
    margin-bottom: 30px;
    color: #333;
}

.feedback-form select, .feedback-form textarea {
    width: 100%;
    padding: 10px;
    margin: 10px 0;
    border: 1px solid #e0e0e0;
    border-radius: 5px;
}

.feedback-form button {
    background-color: #007bff;
    color: white;
    border: none;
    padding: 10px 20px;
    border-radius: 5px;
    cursor: pointer;
}

.feedback-form button:hover {
    background-color: #0056b3;
}
</style>
