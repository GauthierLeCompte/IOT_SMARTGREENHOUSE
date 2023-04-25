import Vue from 'vue'
import VueRouter from 'vue-router'
import GreenhouseDashboard from "@/components/GreenhouseDashboard";

Vue.use(VueRouter)

const routes = [
  {
    path: '/greenhousedashboard',
    name: 'GreenhouseDashboard',
    component: GreenhouseDashboard
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
