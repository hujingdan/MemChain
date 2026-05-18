import { createApp } from 'vue'
import { createPinia } from 'pinia'
import App from './App.vue'
import router from './router'

// 全局CSS变量
import './shared/styles/variables.css'

const app = createApp(App)

app.use(createPinia())  // 注册Pinia
app.use(router)         // 注册Router

app.mount('#app')