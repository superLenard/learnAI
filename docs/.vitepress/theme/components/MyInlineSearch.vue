<script setup>
import { shallowRef, ref, onMounted, onBeforeUnmount, watch } from 'vue'
import { computedAsync } from '@vueuse/core'
import MiniSearch from 'minisearch'
import localSearchIndex from '@localSearchIndex'
import { useRouter, useData } from 'vitepress'

// 真正的内联搜索：输入框常驻导航栏“笔记合集”左侧，
// 点击/打字直接在本框输入，结果以下拉列表显示，无弹出面板、无快捷键说明。

const { localeIndex, theme } = useData()
const router = useRouter()

const root = ref()
const input = ref()
const query = ref('')
const results = ref([])
const showList = ref(false)
const selected = ref(-1)

const index = computedAsync(async () => {
  const locale = localeIndex.value || ''
  const loader = localSearchIndex[locale] || localSearchIndex[Object.keys(localSearchIndex)[0]]
  const data = (await loader?.())?.default
  if (!data) return null
  return MiniSearch.loadJSON(data, {
    fields: ['title', 'titles', 'text'],
    storeFields: ['title', 'titles'],
    searchOptions: {
      fuzzy: 0.2,
      prefix: true,
      boost: { title: 4, text: 2, titles: 1 },
      ...(theme.value.search?.provider === 'local' &&
        theme.value.search.options?.miniSearch?.searchOptions)
    },
    ...(theme.value.search?.provider === 'local' &&
      theme.value.search.options?.miniSearch?.options)
  })
})

// 输入变化（键入 / 粘贴 / 中文输入法选词）即搜索；
// 索引异步加载完成后也会对当前词补搜一次
watch([query, index], () => {
  const q = query.value.trim()
  if (!index.value || !q) {
    results.value = []
    showList.value = false
    return
  }
  results.value = index.value.search(q).slice(0, 16)
  selected.value = results.value.length ? 0 : -1
  showList.value = true
})

function onKey(e) {
  if (e.key === 'ArrowDown') {
    e.preventDefault()
    if (results.value.length) selected.value = (selected.value + 1) % results.value.length
  } else if (e.key === 'ArrowUp') {
    e.preventDefault()
    if (results.value.length) selected.value = (selected.value - 1 + results.value.length) % results.value.length
  } else if (e.key === 'Enter') {
    go(results.value[selected.value])
  } else if (e.key === 'Escape') {
    showList.value = false
    query.value = ''
    input.value?.blur()
  }
}

function go(r) {
  if (!r) return
  router.go(r.id)
  showList.value = false
  query.value = ''
  input.value?.blur()
}

function onFocus() {
  if (query.value.trim()) showList.value = true
}

function onDocClick(e) {
  if (!root.value?.contains(e.target)) showList.value = false
}

onMounted(() => document.addEventListener('click', onDocClick))
onBeforeUnmount(() => document.removeEventListener('click', onDocClick))
</script>

<template>
  <div class="my-inline-search" ref="root">
    <input
      ref="input"
      v-model="query"
      type="search"
      placeholder="搜索"
      aria-label="搜索"
      class="my-inline-input"
      autocomplete="off"
      autocorrect="off"
      autocapitalize="off"
      spellcheck="false"
      maxlength="64"
      @keydown="onKey"
      @focus="onFocus"
    />
    <ul v-if="showList && results.length" class="my-inline-results" role="listbox">
      <li v-for="(r, i) in results" :key="r.id" role="option" :aria-selected="selected === i">
        <a
          class="my-inline-result"
          :class="{ selected: selected === i }"
          :href="r.id"
          @mousedown.prevent="go(r)"
        >
          <span class="crumb">{{ Array.isArray(r.titles) ? r.titles.join(' › ') : (r.titles || '') }}</span>
          <span class="main">{{ r.title }}</span>
        </a>
      </li>
    </ul>
  </div>
</template>

<style scoped>
.my-inline-search {
  position: relative;
  display: flex;
  align-items: center;
  /* 与导航项间距（VPNavBarMenuLink padding 0 12px，相邻项 24px）保持一致 */
  margin-right: 24px;
}
.my-inline-input {
  width: 16px;
  padding: 6px 12px;
  font-size: 14px;
  line-height: 1.4;
  color: var(--vp-c-text-1);
  /* 半透明玻璃背景，适配站点雾团渐变底色 */
  background: rgba(30, 41, 59, 0.35);
  border: 1px solid rgba(148, 163, 184, 0.18);
  border-radius: 8px;
  outline: none;
  -webkit-backdrop-filter: blur(10px) saturate(1.1);
  backdrop-filter: blur(10px) saturate(1.1);
  transition: border-color 0.25s, background 0.25s;
}
.my-inline-input:focus {
  border-color: var(--vp-c-brand-1);
  background: rgba(51, 65, 85, 0.5);
}
:root:not(.dark) .my-inline-input {
  background: rgba(255, 255, 255, 0.5);
  border-color: rgba(148, 163, 184, 0.3);
}
:root:not(.dark) .my-inline-input:focus {
  background: rgba(255, 255, 255, 0.68);
}
.my-inline-results {
  position: absolute;
  top: calc(100% + 8px);
  left: 0;
  width: 300px;
  max-height: min(58vh, 480px);
  overflow-y: auto;
  margin: 0;
  padding: 6px;
  list-style: none;
  /* 半透明玻璃背景，与输入框/站点底色协调 */
  background: rgba(30, 41, 59, 0.55);
  border: 1px solid var(--vp-c-divider);
  border-radius: 10px;
  -webkit-backdrop-filter: blur(16px) saturate(1.1);
  backdrop-filter: blur(16px) saturate(1.1);
  box-shadow: 0 16px 48px rgba(0, 0, 0, 0.22);
  z-index: 300;
}
:root:not(.dark) .my-inline-results {
  background: rgba(255, 255, 255, 0.62);
}
.my-inline-result {
  display: flex;
  flex-direction: column;
  gap: 2px;
  padding: 8px 10px;
  border-radius: 6px;
  color: var(--vp-c-text-1);
  text-decoration: none !important;
  cursor: pointer;
}
.my-inline-result.selected {
  background: var(--vp-c-default-soft, rgba(128, 128, 128, 0.1));
}
.my-inline-result .crumb {
  font-size: 12px;
  color: var(--vp-c-text-3, rgba(128, 128, 128, 0.6));
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
.my-inline-result .main {
  font-size: 13px;
  font-weight: 500;
  overflow: hidden;
  white-space: nowrap;
  text-overflow: ellipsis;
}
@media (min-width: 960px) {
  .my-inline-input { width: 160px; }
}
@media (max-width: 767px) {
  .my-inline-search { display: none !important; }  /* 移动端不显示 */
}
</style>
