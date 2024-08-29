<template>
  <div class="sidebar">
    <!-- 操作按鈕區域 -->
    <div class="button-group">
      <div class="button-row">
        <el-button type="primary" icon="plus" @click="openAddFolderDialog">
          新增目錄
        </el-button>

        <el-button
          type="warning"
          icon="edit"
          @click="toggleEditMode"
          :disabled="!currentFolder"
          v-if="directoryTree.length > 0 && currentFolder && showOperations"
        >
          {{ editMode ? "完成編輯" : "編輯目錄" }}
        </el-button>
      </div>

      <div
        v-if="
          editMode &&
          showOperations &&
          currentFolder &&
          directoryTree.length > 0
        "
        class="button-row"
      >
        <el-button
          icon="edit-pen"
          type="primary"
          @click="openRenameFolderDialog"
          :disabled="!currentFolder"
        >
          重命名目錄
        </el-button>

        <!-- 使用 Popconfirm 包裹刪除按鈕 -->
        <div style="display: flex; align-items: center">
          <el-popconfirm
            :title="`確定要刪除目錄「${
              currentFolder ? currentFolder.label : ''
            }」嗎？`"
            confirm-button-text="確定"
            cancel-button-text="取消"
            @confirm="deleteCurrentFolder"
          >
            <template #reference>
              <el-button
                icon="folder-delete"
                type="danger"
                :disabled="!currentFolder"
              >
                刪除目錄
              </el-button>
            </template>
          </el-popconfirm>
        </div>
      </div>
    </div>

    <!-- 分隔線 -->
    <el-divider />

    <!-- 目錄列表 -->
    <el-tree
      :data="directoryTree"
      :props="defaultProps"
      @node-click="handleNodeClick"
      class="directory-tree"
      highlight-current
    ></el-tree>
  </div>
</template>

<script>
export default {
  props: {
    directoryTree: Array,
    currentFolder: Object,
    showOperations: Boolean,
    editMode: Boolean,
  },
  methods: {
    openAddFolderDialog() {
      this.$emit("open-add-folder-dialog");
    },
    toggleEditMode() {
      this.$emit("toggle-edit-mode");
    },
    openRenameFolderDialog() {
      this.$emit("open-rename-folder-dialog");
    },
    deleteCurrentFolder() {
      this.$emit("delete-current-folder");
    },
    handleNodeClick(node) {
      this.$emit("node-click", node);
    },
  },
};
</script>

<style scoped>
.sidebar {
  width: 250px;
  margin-right: 20px;
  display: flex;
  flex-direction: column;
}

.divider {
  height: 2px;
  background-color: #dcdfe6;
  margin-bottom: 10px;
}

.directory-tree {
  flex-grow: 1;
  overflow-y: auto;
}

.button-row {
  display: flex;
  justify-content: space-between;
}

.button-group {
  display: flex;
  flex-direction: column;
  gap: 10px; /* 將按鈕組之間的距離設定為 10px */
  margin-bottom: 10px;
}

.el-button {
  width: 110px; /* 固定按鈕寬度 */
  height: 35px; /* 固定按鈕高度 */
}
</style>
