<template>
    <el-dialog
      title="文件內容比較"
      :model-value="isVisible"
      @update:model-value="updateVisibility"
      width="80%"
    >
      <div class="header">
        <div class="header-item">歷史版本</div>
        <div class="header-item">當前版本</div>
      </div>
      <div class="content-preview">
        <!-- 使用 Diff 組件顯示差異 -->
        <Diff
          :mode="'split'"
          :theme="'light'"
          :language="'plaintext'"
          :prev="historyContent.content || ''"
          :current="currentContent.content || ''"
        />
      </div>
    </el-dialog>
  </template>
  
  <script>
  import { Diff } from "vue-diff"; // 正確引入 Diff 組件
  import "vue-diff/dist/index.css"; // 引入樣式
  
  export default {
    components: {
      Diff,
    },
    props: {
      isVisible: Boolean,
      currentContent: Object,
      historyContent: Object,
    },
    methods: {
      updateVisibility(val) {
        this.$emit("update:isVisible", val);
      },
    },
  };
  </script>
  
  <style scoped>
  .content-preview {
    display: flex;
    flex-direction: column;
    gap: 20px;
    padding: 20px;
    overflow-y: auto;
    background: #fff;
  }
  
  .header {
    display: flex;
    justify-content: space-between;
    padding: 10px 20px;
    background-color: #f0f0f0;
    border-bottom: 1px solid #ddd;
  }
  
  .header-item {
    flex: 1;
    text-align: center;
    font-weight: bold;
  }
  </style>
  