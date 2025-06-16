<template>
  <div class="modal fade show d-block" v-if="show" tabindex="-1" style="background: rgba(0, 0, 0, 0.5);">
    <div class="modal-dialog modal-dialog-centered">
      <div class="modal-content">
        <!-- 標題列 -->
        <div class="modal-header">
          <h5 class="modal-title">註冊</h5>
          <button type="button" class="btn-close" @click="$emit('close')"></button>
        </div>

        <!-- 表單區 -->
        <div class="modal-body">
          <div class="mb-3">
            <label class="form-label">帳號</label>
            <input v-model="username" type="text" class="form-control" placeholder="請輸入帳號" />
          </div>

          <div class="mb-3">
            <label class="form-label">密碼</label>
            <input v-model="password" type="password" class="form-control" placeholder="請輸入密碼" />
          </div>

          <div v-if="error" class="alert alert-danger">{{ error }}</div>

          <div class="d-grid gap-2">
            <button class="btn btn-primary" @click="signup">送出</button>
            <button class="btn btn-secondary" @click="$emit('close')">取消</button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  props: {
    show: {
      type: Boolean,
      required: true
    }
  },
  data() {
    return {
      username: '',
      password: '',
      error: ''
    };
  },
  methods: {
    signup() {
      this.error = "";
      this.$emit('signup', {
        username: this.username,
        password: this.password
      });
      this.username = '';
      this.password = '';
    }
  }
};
</script>

<style scoped>
/* 修正 Bootstrap Modal 因 v-if 無動畫的情況 */
.modal {
  z-index: 1050;
}
</style>
