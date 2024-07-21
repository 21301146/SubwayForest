import Vue from 'vue'
import Router from 'vue-router'
import home from '@/views/home';

import login from '@/views/components/login.vue'
import register from '@/views/components/register.vue'

Vue.use(Router)

const router = new Router({
    routes: [
        {
            path: '/',
            redirect: '/login'
        },
        {
            path: '/login',
            name: 'login',
            component: login
        },
        {
            path: '/register',
            name: 'register',
            component: register
        },
        {
            path: '',
            name: 'home',
            component: home,
            children: [
                {
                    path: '/page2',
                    name: 'page2',
                    component: () => import('@/views/page2')
                }
            ]
        }
    ]
})
export default router
