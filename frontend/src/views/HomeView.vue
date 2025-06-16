<template>
  <!-- 導覽列 -->
  <NavBar title="選擇地圖" />
  <div class="esports-bg text-white min-vh-100 py-5">
  <!-- 地圖卡片清單 -->
  <div class="container">
    <!-- 一般用戶地圖 -->
    <h4 class="mb-4 fw-bold text-info esports-title">🎮 選擇地圖</h4>
    <div class="row g-4 mb-5">
      <div 
        v-for="map in maps" 
        :key="map" 
        class="col-sm-6 col-md-4 col-lg-3"
      >
        <div class="card esports-card text-center" @click="goToMap(map)" style="cursor: pointer;">
          <img :src="`/cover/${map.toLowerCase()}.jpg`" class="card-img-top" :alt="map">
          <div class="card-body text-center">
            <h5 class="card-title text-info">{{ map }}</h5>
          </div>  
        </div>
      </div>
    </div>

    <!-- ✅ 僅限 admin 顯示 -->
    <div v-if="admin_session">
      <h5 class="text-danger fw-bold mb-3">👮 管理員專區</h5>
      <div class="row">
        <div 
          v-for="ad in adm" 
          :key="ad" 
          class="col-sm-6 col-md-4 col-lg-3"
        >
          <div class="card esports-card text-center" @click="goToAdmin(ad)" style="cursor: pointer;">
            <img :src="`/cover/${ad.toLowerCase()}.jpg`" class="card-img-top" :alt="ad">
            <div class="card-body text-center">
              <h5 class="card-title fw-bold text-danger">待審核投擲</h5>
            </div>  
          </div>
        </div>
      </div>
    </div>
  </div>
  </div>  
</template>

<script>
import NavBar from '@/components/NavBar.vue'
import { useUserStore } from '@/stores/user'
export default {
  components: { NavBar },
  data() {
    return {
      maps: ['Dust2', 'Mirage','Inferno','Anubis','Ancient','Nuke','Train'], // 地圖池
      adm :['admin'],// 管理方法
      
    };
  },

  computed: {
    // ✅ 計算屬性來決定是否為管理員
    admin_session() {
      const userStore = useUserStore()
      return userStore.isLoggedIn && userStore.role === 'admin'
    }
  },

  methods: {
    goToMap(map) {
      this.$router.push(`/map/${map}`);
    },

    goToAdmin() {
      this.$router.push(`/admin`);
    }
  }
}
</script>
<style scoped>
.card:hover {
  transform: translateY(-4px);
  transition: all 0.2s ease-in-out;
  box-shadow: 0 0 10px rgba(0, 0, 0, 0.2);
}


.esports-bg {
  background: linear-gradient(135deg, #0d1117, #1a1f2b);
  font-family: 'Orbitron', sans-serif;
}

.esports-title {
  border-left: 5px solid #0dcaf0;
  padding-left: 12px;
  text-shadow: 0 0 5px #0dcaf0;
}

.esports-card {
  background-color: #1e2734;
  border: 1px solid #2c384a;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.esports-card:hover {
  transform: scale(1.05);
  box-shadow: 0 0 15px #0dcaf0;
}

</style>
