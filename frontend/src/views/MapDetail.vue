<template>
  <NavBar :title="`${mapName} - 道具教學`" />
  <div class="esports-bg text-white min-vh-100 py-5">

  <!-- 主頁面容器 --> 
  <div class="container py-4 text-white esports-bg position-relative">
    <!-- 地圖圖像 + 工具列區塊 -->
    <div class="card esports-card p-3 bg-dark mb-4 position-relative">
      <!-- 工具列（嵌入地圖卡片上方） -->
      <div class="d-flex justify-content-between align-items-center flex-wrap gap-2 mb-3">
        <div class="d-flex align-items-center">
          <label for="grenadeSelect" class="form-label text-light me-2 mb-0">選擇道具：</label>
          <select id="grenadeSelect" class="form-select bg-dark text-light border-secondary w-auto" v-model="selectedGrenade">
            <option disabled value="">請選擇道具</option>
            <option v-for="type in grenadeTypes" :key="type">{{ type }}</option>
          </select>
        </div>
        <!-- 新增點位丟法按鈕 -->
        <div class="d-flex gap-2">
          <button 
            v-if="selectedGrenade && account_session" 
            class="btn btn-outline-info" 
            :class="{ active: isAddP}" 
            @click="isAddP = true; selectedMethodPanelVisible = false;showAddForm = false"
            >➕ 新增點位丟法
          </button>
          <button
            v-if="selectedPoint && account_session"
            class="btn btn-outline-warning "
            :class="{ active: showAddForm}"
            @click="showAddForm = true; selectedMethodPanelVisible = false;isAddP = false"
          >
            ➕ 新增丟法
          </button>
        </div>
      </div>

      <!-- 地圖圖像與標記 -->
      <div class="position-relative mx-auto" style="max-width: 800px">
        <img 
          :src="`/maps/${mapName.toLowerCase()}.png`" 
          class="img-fluid"
          @click="MapClick"
        />
        <!-- 點位渲染 -->
        <button
          v-for="(point, index) in points"
          :key="index"
          class="btn btn-info position-absolute translate-middle marker "
          :class="{ active: selectedPoint?.name === point.name }"
          :style="{ left: point.x + 'px', top: point.y + 'px' }"
          @click="selectUsagePoint(point)"
          :title="point.name"
        >📍</button>
        <button
          v-if="tempxy && tempxy.x !== undefined && tempxy.y !== undefined"
          class="position-absolute translate-middle marker-temp"
          :style="{ left: tempxy.x + 'px', top: tempxy.y + 'px'}"
          :title="暫存點"
          disabled
        >📌</button>
        
      </div>
    </div>

    <!-- 點位丟法表單 -->
    <div v-if="showAddPForm && tempxy.x !== undefined" class="position-fixed top-50 start-50 translate-middle bg-dark text-white p-4 rounded shadow-lg">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="text-info">新增點位丟法</h5>
        <button class="btn-close btn-close-white" @click="showAddPForm = false"></button>
      </div>
      <input class="form-control mb-2" v-model="newPostionName" placeholder="點位名稱" />
      <input class="form-control mb-2" v-model="newMethodName" placeholder="丟法名稱" />
      <input class="form-control mb-2" v-model="newMethodURL" placeholder="影片網址" />
      <div class="d-flex gap-2">
        <button class="btn btn-success" @click="submitNewPostionMethod()">送出</button>
        <button class="btn btn-secondary" @click="cancel_npm()">取消</button>
      </div>
    </div>

    <!-- 丟法新增表單 -->
    <div v-if="showAddForm" class="position-fixed top-50 start-50 translate-middle bg-dark text-white p-4 rounded shadow-lg">
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="text-info">新增丟法：{{ selectedPoint.name }}</h5>
        <button class="btn-close btn-close-white" @click="showAddForm = false"></button>
      </div>
      <input class="form-control mb-2" v-model="newMethodName" placeholder="丟法名稱" />
      <input class="form-control mb-2" v-model="newMethodURL" placeholder="影片網址" />
      <div class="d-flex gap-2">
        <button class="btn btn-success" @click="submitNewMethod">送出</button>
        <button class="btn btn-secondary" @click="showAddForm = false">取消</button>
      </div>
    </div>

    <!-- 彈出式丟法選單 -->
    <div 
      v-if="selectedPoint && selectedPoint.methods.length > 1 && selectedMethodPanelVisible"
      class="position-fixed top-50 start-50 translate-middle bg-dark text-white p-4 rounded shadow-lg"
      style="z-index: 1050; min-width: 300px"
    >
      <div class="d-flex justify-content-between align-items-center mb-3">
        <h5 class="text-info mb-0">選擇丟法：{{ selectedPoint.name }}</h5>
        <button class="btn-close btn-close-white" @click="selectedMethodPanelVisible = false"></button>
      </div>
      <select class="form-select" v-model="selectedMethod" @change="fetchVideoFromPoint">
        <option disabled value="">請選擇丟法</option>
        <option v-for="m in selectedPoint.methods" :key="m.name" :value="m.video_url">
          {{ m.name }}
        </option>
      </select>
    </div>

    <!-- 影片播放區 -->
    <div v-if="videoUrl" class="card bg-dark text-white p-3 mb-4">
      <h5 class="text-info mb-3">🎮 影片播放</h5>
      <div class="ratio ratio-16x9">
        <template v-if="embedInfo.type === 'iframe'">
          <iframe
            :src="embedInfo.src"
            allowfullscreen
          ></iframe>
        </template>
        <template v-else>
          <video class="w-100" controls :src="embedInfo.src"></video>
        </template>
      </div>
    </div>
  </div>

  <div>
    <!-- 當聊天室被關閉，顯示右下角按鈕 -->
    <button
      v-if="!showChat"
      class="btn btn-secondary position-fixed bottom-0 end-0 m-3 z-3"
      @click="showChat = true"
    >
      顯示聊天室
    </button>

    <!-- 聊天室元件 -->
    <ChatRoom
      v-if="showChat"
      :mapName="mapName"
      :username="username"
      @close="showChat = false"
    />
  </div>
  </div>
</template>


<script>
import NavBar from '@/components/NavBar.vue'
import ChatRoom from '@/components/ChatRoom.vue'
import { useUserStore } from '@/stores/user'
import axios from 'axios';
export default {
  components: { NavBar,ChatRoom },
  props: ['mapName'],
  data() {
    return {
      selectedGrenade: '',        // 目前還可保留（可加切換類型功能）
      selectedPoint: null,        // 使用者點選的點位（包含名稱與 methods）
      selectedMethod: '',         // 被選中的影片網址
      videoUrl: '',               // 真正播放的影片 URL
      points:[],
      selectedMethodPanelVisible: false,
      grenadeTypes: ['smoke', 'flash', 'molotov'],
      tempxy:null,
      isAddP:false,
      showAddPForm: false,
      showAddForm: false,
      showChat: true,
      newMethodName: '',
      newMethodURL: '',
    };
  },

  
  watch: {
    selectedGrenade(newVal) {
        if (newVal) {
        // 根據目前選的地圖與道具，向後端取得點位資訊
        axios.get(`/maps/${this.mapName}/${newVal}/points`)
            .then(res => {
            this.points = res.data;
            this.selectedPoint = null;
            this.selectedMethod = '';
            this.videoUrl = '';
            this.tempxy=null;
            this.isAddP=false;
            this.showAddPForm= false;
            this.showAddForm=false;
            })
            .catch(err => {
            console.error('載入點位失敗：', err);
            });
        } else {
        this.points = [];
        }
    }
  },
  
  computed: {
    // ✅ 計算屬性來決定是否登入
    account_session() {
      const userStore = useUserStore()
      return userStore.isLoggedIn && ( userStore.role === 'admin' || userStore.role === 'user')
    },
    username(){
      return useUserStore().username
    }
    embedInfo() {
      return this.getEmbedInfo(this.videoUrl)
    }
    
  },

  methods: {
    selectUsagePoint(point) {
        this.selectedPoint = point;
        this.selectedUsage = '';
        this.videoUrl = '';
        this.showAddForm = false;
        this.showAddPForm = false;
        this.newPostionName = ''
        this.newMethodName = '';
        this.newMethodURL = '';
        this.isAddP=false;
        this.selectedMethodPanelVisible = point.methods?.length > 1;

        // 多種丟法 => 顯示選單
        if (point.methods.length > 1) {
            this.usages = point.methods;
            this.tempxy = null
            }
        // 一種丟法 => 直接顯示影片
        else if (point.methods.length === 1) {
            this.videoUrl = point.methods[0].video_url;
            this.tempxy = null
        }
    },
    
    isYoutube(url) {
        return url.includes('youtube.com') || url.includes('youtu.be');
    },
    embedYoutube(url) {
        if (url.includes('/shorts/')) {
        const id = url.split('/shorts/')[1].split('?')[0];
        return `https://www.youtube.com/embed/${id}`;
        } else if (url.includes('watch?v=')) {
        const id = url.split('watch?v=')[1].split('&')[0];
        return `https://www.youtube.com/embed/${id}`;
        } else if (url.includes('youtu.be/')) {
        const id = url.split('youtu.be/')[1].split('?')[0];
        return `https://www.youtube.com/embed/${id}`;
        } else {
        return ''; // 無效網址處理
        }
    },
    
    getEmbedInfo(url) {
        if (!url) return { type: 'none', src: '' };
    
        // ✅ YouTube (含 Shorts / youtu.be)
        if (url.includes('youtube.com') || url.includes('youtu.be')) {
          let id = '';
          if (url.includes('youtu.be/')) {
            id = url.split('youtu.be/')[1].split('?')[0];
          } else if (url.includes('/shorts/')) {
            id = url.split('/shorts/')[1].split('?')[0];
          } else if (url.includes('v=')) {
            id = new URL(url).searchParams.get('v');
          }
          return {
            type: 'iframe',
            src: `https://www.youtube.com/embed/${id}`
          };
        }
    
        // ✅ Instagram
        if (url.includes('instagram.com')) {
          if (url.endsWith('/')) url = url.slice(0, -1);
          return {
            type: 'iframe',
            src: `${url}/embed`
          };
        }
    
        // ✅ TikTok
        if (url.includes('tiktok.com')) {
          const match = url.match(/video\/(\d+)/);
          if (match) {
            return {
              type: 'iframe',
              src: `https://www.tiktok.com/embed/v2/${match[1]}`
            };
          }
        }
    
        // ✅ 其他當成本地影片
        return { type: 'video', src: url };
      }
    }
    
    fetchVideoFromPoint() {
      this.videoUrl = this.selectedMethod;
      this.selectedMethodPanelVisible = false;
    },

    submitNewMethod() {
        if (!this.newMethodName || !this.newMethodURL) {
            alert('請填寫完整資訊');
            return;
        }

        const payload = {
            map: this.mapName,
            grenade_type: this.selectedGrenade,
            point_name: this.selectedPoint.name,
            x: this.selectedPoint.x,
            y: this.selectedPoint.y,
            method: {
            name: this.newMethodName,
            video_url: this.newMethodURL
            }
        };

        axios.post('/submit_method', payload)
            .then(() => {
            alert('送出成功，等待審核');
            this.showAddForm = false;
            this.newMethodName = '';
            this.newMethodURL = '';
            })
            .catch(err => {
            console.error('送出失敗', err);
            alert('發生錯誤，請稍後再試');
            });
    },

    MapClick(event){
      if (!this.isAddP) return;
      this.showAddForm = false;
      this.showAddPForm = true;
      this.videoUrl=''
      const rect = event.target.getBoundingClientRect();
      const x = Math.round(event.clientX - rect.left);
      const y = Math.round(event.clientY - rect.top);
      this.tempxy = {x,y}
      this.selectedPoint=null
    },
    cancel_npm(){
      this.tempxy = null;
      this.showAddPForm = false;
      this.isAddP=false;
    },
    submitNewPostionMethod() {
        if (!this.newPostionName||!this.newMethodName || !this.newMethodURL) {
            alert('請填寫完整資訊');
            return;
        }
        const {x,y} = this.tempxy
        const payload = {
            map: this.mapName,
            grenade_type: this.selectedGrenade,
            point_name: this.newPostionName,
            x,
            y,
            method: {
            name: this.newMethodName,
            video_url: this.newMethodURL
            }
        };

        axios.post('/submit_method', payload)
            .then(() => {
            alert('送出成功，等待審核');
            this.isAddP=false;
            this.tempxy=null;
            this.showAddPForm = false;
            this.newPostionName = '';
            this.newMethodName = '';
            this.newMethodURL = '';
            })
            .catch(err => {
            console.error('送出失敗', err);
            alert('發生錯誤，請稍後再試');
            });
    }
  }
};
</script>

<style scoped>

.esports-card {
  background-color: #1e2734;
  border: 1px solid #2c384a;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
  cursor: pointer;
}

.esports-bg {
  background: linear-gradient(135deg, #0d1117, #1a1f2b);
  font-family: 'Orbitron', sans-serif;
}

.marker {
  width: 28px;
  height: 28px;
  background-color: #68a4ff4b;
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  font-size: 16px;
  color: white;
  box-shadow: 0 0 8px rgba(1, 124, 238, 0.878);
  cursor: pointer;
  display: flex;
  justify-content: center;
  align-items: center;
  transition: all 0.2s ease-in-out;
  backdrop-filter: blur(2px);
}
.marker:hover {
  transform: scale(1.15);
  box-shadow: 0 0 12px rgba(102, 178, 255, 0.9);
}
.marker.active {
  background-color: rgba(13, 202, 240, 0.85);
  box-shadow: 0 0 16px rgba(13, 202, 240, 0.8), 0 0 8px rgba(255, 255, 255, 0.6);
}
.marker-temp {
  width: 30px;
  height: 30px;
  background-color: rgba(255, 193, 7, 0.8);
  border: 2px solid rgba(255, 255, 255, 0.8);
  border-radius: 50%;
  text-align: center;
  line-height: 20px;
  font-size: 16px;
  color: black;
  box-shadow: 0 0 5px rgba(255, 193, 7, 0.6);
  pointer-events: none;
}



</style>
