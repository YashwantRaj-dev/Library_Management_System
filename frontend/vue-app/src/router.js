import { createRouter, createWebHistory } from 'vue-router';
import AllHome from './components/AllHome.vue';
import SignUp from './components/SignUp.vue';
import UserLogin from './components/UserLogin.vue';
import UserDashboard from './components/UserDashboard.vue';
import UserBooks from './components/UserBooks.vue';
import UserProfile from './components/UserProfile.vue';
import LibrarianLogin from './components/LibrarianLogin.vue';
import AdminLogin from './components/AdminLogin.vue';
import LibrarianDashboard from './components/LibrarianDashboard.vue';
import BookSections from './components/BookSections.vue';
import LibrarianRequests from './components/LibrarianRequests.vue';
import LibrarianStats from './components/LibrarianStats.vue';
import SectionViewBook from './components/SectionViewBook.vue';
import ModifySection from './components/ModifySection.vue';
import ModifyBook from './components/ModifyBook.vue';
import LibReadBook from './components/LibReadBook.vue';
import UserReadBooks from './components/UserReadBooks.vue';
import UserFeedback from './components/UserFeedback.vue';
import UserReadReview from './components/UserReadReview.vue';

const routes = [
  { path: '/', name: 'allhome', component: AllHome },
  { path: '/login', name: 'login', component: UserLogin },
  { path: '/signup', name: 'signup', component: SignUp },
  { path: '/librarian-login', name: 'librarian-login', component: LibrarianLogin },
  { path: '/admin-login', name: 'admin-login', component: AdminLogin },
  { path: '/userdashboard', name: 'userdashboard', component: UserDashboard, meta: { requiresAuth: true } },
  { path: '/userbooks', name: 'userbooks', component: UserBooks, meta: { requiresAuth: true } },
  { path: '/userprofile', name: 'userprofile', component: UserProfile, meta: { requiresAuth: true } },
  { path: '/librarian-dashboard', name: 'librarian-dashboard', component: LibrarianDashboard, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/librarian-booksections', name: 'booksections', component: BookSections, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/librarian-requests', name: 'librarianrequests', component: LibrarianRequests, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/librarian-stats', name: 'librarianstats', component: LibrarianStats, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/section/books', name: 'sectionviewbook', component: SectionViewBook, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/modify-section', name: 'modifysection', component: ModifySection, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/modify-book', name: 'modifybook', component: ModifyBook, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/read-book', name: 'readbook', component: LibReadBook, meta: { requiresAuth: true, role: 'librarian' } },
  { path: '/read', name: 'UserReadBooks', component: UserReadBooks, meta: { requiresAuth: true } },
  { path: '/userfeedback', name: 'UserFeedback', component: UserFeedback, meta: { requiresAuth: true } },
  { path: '/userreadreview', name: 'UserReadReview', component: UserReadReview, meta: { requiresAuth: true }}

];

const router = createRouter({
  history: createWebHistory(),
  routes
});

router.beforeEach((to, from, next) => {
  const requiresAuth = to.matched.some(record => record.meta.requiresAuth);
  const token = localStorage.getItem('token');
  const userRole = localStorage.getItem('role');

  if (requiresAuth && !token) {
    next({ name: 'login' });
  } else if (to.meta.role && to.meta.role !== userRole) {
    next({ name: 'login' });
  } else {
    next();
  }
});

export default router;
