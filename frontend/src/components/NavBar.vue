<template>
  <nav class="navbar bg-dark border-bottom border-body" data-bs-theme="dark">
    <div class="container-fluid">
      <span class="navbar-brand fw-bold fs-5 fst-italic text-warning" href="#">{{ title }}</span>
      <ul class="navbar-nav me-auto mb-2 mb-lg-0">
        <li class="nav-item">
          <a class="nav-link active" aria-current="page" href="/"> 首頁</a>
        </li>
      </ul>
      
      <div class="d-flex align-items-center">
        <template v-if="userStore.isLoggedIn">
          <span class="text-info me-3">👤 {{ userStore.username }}</span>
          <button class="btn btn-outline-light btn-sm" @click="logout">登出</button>
        </template>
        <template v-else>
          <button class="btn btn-warning btn-sm" @click="showSignUp = true">註冊</button>
          <button class="btn btn-outline-light btn-sm" @click="showLogin = true">登入</button>
        </template>
      </div>
    </div>
  </nav>

  <LoginModal 
      :show="showLogin"
      @close="showLogin = false"
      @login="handleLogin"
  />

  <SignUp 
      :show="showSignUp"
      @close="showSignUp = false"
      @signup="handleSignUp"
  />
</template>

<script>
import { useUserStore } from '@/stores/user'
import LoginModal from './LoginModal.vue'
import { ref,onMounted } from 'vue'
import axios from 'axios'
import { useRouter,useRoute  } from 'vue-router'
import SignUp from './SignUp.vue'



export default {
  name: 'NavBar',
  props: {
    title: {
      type: String,
      default: ''
    }
  },
  components: { LoginModal, SignUp },

  setup() {
    const showLogin = ref(false)
    const showSignUp = ref(false)
    const userStore = useUserStore()
    const router = useRouter() //提供改變路由的各種方法
    const route = useRoute() //拿到 當前路由資訊

    onMounted(() => {
      axios.get('/me', { withCredentials: true })
        .then(res => {
          if (res.data.success) {
            userStore.login(res.data.username, res.data.role)
          } else {
            userStore.logout()
          }
        })
    })

    const handleLogin = ({ username, password }) => {
      axios.post('/login', { username, password }, { withCredentials: true })
        .then(res => {
          if (res.data.success) {
            userStore.login(res.data.username, res.data.role)
            showLogin.value = false
            showSignUp.value = false
            router.push(`/`)
          } else {
            alert('帳號或密碼錯誤')
          }
        })
    }
    
    const handleSignUp = ({ username, password }) => {
      axios.post('/signup', { username, password }, { withCredentials: true })
        .then(res => {
          if (res.data.success) {
            alert('註冊成功')
            location.reload()
          } else {
            alert('帳號已存在')
          }
        })
    }

    const logout = () => {
      axios.post('/logout', {}, { withCredentials: true })
        .then(() => {
          userStore.logout()
          if(route.path.startsWith('/admin')){
            router.push(`/`)
          }
          else{
            router.push(`/`)
          }
        })
    }

    return {
      showLogin,
      showSignUp,
      userStore,
      handleSignUp,
      handleLogin,
      logout
    }
  }
}
</script>

  

<style scoped>

.nav-link {
  font-size: 20px;
  text-decoration: none;
  color: #8b0aed;
  font-weight: bold;
  margin-left: 12px;
}


.nav-link:first-child {
  margin-left: 0;
}
</style>
