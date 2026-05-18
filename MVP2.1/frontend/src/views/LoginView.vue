<template>
  <div class="login-page">
    <div class="login-box">
      <!-- Logo -->
      <div class="login-logo">
        <img src="/logo.png" alt="MemChain" />
        <h1>MemChain</h1>
        <p class="login-slogan">珍藏每一段不可复制的人生故事</p>
      </div>
      
      <!-- 表单 -->
      <form class="login-form" @submit.prevent="handleLogin">
        <input
          v-model="form.username"
          type="text"
          placeholder="用户名"
          class="login-input"
          required
        />
        <input
          v-model="form.password"
          type="password"
          placeholder="密码"
          class="login-input"
          required
        />
        <label class="remember-me">
          <input type="checkbox" v-model="form.remember" />
          <span>记住我</span>
        </label>
        <button type="submit" class="login-btn" :disabled="loading">
          {{ loading ? '登录中...' : '登录' }}
        </button>
      </form>
      
      <p class="login-hint">Phase 2将接入真实用户系统</p>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()
const loading = ref(false)
const form = ref({ username: '', password: '', remember: true })

function handleLogin() {
  loading.value = true
  // Phase 2接入真实登录API
  setTimeout(() => {
    loading.value = false
    router.push('/corridor')
  }, 500)
}
</script>

<style scoped>
.login-page {
  min-height: 100vh;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #E88B7C 0%, #F5A89A 50%, #E88B7C 100%);
}

.login-box {
  width: 380px;
  padding: 40px 36px;
  background: rgba(255,255,255,0.95);
  border-radius: var(--card-radius);
  box-shadow: var(--shadow-lg);
}

.login-logo {
  text-align: center;
  margin-bottom: 32px;
}

.login-logo img {
  width: 80px;
  height: 70px;
  margin-bottom: 12px;
}

.login-logo h1 {
  font-size: 28px;
  color: var(--primary-dark);
  margin-bottom: 6px;
}

.login-slogan {
  font-size: 13px;
  color: var(--text-secondary);
}

.login-form {
  display: flex;
  flex-direction: column;
  gap: 14px;
}

.login-input {
  padding: 12px 16px;
  border: 1px solid var(--border);
  border-radius: var(--input-radius);
  font-size: 15px;
  background: var(--bg-page);
  transition: border-color var(--transition-fast);
}

.login-input:focus {
  outline: none;
  border-color: var(--primary);
}

.remember-me {
  display: flex;
  align-items: center;
  gap: 8px;
  font-size: 13px;
  color: var(--text-secondary);
  cursor: pointer;
}

.login-btn {
  padding: 12px;
  background: linear-gradient(135deg, var(--primary) 0%, var(--primary-dark) 100%);
  color: white;
  border: none;
  border-radius: var(--btn-radius);
  font-size: 16px;
  font-weight: 500;
  cursor: pointer;
  transition: all var(--transition-fast);
}

.login-btn:hover {
  box-shadow: 0 4px 12px rgba(232,139,124,0.4);
}

.login-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.login-hint {
  text-align: center;
  margin-top: 20px;
  font-size: 12px;
  color: var(--text-tertiary);
}
</style>