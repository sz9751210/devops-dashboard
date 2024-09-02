<template>
  <el-dialog
    title="文件預覽"
    :model-value="isVisible"
    @update:model-value="updateVisibility"
    width="80%"
  >
    <el-row :gutter="20">
      <!-- 第一列：左邊顯示文件資訊，右邊顯示日期及目錄 -->
      <el-col :span="12">
        <el-form label-position="top" label-width="80px">
          <el-form-item label="文件名">
            <span class="preview-content">{{ previewDocumentData.title }}</span>
          </el-form-item>
          <el-form-item label="作者">
            <span class="preview-content">{{
              previewDocumentData.author
            }}</span>
          </el-form-item>
        </el-form>
      </el-col>
      <el-col :span="12">
        <el-form label-position="top" label-width="80px">
          <el-form-item label="日期">
            <span class="preview-content">{{ previewDocumentData.date }}</span>
          </el-form-item>
          <el-form-item label="目錄">
            <span class="preview-content">{{
              previewDocumentData.folderName
            }}</span>
          </el-form-item>
        </el-form>
      </el-col>
    </el-row>
    <el-divider />
    <!-- 內容顯示區，添加固定高度和捲動條 -->
    <el-form label-position="top" class="content-section">
      <el-form-item label="內容">
        <v-md-preview
          class="content-preview"
          :text="previewDocumentData.content"
        ></v-md-preview>
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
import createLineNumbertPlugin from "@kangc/v-md-editor/lib/plugins/line-number/index";
import createCopyCodePlugin from "@kangc/v-md-editor/lib/plugins/copy-code/index";
import "@kangc/v-md-editor/lib/plugins/copy-code/copy-code.css";

VMdPreview.use(githubTheme, { Hljs: hljs })
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

<style scoped>
.preview-content {
  font-weight: 500;
  color: #333;
}

.content-section {
  margin-top: 20px;
}

.content-preview {
  padding: 10px;
  box-shadow: rgba(0, 0, 0, 0.24) 0px 3px 8px;
  background-color: #fff; /* 增加背景顏色，確保陰影效果清晰 */
}

</style>
