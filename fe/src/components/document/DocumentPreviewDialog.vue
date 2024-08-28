<template>
  <el-dialog
    title="文件預覽"
    :model-value="isVisible"
    @update:model-value="updateVisibility"
    width="80%"
  >
    <el-form label-position="left" label-width="100px">
      <el-form-item label="文件名">
        <span>{{ previewDocumentData.title }}</span>
      </el-form-item>
      <el-form-item label="作者">
        <span>{{ previewDocumentData.author }}</span>
      </el-form-item>
      <el-form-item label="日期">
        <span>{{ previewDocumentData.date }}</span>
      </el-form-item>
      <el-form-item label="目錄">
        <span>{{ previewDocumentData.folderName }}</span>
      </el-form-item>
      <el-form-item label="內容">
        <v-md-preview :text="previewDocumentData.content"></v-md-preview>
      </el-form-item>
    </el-form>
  </el-dialog>
</template>

<script>
export default {
  props: {
    isVisible: Boolean,
    previewDocumentData: Object,
  },
  methods: {
    updateVisibility(val) {
      this.$emit("update:isVisible", val);
    },
  },
};
</script>
