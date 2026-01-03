import { createRouter, createWebHistory } from 'vue-router'
import MapDetail from '../views/MapDetail.vue'
import HomeView from '../views/HomeView.vue'
import AdminView from '../views/AdminView.vue'

const routes = [
  {
    path: '/',
    name: 'home',
    component: HomeView
  },
  {
    path: '/map/:mapName',
    name: 'MapDetail',
    component: MapDetail,
    props: true
  },
  {
    path: '/admin',
    name: 'Admin',
    component: AdminView
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
