import DefaultTheme from 'vitepress/theme'
import './custom.css'

// 移动端悬浮“返回顶部”按钮
function initBackTop() {
  // 防止重复创建
  if (document.querySelector('.back-top-btn')) return

  const btn = document.createElement('button')
  btn.className = 'back-top-btn'
  btn.type = 'button'
  btn.textContent = '返回顶部'
  btn.setAttribute('aria-label', '返回顶部')
  document.body.appendChild(btn)

  const update = () => btn.classList.toggle('show', window.scrollY > 400)
  window.addEventListener('scroll', update, { passive: true })
  update()

  btn.addEventListener('click', () => {
    window.scrollTo({ top: 0, left: 0, behavior: 'smooth' })
  })
}

export default {
  ...DefaultTheme,
  enhanceApp(ctx) {
    // 保留默认主题的增强（注册 Badge 组件等）
    if (typeof DefaultTheme.enhanceApp === 'function') {
      DefaultTheme.enhanceApp(ctx)
    }
    // 根组件挂载完成后初始化悬浮返回顶部按钮
    ctx.app.mixin({
      mounted() {
        if (this.$root === this) {
          initBackTop()
        }
      }
    })
  }
}
