<template>
  <NavBar title="待審核投擲教學" />

  <div class="detail-wrapper"> <!-- ✅ 包整頁，置中所有內容 -->

    <!-- 若無資料 -->
    <div v-if="pendingList.length === 0">目前沒有待審核的資料</div>

    <!-- 表格列表 -->
    <table v-else class="pending-table">
      <thead>
        <tr>
          <th>#</th>
          <th>地圖</th>
          <th>道具</th>
          <th>點位</th>
          <th>方法名稱</th>
        </tr>
      </thead>
      <tbody>
        <tr
          v-for="(item, index) in pendingList"
          :key="item.id"
          @click="selectItem(item.method.name)"
          class="table-row"
        >
          <td>{{ (page - 1) * pageSize + index + 1 }}</td>
          <td>{{ item.map }}</td>
          <td>{{ item.grenade_type }}</td>
          <td>{{ item.point_name }}</td>
          <td>
            <a href="#" @click.prevent="selectItem(item.method.name)">{{ item.method.name }}</a>
          </td>
        </tr>
      </tbody>
    </table>

    <!-- 分頁按鈕 -->
    <div class="pagination-controls">
      <button @click="prevPage" :disabled="page === 1">上一頁</button>
      <span>第 {{ page }} 頁</span>
      <button @click="nextPage" :disabled="page * pageSize >= total">下一頁</button>
    </div>

    <!-- 🔽 左右並排容器 -->
    <div v-if="selected" class="preview-flex">
        <!-- 左側：影片預覽 -->
        <div class="video-section">
            <h3>影片預覽：</h3>
            <div v-if="isYoutube(videoUrl)">
                <iframe
                    width="1080"
                    height="720"
                    :src="embedYoutube(videoUrl)"
                    frameborder="0"
                    allowfullscreen
                ></iframe>
            </div>
            <div v-else-if="videoUrl">
                <video :src="videoUrl" controls width="400" />
            </div>
        </div>

        <!-- 右側：地圖與紅點 -->
        <div class="map-section">
            <h4>地圖與丟點預覽：</h4>
            <div class="map-preview">
                <img 
                    :src="`/maps/${selected.map.toLowerCase()}.png`" alt="map" />
                <div
                    class="red-dot"
                    :style="{ left: selected.x + 'px', top: selected.y + 'px' }"
                ></div>
            </div>
        </div>
    </div>

    <div v-if="selected">
        <div class="info-block">
            <p><strong>地圖：</strong>{{ selected.map }}</p>
            <p><strong>道具：</strong>{{ selected.grenade_type }}</p>
            <p><strong>點位：</strong>{{ selected.point_name }}</p>
            <p><strong>方法名稱：</strong>{{ selected.method.name }}</p>

            <div class="actions">
                <button @click="approve(selected.id)">✅ 同意</button>
                <button @click="reject(selected.id)">❌ 拒絕</button>
            </div>
        </div>
    </div>

  </div>
</template>


<script>
import axios from "axios";
import NavBar from '@/components/NavBar.vue'
export default {
  components: { NavBar },
  name: "AdminView",
  data() {
    return {
      pendingList: [],
      selected: null,
      page: 1,
      pageSize: 10,
      total: 0,
      videoUrl: '',
    };
  },
  created() {
    this.fetchPending();
  },
  methods: {
    fetchPending() {
      axios.get(`/pending_methods_paginated?page=${this.page}&size=${this.pageSize}`)
        .then(res => {
            this.pendingList = res.data.data;
            this.total = res.data.total;
        });
    },
    nextPage() {
        if (this.page * this.pageSize < this.total) {
            this.page++;
            this.fetchPending();
        }
    },

    prevPage() {
        if (this.page > 1) {
            this.page--;
            this.fetchPending();
        }
    },

    selectItem(name) {
      axios.get(`/get_single_pending/${name}`)
        .then(res => {
            this.videoUrl=res.data.method.video_url;
            this.selected = res.data;

        })
        .catch(err => {
            console.error('無法取得影片資訊：', err);
        });
    },
    approve(id) {
      axios.post(`/approve/${id}`)
        .then(() => {
          this.fetchPending();  
          this.removeItem(id);
        });
    },
    reject(id) {
      axios.post(`/reject/${id}`)
        .then(() => {
          this.fetchPending();  
          this.removeItem(id);
        });
    },
    removeItem(id) {
      this.pendingList = this.pendingList.filter(item => item.id !== id);
      this.selected = null;
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
  }
};
</script>

<style scoped>
.detail-wrapper {
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  margin-top: 30px;
}

.pending-table {
  width: 90%;
  border-collapse: collapse;
  margin-bottom: 20px;
  text-align: center;
}

.pending-table th,
.pending-table td {
  border: 1px solid #ccc;
  padding: 12px 16px;
}

.pending-table th {
  background-color: #f9f9f9;
}

.pagination-controls {
  margin-bottom: 30px;
}

.info-block {
  margin-top: 20px;
  font-size: 16px;
  line-height: 1.8;
}

.actions {
  margin-top: 12px;
}

.actions button {
  margin: 0 10px;
  padding: 6px 12px;
  font-size: 14px;
}

.preview-flex {
  display: flex;
  justify-content: center;
  align-items: flex-start;
  gap: 40px;
  margin-top: 20px;
  flex-wrap: wrap;
}

.video-section, .map-section {
  display: flex;
  flex-direction: column;
  align-items: center;
}

.map-preview {
  position: relative;
  width: 800px;
  /*height: 500px;*/
  border: 2px solid #05597f;
}

.map-preview img {
  width: 100%;
  height: 100%;
  object-fit: contain;
}

.red-dot {
  position: absolute;
  width: 16px;
  height: 16px;
  background-color: red;
  border-radius: 50%;
  transform: translate(-50%, -50%);
  border: 2px solid black;
}

</style>
