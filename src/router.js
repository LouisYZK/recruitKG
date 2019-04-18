// import Vue from 'vue'
// import Router from 'vue-router'
import VueDemo from '@/components/VueDemo'
import Messages from '@/components/Messages'

// Vue.use(Router)

// export default new Router({
//   routes: [
//     {
//       path: '/',
//       name: 'home',
//       component: VueDemo
//     },
//     {
//       path: '/messages',
//       name: 'messages',
//       component: Messages
//     }
//   ]
// })

export default [
  {
       // 配置路由，当路径为'/activePublic',使用组件activePublic
       path:'/home', component: VueDemo,
 },
 {
   path:'/messages', component: Messages
 }
]
