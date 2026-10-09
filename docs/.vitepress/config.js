import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/learnAI/',
  title: "Lenard的博客",
  description: "个人笔记博客，记录学习与思考",
  // 在这里添加配置，关闭标题旁边的 # 锚链接标记
  markdown: {
    anchor: {
      permalink: false
    }
  },
  // 页面头部元信息
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/learnAI/favicon.svg' }],
    ['link', { rel: 'icon', type: 'image/x-icon', href: '/learnAI/favicon.ico' }]
  ],

  themeConfig: {
    siteTitle: "Lenard · 个人博客",
    outline: { level: [2,4], label: '本章目录' },
    sidebar: [
      {
        text: '📖 AI学习笔记',
        items: [
          // { text: '首页', link: '/' },
          { text: '第一章：起步', link: '/01-start' },
          // { text: '第二章：动效演示', link: '/02-animation' }
        ]
      }
    ],
    nav: [
      { text: '笔记合集', link: 'https://superlenard.github.io/myblog/' },
    ],
    // GitHub 右上角链接
    socialLinks: [
      { icon: 'github', link: 'https://github.com/superLenard' }
    ],
  }
})