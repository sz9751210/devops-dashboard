<template>
  <el-dialog
    title="重命名目錄"
    :model-value="showRenameFolderDialog"
    @update:model-value="updateShowRenameFolderDialog"
  >
    <el-input
      class="input"
      :model-value="renameFolderName"
      @update:model-value="updateRenameFolderName"
      placeholder="輸入新的目錄名稱"
    ></el-input>
    <el-button type="primary" @click="renameFolder"
      >確定</el-button
    >
  </el-dialog>
</template>

<script>
export default {
  props: {
    showRenameFolderDialog: Boolean,
    renameFolderName: String,
  },
  methods: {
    renameFolder() {
      this.$emit("rename-folder", this.renameFolderName);
    },
    updateShowRenameFolderDialog(val) {
      this.$emit("update:showRenameFolderDialog", val);
    },
    updateRenameFolderName(val) {
      this.$emit("update:renameFolderName", val);
    },
  },
};
</script>
<style scoped>
.input {
  margin-bottom: 10px; /* 在 input 元素的底部增加 5px 間隔 */
}

</style>