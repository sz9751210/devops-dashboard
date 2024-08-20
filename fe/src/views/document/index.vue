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
      <el-radio-group v-model="addFolderLevel">
        <el-radio label="root">根目錄</el-radio>
        <el-radio label="current" :disabled="!currentFolder">當前目錄</el-radio>
      </el-radio-group>
      <el-input v-model="newFolderName" placeholder="輸入目錄名稱"></el-input>
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
      </el-form>
      <el-button type="primary" @click="saveDocument">確定</el-button>
    </el-dialog>
  </div>
</template>

<script>
import {
  fetchDocuments,
  fetchDocumentDetail,
  createDocument,
  updateDocument,
  deleteDocument,
  fetchFolders,
  createFolder as apiCreateFolder,
  updateFolder as apiUpdateFolder,
  deleteFolder as apiDeleteFolder,
} from "@/api/document";

export default {
  data() {
    return {
      directoryTree: [], // 目錄樹的結構數據
      currentFolder: null, // 當前選中的目錄
      currentFiles: [], // 當前目錄中的文件列表
      newFolderName: "",
      renameFolderName: "",
      folderToRename: null,
      newDocument: {
        title: "",
        author: "",
        date: "",
        folderId: null, // 文件所在的目錄 ID
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
        this.directoryTree = response.data.map((folder) => ({
          ...folder,
          files: folder.files || [], // 如果後端沒有提供 `files` 屬性，則默認設置為空數組
        }));
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
    },
    async createFolder() {
      try {
        const newFolder = {
          label: this.newFolderName,
          parentId:
            this.addFolderLevel === "current" && this.currentFolder
              ? this.currentFolder._id
              : null,
        };
        await apiCreateFolder(newFolder);

        // this.directoryTree.push(response.data);
        // 在成功創建目錄後，重新調用 fetchFolders 來刷新目錄樹
        this.fetchFolders();
        this.showAddFolderDialog = false;
        this.newFolderName = "";
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
        await apiUpdateFolder(this.currentFolder._id, updatedFolder);
        this.currentFolder.label = this.renameFolderName;
        this.showRenameFolderDialog = false;
      } catch (error) {
        console.error("Error renaming folder:", error);
      }
    },
    async deleteCurrentFolder() {
      try {
        await apiDeleteFolder(this.currentFolder._id);
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
        folderId: this.currentFolder ? this.currentFolder._id : null,
        originalFolderId: null,
      };
      this.showAddDocumentDialog = true;
    },
    async editDocument(document) {
      try {
        this.isEditing = true;
        const response = await fetchDocumentDetail(document._id);
        this.newDocument = response.data;
        this.newDocument.originalFolderId = this.currentFolder._id;
        this.showAddDocumentDialog = true;
      } catch (error) {
        console.error("Error fetching document details:", error);
      }
    },
    async saveDocument() {
      try {
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
  },
};
</script>

<style scoped>
.document-page {
  display: flex;
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
