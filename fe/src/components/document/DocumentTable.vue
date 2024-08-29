<template>
  <el-table :data="currentFiles" style="width: 100%">
    <el-table-column prop="title" label="文件名" />
    <el-table-column prop="author" label="作者" />
    <el-table-column prop="date" label="日期" />
    <el-table-column label="操作">
      <template v-slot="scope">
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
        <el-button
          class="action-button"
          size="small"
          @click="previewDocument(scope.row)"
          type="primary"
          >Detail</el-button
        >
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
  },
};
</script>

<style scoped>
.action-button {
  margin-right: 1px;
}
</style>
