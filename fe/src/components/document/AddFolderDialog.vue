<template>
  <el-dialog
    title="新增目錄"
    :model-value="isVisible"
    @update:model-value="updateVisibility"
    :before-close="beforeClose"
  >
    <el-form label-width="80px">
      <el-form-item label="父目錄">
        <el-select
          :model-value="selectedParentFolderId"
          placeholder="選擇父目錄"
          @update:model-value="updateSelectedParentFolderId"
        >
          <el-option :label="'無父目錄'" :value="null"></el-option>
          <el-option
            v-for="folder in getAllFolders(directoryTree)"
            :key="folder._id"
            :label="folder.label"
            :value="folder._id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="目錄名稱">
        <el-input
          :model-value="folderName"
          @update:model-value="updateFolderName"
          placeholder="輸入目錄名稱"
        ></el-input>
      </el-form-item>
    </el-form>
    <el-button type="primary" @click="saveFolder">確定</el-button>
  </el-dialog>
</template>

<script>
export default {
  props: {
    directoryTree: Array,
    isVisible: Boolean,
    selectedParentFolderId: String,
    folderName: String,
  },
  methods: {
    getAllFolders(nodes) {
      let result = [];
      for (let node of nodes) {
        result.push({ _id: node._id, label: node.label });
        if (node.children && node.children.length > 0) {
          result = result.concat(this.getAllFolders(node.children));
        }
      }
      return result;
    },
    saveFolder() {
      this.$emit("save-folder", {
        name: this.folderName,
        parentId: this.selectedParentFolderId,
      });
    },
    beforeClose(done) {
      this.$emit("before-close", done);
    },
    updateVisibility(val) {
      this.$emit("update:isVisible", val);
    },
    updateSelectedParentFolderId(val) {
      this.$emit("update:selectedParentFolderId", val);
    },
    updateFolderName(val) {
      this.$emit("update:folderName", val);
    },
  },
};
</script>
