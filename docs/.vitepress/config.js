import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/learnAI/',
  title: "Leonard 的博客",
  description: "个人笔记博客",
  themeConfig: {
    outline: { level: [2,4], label: '本章目录' },
    sidebar: [
      {
        text: '📖 基础笔记',
        items: [
          { text: '首页', link: '/' },
          { text: '第一章：起步', link: '/01-start' },
          { text: '第二章：动效演示', link: '/02-animation' }
        ]
      }
    ],
    nav: [
      { text: '首页', link: '/' }
    ]
  }
})