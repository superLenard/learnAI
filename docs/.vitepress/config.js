import { defineConfig } from 'vitepress'

export default defineConfig({
  base: '/learnAI/',
  title: "Lenard的博客",
  description: "个人笔记博客，记录学习与思考",
  // 在这里添加配置，关闭标题旁边的 # 锚链接标记
  markdown: {
    anchor: {
      permalink: false
    },
    // 启用数学公式渲染（$...$ 行内、$$...$$ 独立行，基于 markdown-it-mathjax3）
    math: true
  },
  // 页面头部元信息
  head: [
    ['link', { rel: 'icon', type: 'image/svg+xml', href: '/learnAI/favicon.svg' }],
    ['link', { rel: 'icon', type: 'image/x-icon', href: '/learnAI/favicon.ico' }],
    ['script', { id: 'MathJax-script', async: '', src: 'https://cdn.jsdelivr.net/npm/mathjax@3/es5/tex-mml-chtml.js' }]
  ],

  themeConfig: {
    siteTitle: "Lenard · 个人博客",
    outline: { level: [2,4], label: '本章目录' },
    // 底部分页文案
    docFooter: {
      prev: '上一页',
      next: '下一页'
    },
    sidebar: [
      {
        text: '📖 AI 学习笔记',
        items: [
          // { text: '首页', link: '/' },
          { text: '第一章：学习路线', link: '/01-roadmap' },
          {
            text: '第二章：大语言模型原理',
            link: '/llm-principles/',
            collapsed: false,
            items: [
              { text: '2.1 大语言模型的演变', link: '/llm-principles/01-evolution' },
              { text: '2.2 核心思想：预测下一个词', link: '/llm-principles/02-next-word' },
              { text: '2.3 Token 与分词器', link: '/llm-principles/03-tokenizer' },
              { text: '2.4 Transformer 机制', link: '/llm-principles/04-transformer' },
              { text: '2.5 预训练与规模效应', link: '/llm-principles/05-pretraining' },
              { text: '2.6 上下文机制与 KV Cache', link: '/llm-principles/06-context' },
              { text: '2.7 主流模型与开源生态', link: '/llm-principles/07-models' },
              { text: '2.8 动手：跑一个小模型', link: '/llm-principles/08-hands-on' },
              { text: '2.9 小结', link: '/llm-principles/09-summary' }
            ]
          },
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