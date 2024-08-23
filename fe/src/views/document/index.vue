<template>
  <div class="document-page">
    <!-- 左側目錄區域 -->
    <div class="sidebar">
      <!-- 操作按鈕區域 -->
      <div class="button-group">
        <el-button type="primary" icon="plus" @click="openAddFolderDialog"
          >新增目錄</el-button
        >
        <el-button
          type="warning"
          icon="edit"
          @click="toggleEditMode"
          :disabled="!currentFolder"
          >{{ editMode ? "完成編輯" : "編輯目錄" }}</el-button
        >
      </div>

      <!-- 分隔線 -->
      <div class="divider"></div>

      <!-- 目錄列表 -->
      <el-tree
        :data="directoryTree"
        :props="defaultProps"
        @node-click="handleNodeClick"
        class="directory-tree"
      ></el-tree>

      <!-- 如果在編輯模式下，顯示重命名和刪除按鈕 -->
      <div v-if="editMode" class="edit-actions">
        <el-button
          type="primary"
          @click="openRenameFolderDialog"
          :disabled="!currentFolder"
          >重命名目錄</el-button
        >
        <el-button
          type="danger"
          @click="deleteCurrentFolder"
          :disabled="!currentFolder"
          >刪除目錄</el-button
        >
      </div>
    </div>

    <!-- 分隔線 -->
    <div class="vertical-divider"></div>

    <!-- 右側文件顯示區域 -->
    <div class="content">
      <div class="header">
        <el-button type="primary" icon="plus" @click="openAddDocumentDialog"
          >新增文件</el-button
        >
      </div>

      <el-table :data="currentFiles" style="width: 100%">
        <el-table-column prop="title" label="文件名" />
        <el-table-column prop="author" label="作者" />
        <el-table-column prop="date" label="日期" />
        <el-table-column label="操作">
          <template v-slot="scope">
            <el-button @click="editDocument(scope.row)">編輯</el-button>
            <el-button type="danger" @click="deleteDocument(scope.row)"
              >刪除</el-button
            >
          </template>
        </el-table-column>
      </el-table>
    </div>

    <!-- 新增目錄對話框 -->
    <el-dialog title="新增目錄" v-model="showAddFolderDialog">
      <el-form>
        <el-form-item label="父目錄">
          <el-select v-model="selectedParentFolderId" placeholder="選擇父目錄">
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
            v-model="newFolderName"
            placeholder="輸入目錄名稱"
          ></el-input>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="createFolder">確定</el-button>
    </el-dialog>

    <!-- 重命名目錄對話框 -->
    <el-dialog title="重命名目錄" v-model="showRenameFolderDialog">
      <el-input
        v-model="renameFolderName"
        placeholder="輸入新的目錄名稱"
      ></el-input>
      <el-button type="primary" @click="renameFolder">確定</el-button>
    </el-dialog>

    <!-- 新增/編輯文件對話框 -->
    <el-dialog
      :title="isEditing ? '編輯文件' : '新增文件'"
      v-model="showAddDocumentDialog"
    >
      <el-form :model="newDocument">
        <el-form-item label="文件名">
          <el-input v-model="newDocument.title" />
        </el-form-item>
        <el-form-item label="作者">
          <el-input v-model="newDocument.author" />
        </el-form-item>
        <el-form-item label="日期">
          <el-date-picker
            v-model="newDocument.date"
            type="date"
            placeholder="選擇日期"
          />
        </el-form-item>
        <el-form-item label="目錄">
          <el-select v-model="newDocument.folderId" placeholder="選擇目錄">
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
            v-model="newDocument.content"
            :disabled-menus="[]"
            @upload-image="handleUploadImage"
          />
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="saveDocument">確定</el-button>
    </el-dialog>
  </div>
</template>

<script>
import VMdEditor from "@kangc/v-md-editor";
import "@kangc/v-md-editor/lib/style/base-editor.css";
import vuepressTheme from "@kangc/v-md-editor/lib/theme/vuepress.js";
import "@kangc/v-md-editor/lib/theme/style/vuepress.css";
import zhTW from '@kangc/v-md-editor/lib/lang/zh-TW';
import Prism from "prismjs";
import {
  fetchDocuments,
  fetchDocumentDetail,
  createDocument,
  updateDocument,
  deleteDocument,
  fetchFolders,
  createFolder,
  updateFolder,
  deleteFolder,
  uploadImage,
} from "@/api/document";

// 配置 Markdown 編輯器
VMdEditor.use(vuepressTheme, {
  Prism,
});

VMdEditor.lang.use('zh-TW', zhTW);

export default {
  components: {
    VMdEditor,
  },
  data() {
    return {
      directoryTree: [], // 目錄樹的結構數據
      currentFolder: null, // 當前選中的目錄
      currentFiles: [], // 當前目錄中的文件列表
      newFolderName: "",
      renameFolderName: "",
      folderToRename: null,
      selectedParentFolderId: null, // 選擇的父目錄 ID
      newDocument: {
        title: "",
        author: "",
        date: "",
        folderId: null, // 文件所在的目錄 ID
        content: "",
        originalFolderId: null, // 用於追踪原始文件所在的目錄 ID
      },
      showAddFolderDialog: false,
      showRenameFolderDialog: false,
      showAddDocumentDialog: false,
      isEditing: false, // 是否在編輯文件
      editMode: false, // 編輯模式標識
      addFolderLevel: "root", // 默認新增根目錄
      defaultProps: {
        children: "children",
        label: "label",
      },
    };
  },
  created() {
    this.fetchFolders();
  },
  methods: {
    async fetchFolders() {
      try {
        const response = await fetchFolders();
        const flatFolders = response.data;

        // 將目錄列表轉換為樹狀結構
        const folderMap = {};
        flatFolders.forEach((folder) => {
          folder.children = [];
          folderMap[folder._id] = folder;
        });

        const treeData = [];
        flatFolders.forEach((folder) => {
          if (folder.parentId) {
            if (folderMap[folder.parentId]) {
              folderMap[folder.parentId].children.push(folder);
            }
          } else {
            treeData.push(folder);
          }
        });

        this.directoryTree = treeData;
      } catch (error) {
        console.error("Error fetching folders:", error);
      }
    },
    async handleNodeClick(node) {
      if (!node) {
        console.error("Node is null, cannot proceed.");
        this.currentFiles = []; // 設置為空數組以避免 UI 問題
        return;
      }

      this.currentFolder = node;
      // 過濾出屬於該目錄的文件
      try {
        const response = await fetchDocuments(node._id);
        this.currentFiles = response.data;
      } catch (error) {
        console.error("Error fetching documents:", error);
        this.currentFiles = [];
      }
    },
    toggleEditMode() {
      this.editMode = !this.editMode;
    },
    openAddFolderDialog() {
      this.showAddFolderDialog = true;
      // 默認選擇當前目錄作為父目錄
      this.selectedParentFolderId = this.currentFolder
        ? this.currentFolder._id
        : null;
    },
    async createFolder() {
      try {
        const newFolder = {
          label: this.newFolderName,
          parentId: this.selectedParentFolderId || null, // 使用選擇的父目錄 ID
        };

        // 調用 API 創建新目錄
        await createFolder(newFolder);

        // 刷新目錄樹，顯示新增的目錄
        await this.fetchFolders();

        // 如果新增目錄是當前選中目錄的子目錄，刷新後自動展開這個目錄
        if (this.selectedParentFolderId) {
          const updatedParentFolder = this.findFolderById(
            this.selectedParentFolderId
          );
          if (updatedParentFolder) {
            this.handleNodeClick(updatedParentFolder);
          }
        }

        this.showAddFolderDialog = false;
        this.newFolderName = "";
        this.selectedParentFolderId = null;
      } catch (error) {
        console.error("Error creating folder:", error);
      }
    },
    openRenameFolderDialog() {
      this.renameFolderName = this.currentFolder.label;
      this.showRenameFolderDialog = true;
    },
    async renameFolder() {
      try {
        const updatedFolder = {
          ...this.currentFolder,
          label: this.renameFolderName,
        };
        await updateFolder(this.currentFolder._id, updatedFolder);
        this.currentFolder.label = this.renameFolderName;
        this.showRenameFolderDialog = false;
      } catch (error) {
        console.error("Error renaming folder:", error);
      }
    },
    async deleteCurrentFolder() {
      try {
        await deleteFolder(this.currentFolder._id);
        this.directoryTree = this.directoryTree.filter(
          (folder) => folder._id !== this.currentFolder._id
        );
        this.currentFolder = null;
      } catch (error) {
        console.error("Error deleting folder:", error);
      }
    },
    openAddDocumentDialog() {
      this.isEditing = false;
      this.newDocument = {
        title: "",
        author: "",
        date: "",
        folderId: null,
        originalFolderId: null,
      };
      this.showAddDocumentDialog = true;
      // 將父目錄設為 null，允許創建根目錄或同級目錄
      this.selectedParentFolderId = null;
    },
    async editDocument(document) {
      try {
        this.isEditing = true;
        const response = await fetchDocumentDetail(document._id);
        this.newDocument = response.data;

        // 设置为文档当前的 folderId，而不是原来的 currentFolder._id
        this.newDocument.folderId = response.data.folderId;
        // this.newDocument.originalFolderId = this.currentFolder._id;
        this.showAddDocumentDialog = true;
      } catch (error) {
        console.error("Error fetching document details:", error);
      }
    },
    async saveDocument() {
      try {
        console.log("Saving document:", this.newDocument);
        if (this.isEditing) {
          await updateDocument(this.newDocument._id, this.newDocument);
        } else {
          await createDocument(this.newDocument);
        }
        this.handleNodeClick(this.currentFolder);
        this.showAddDocumentDialog = false;
      } catch (error) {
        console.error("Error saving document:", error);
      }
    },
    async deleteDocument(document) {
      try {
        await deleteDocument(document._id);
        this.currentFiles = this.currentFiles.filter(
          (file) => file._id !== document._id
        );
      } catch (error) {
        console.error("Error deleting document:", error);
      }
    },
    findFolderById(id) {
      const findInTree = (nodes) => {
        for (let node of nodes) {
          if (node._id === id) return node;
          if (node.children && node.children.length > 0) {
            const found = findInTree(node.children);
            if (found) return found;
          }
        }
        return null;
      };
      return findInTree(this.directoryTree);
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
    // 獲取所有目錄（包括子目錄）
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
    async handleUploadImage(event, insertImage, files) {
      try {
        if (!files || files.length === 0) {
          console.error("No file selected");
          return;
        }

        const file = files[0]; // 假設一次上傳一張圖片
        console.log("Uploading image:", file);

        // 構造 FormData 對象
        const formData = new FormData();
        formData.append("file", file);

        // 調用 API 上傳圖片
        const response = await uploadImage(formData);
        console.log("Image uploaded successfully:", response.data);

        // 構建圖片的完整 URL
        const imageUrl = `${window.location.origin}/api/devops/image/${response.data.image_id}`;
        console.log("Image URL:", imageUrl);

        // 將圖片 URL 插入到 Markdown 編輯器
        insertImage({
          url: imageUrl,
          desc: "DESC",
        });
      } catch (error) {
        console.error("Image upload failed:", error);
      }
    },
  },
};
</script>

<style scoped>
.document-page {
  display: flex;
  height: 100vh; /* 使页面高度占满整个视窗 */
}

.sidebar {
  width: 250px;
  margin-right: 20px;
  display: flex;
  flex-direction: column;
}

.button-group {
  display: flex;
  justify-content: space-between;
  margin-bottom: 10px;
}

.divider {
  height: 2px;
  background-color: #dcdfe6;
  margin-bottom: 10px;
}

.vertical-divider {
  width: 2px;
  background-color: #dcdfe6;
  margin-right: 20px;
  align-self: stretch;
}

.directory-tree {
  flex-grow: 1;
  overflow-y: auto;
}

.edit-actions {
  margin-top: 10px;
  display: flex;
  justify-content: space-between;
}

.content {
  flex: 1;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
</style>
