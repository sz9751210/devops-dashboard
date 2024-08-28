<template>
  <el-dialog
    :title="isEditing ? '編輯文件' : '新增文件'"
    :model-value="isVisible"
    @update:model-value="updateVisibility"
  >
    <el-form :model="document" label-width="80px">
      <el-form-item label="文件名">
        <el-input v-model="document.title" />
      </el-form-item>
      <el-form-item label="作者">
        <el-select v-model="document.author" placeholder="請選擇">
          <el-option
            v-for="author in authors"
            :key="author"
            :label="author"
            :value="author"
          />
        </el-select>
      </el-form-item>
      <el-form-item label="日期">
        <el-date-picker
          v-model="document.date"
          type="date"
          placeholder="選擇日期"
          value-format="YYYY-MM-DD"
        />
      </el-form-item>
      <el-form-item label="目錄">
        <el-select v-model="document.folderId" placeholder="選擇目錄">
          <el-option
            v-for="folder in getLeafFolders(directoryTree)"
            :key="folder._id"
            :label="folder.label"
            :value="folder._id"
          ></el-option>
        </el-select>
      </el-form-item>
      <el-form-item label="內容">
        <!-- Markdown 編輯器 -->
        <v-md-editor
          v-model="document.content"
          :disabled-menus="[]"
          @upload-image="handleUploadImage"
        />
      </el-form-item>
    </el-form>
    <el-button type="primary" @click="save">確定</el-button>
  </el-dialog>
</template>

<script>
import VMdEditor from "@kangc/v-md-editor";

export default {
  components: {
    VMdEditor,
  },
  props: {
    isVisible: Boolean,
    document: Object,
    isEditing: Boolean,
    authors: Array,
    directoryTree: Array,
  },
  methods: {
    updateVisibility(val) {
      this.$emit("update:isVisible", val);
    },
    save() {
      this.$emit("save-document");
    },
    handleUploadImage(event, insertImage, files) {
      this.$emit("upload-image", event, insertImage, files);
    },
    getLeafFolders(nodes) {
      let result = [];
      for (let node of nodes) {
        if (!node.children || node.children.length === 0) {
          result.push({ _id: node._id, label: node.label });
        } else {
          result = result.concat(this.getLeafFolders(node.children));
        }
      }
      return result;
    },
  },
};
</script>
