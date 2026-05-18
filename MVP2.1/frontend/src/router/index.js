/**
 * router/index.js - Vue Router配置
 * 定义所有页面路由、路由守卫、导航行为。
 */
import { createRouter, createWebHistory } from 'vue-router'

// 布局组件（立即加载，因为每个页面都用）
import AppLayout from '../layouts/AppLayout.vue'

// 页面组件（懒加载，访问时才下载）
const MemoryCorridor = () => import('../views/MemoryCorridor.vue')
const IdeaFreeze = () => import('../views/IdeaFreeze.vue')
const HealingSpace = () => import('../views/HealingSpace.vue')
const PrivateUniverse = () => import('../views/PrivateUniverse.vue')
const LoginView = () => import('../views/LoginView.vue')

// 路由配置
const routes = [
  {
    path: '/login',
    name: 'Login',
    component: LoginView,
    meta: { public: true, title: '登录' }  // public=true表示无需登录
  },
  {
    path: '/',
    component: AppLayout,  // 所有需要登录的页面共享此布局
    redirect: '/corridor', // 访问/自动跳转到记忆长廊
    children: [
      {
        path: 'corridor',
        name: 'MemoryCorridor',
        component: MemoryCorridor,
        meta: { title: '记忆长廊', icon: '\u{1F5BC}', navKey: 'corridor' }
      },
      {
        path: 'editor',
        name: 'IdeaFreeze',
        component: IdeaFreeze,
        meta: { title: '想法定格', icon: '\u{270D}', navKey: 'editor' }
      },
      {
        path: 'healing',
        name: 'HealingSpace',
        component: HealingSpace,
        meta: { title: '疗愈空间', icon: '\u{1F3B5}', navKey: 'healing' }
      },
      {
        path: 'universe',
        name: 'PrivateUniverse',
        component: PrivateUniverse,
        meta: { title: '私人宇宙', icon: '\u{1F30C}', navKey: 'universe' }
      },
    ]
  },
  // 404 fallback
  {
    path: '/:pathMatch(.*)*',
    redirect: '/corridor'
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes,
  scrollBehavior() {
    // 切换路由时滚动到顶部
    return { top: 0 }
  }
})

// ========== 路由守卫 ==========
// 暂用模拟用户，Phase 2接入真实JWT
const MOCK_LOGGED_IN = true  // TODO: Phase 2改为从localStorage读token判断

router.beforeEach((to, from, next) => {
  // 设置页面标题
  document.title = to.meta.title ? `${to.meta.title} - MemChain` : 'MemChain'
  
  // 公开页面直接放行
  if (to.meta.public) {
    next()
    return
  }
  
  // 其他页面暂时全部放行（Phase 2接入真实JWT后再做权限检查）
  next()
})

export default router