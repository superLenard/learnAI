import { defineConfig } from 'vitepress'

export default defineConfig({
  title: "Leonard 的博客",
  description: "个人笔记博客，左侧章节导航，右侧文章目录，支持动图",
  themeConfig: {
    // 右侧TOC目录
    outline: { level: [2,4], label: '本章目录' },
    // 左侧章节侧边栏
    sidebar: [
      {
        text: '📖 基础',
        items: [
          { text: '首页', link: '/' },
          { text: '第一章：起步', link: '/第一章-起步' }
        ]
      },
      {
        text: '✨ 多媒体示例',
        items: [
          { text: '第二章：动效演示', link: '/第二章-动效演示' }
        ]
      }
    ],
    nav: [
      { text: '首页', link: '/' }
    ]
  }
})
