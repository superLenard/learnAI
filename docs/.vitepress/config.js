import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/learnAI/',  // 👈新增这一行！！仓库名称，前后斜杠不能少
  title: "Leonard 的博客",
  description: "个人笔记博客",
  themeConfig: {
    outline: { level: [2,4], label: '本章目录' },
    sidebar: [
      {
        text: '📖 基础',
        items: [
          { text: '首页', link: '/' }
        ]
      }
    ],
    nav: [
      { text: '首页', link: '/' }
    ]
  }
})