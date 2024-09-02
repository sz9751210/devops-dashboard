<template>
  <el-table :data="currentFiles" style="width: 100%">
    <el-table-column prop="title" label="文件名" />
    <el-table-column prop="author" label="作者" />
    <el-table-column prop="date" label="日期" />
    <el-table-column label="操作">
      <template v-slot="scope">
        <!-- 包裝按鈕組的容器，並設置為垂直排列 -->
        <div class="button-group">
          <!-- 第一行的按鈕 -->
          <div class="button-row">
            <el-button
              class="action-button"
              size="small"
              type="primary"
              v-if="showOperations"
              @click="editDocument(scope.row)"
              >編輯</el-button
            >
            <el-popconfirm
              title="是否刪除這份文件?"
              @confirm="confirmDelete(scope.row._id)"
            >
              <template #reference>
                <el-button
                  class="action-button"
                  size="small"
                  type="danger"
                  v-if="showOperations"
                  >刪除</el-button
                >
              </template>
            </el-popconfirm>
          </div>
          <!-- 第二行的按鈕 -->
          <div class="button-row">
            <el-button
              class="action-button"
              size="small"
              @click="previewDocument(scope.row)"
              type="primary"
              >Detail</el-button
            >
            <!-- 新增查看歷史按鈕 -->
            <el-button
              class="action-button"
              size="small"
              type="info"
              @click="viewHistory(scope.row)"
              >查看歷史</el-button
            >
          </div>
        </div>
      </template>
    </el-table-column>
  </el-table>
</template>

<script>
export default {
  props: {
    currentFiles: Array,
    showOperations: Boolean,
  },
  methods: {
    editDocument(document) {
      this.$emit("edit-document", document);
    },
    confirmDelete(documentId) {
      this.$emit("confirm-delete", documentId);
    },
    previewDocument(document) {
      this.$emit("preview-document", document);
    },
    viewHistory(document) {
      // 觸發父組件中的 fetch-document-history 事件，並傳遞 document._id
      this.$emit("fetch-document-history", document._id);
    },
  },
};
</script>

<style scoped>
.button-group {
  display: flex;
  flex-direction: column;
  gap: 4px; /* 調整兩行之間的距離 */
}

.button-row {
  display: flex;
  gap: 4px; /* 調整按鈕之間的距離 */
}

.action-button {
  margin-right: 1px;
}
</style>
