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
import VMdPreview from "@kangc/v-md-editor/lib/preview";
import "@kangc/v-md-editor/lib/style/preview.css";
import githubTheme from "@kangc/v-md-editor/lib/theme/github.js";
import "@kangc/v-md-editor/lib/theme/style/github.css";
import hljs from "highlight.js";

import createLineNumbertPlugin from '@kangc/v-md-editor/lib/plugins/line-number/index';

import createCopyCodePlugin from '@kangc/v-md-editor/lib/plugins/copy-code/index';
import '@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css';

VMdPreview
  .use(githubTheme, { Hljs: hljs })
  .use(createLineNumbertPlugin())
  .use(createCopyCodePlugin());

export default {
  components: {
    VMdPreview,
  },
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
