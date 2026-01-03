<template>
  <div class="chat-room-sidebar bg-dark text-white d-flex flex-column">
    <div class="chat-header d-flex justify-content-between align-items-center p-2 border-bottom">
      <h5 class="mb-0">{{ mapName }} 聊天室</h5>
      <button class="btn btn-outline-light btn-sm" @click="$emit('close')">隱藏聊天室</button>
    </div>

    <!-- 聊天訊息區塊，可滾動，不會撐大畫面 -->
     
    <div class="flex-grow-1 overflow-auto p-2 border-bottom chat-messages" ref="chatContainer">
        <!-- 每一則訊息 -->
        <div v-for="(msg, index) in messages" :key="index" class="d-flex align-items-start mb-2" :ref="index === messages.length - 1 ? 'lastMessage' : null">
            <!-- 左側頭像：使用者名稱首字母 -->
            <div class="avatar bg-success text-white rounded-circle d-flex justify-content-center align-items-center me-2" style="width: 32px; height: 32px;">
                {{ msg.username.charAt(0).toUpperCase() }}
            </div>
            <!-- 訊息本體 -->
            <div class="flex-grow-1">
            <!-- 使用者名稱與時間 -->
                <div class="d-flex justify-content-between small text-muted">
                    <strong class="text-light">{{ msg.username }}</strong>
                    <span style="color: #cccccc">{{ formatTime(msg.timestamp) }}</span>
                </div>
                <!-- 訊息內容 -->
                <div class="text-white">{{ msg.message }}</div>
            </div>
        </div>
      
    </div>

    <!-- 下方輸入區域（包含輸入框與傳送按鈕） -->
      <div class="p-2 border-top">
        <div class="input-group">
          <input
            v-model="newMessage"
            @keyup.enter="sendMessage"
            placeholder="輸入訊息..."
            class="form-control"
          />
          <button class="btn btn-primary" @click="sendMessage">傳送</button>
        </div>
    </div> 
  </div>
</template>

<script>
import { io } from "socket.io-client";

export default {
  props: {
    mapName: String, // 地圖名稱（聊天室房間）
    username: String // 使用者名稱
  },
  data() {
    return {
      socket: null,         // Socket.IO 客戶端實例
      newMessage: "",      // 當前輸入的訊息文字
      messages: []  ,        // 所有聊天室訊息資料
      justSent: false,        //剛傳送ㄉ
    };
  },
  mounted() {
    // 建立與後端的 WebSocket 連線
    this.socket = io();
    // 加入以 mapName 命名的聊天室房間
    this.socket.emit("join", { map: this.mapName });

    // 接收從後端來的訊息並顯示（不再自動捲到底）
    this.socket.on("chat", (msg) => {
      this.messages.push(msg);
      if (this.justSent){
        this.$nextTick(() => {
            this.scrollToBottom();
        });
      }
       this.justSent = false;
    });
    
    setTimeout(() => this.scrollToBottom(), 500);
    setTimeout(() => this.scrollToBottom(), 1500);
  },
  methods: {
    scrollToBottom() {
        this.$nextTick(() => {
            setTimeout(() => {
                requestAnimationFrame(() => {
                    const container = this.$refs.chatContainer;
                    if (container) {
                        container.scrollTop = container.scrollHeight;
                    }
                });
            },300);
        });
    },

    // 發送訊息至後端
    sendMessage() {
      if (!this.newMessage.trim()) return; // 空白訊息不送出
      this.socket.emit("chat", {
        map: this.mapName,
        username: this.username,
        message: this.newMessage
      });
      this.newMessage = ""; // 清空輸入欄
      this.justSent=true;
    },
    
    // 時間格式化顯示
    formatTime(timestamp) {
      const d = new Date(timestamp);
      return d.toLocaleTimeString();
    }
  }
};
</script>

<style scoped>
.chat-room-sidebar {
  position: fixed;
  top: 56px; /* 假設 navbar 高度是 56px */
  right: 0;
  width: 350px;
  height: calc(100vh - 56px);
  display: flex;
  flex-direction: column;
  z-index: 1050;
  box-shadow: -2px 0 10px rgba(0, 0, 0, 0.5);
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
}
</style>