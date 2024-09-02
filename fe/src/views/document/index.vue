<template>
  <div class="document-page">
    <!-- 左側目錄區域 -->
    <Sidebar
      :directoryTree="directoryTree"
      :currentFolder="currentFolder"
      :editMode="editMode"
      :showOperations="showOperations"
      @open-add-folder-dialog="openAddFolderDialog"
      @toggle-edit-mode="toggleEditMode"
      @open-rename-folder-dialog="openRenameFolderDialog"
      @delete-current-folder="deleteCurrentFolder"
      @node-click="handleNodeClick"
    />

    <!-- 分隔線 -->
    <div class="vertical-divider"></div>

    <!-- 右側文件顯示區域 -->
    <div class="content">
      <div class="header">
        <el-button type="primary" icon="plus" @click="openAddDocumentDialog"
          >新增文件</el-button
        >
        <el-switch
          v-model="showOperations"
          active-text="God Mode"
          inactive-text="Read Only"
          class="mode-switch"
        />
      </div>

      <DocumentTable
        :currentFiles="currentFiles"
        :showOperations="showOperations"
        @edit-document="editDocument"
        @preview-document="previewDocument"
        @confirm-delete="deleteDocument"
        @fetch-document-history="fetchDocumentHistory"
      />
    </div>

    <!-- 文件歷史對話框 -->
    <el-dialog v-model="showHistoryDialog" title="文件編輯歷史">
      <el-table :data="documentHistory" style="width: 100%">
        <el-table-column prop="edit_time" label="編輯時間" width="250" />
        <el-table-column label="詳細資料">
          <template #default="scope">
            <el-button
              type="primary"
              size="small"
              @click="showDetail(scope.row)"
            >
              Detail
            </el-button>
          </template>
        </el-table-column>
      </el-table>
      <template #footer>
        <el-button @click="showHistoryDialog = false">關閉</el-button>
      </template>
    </el-dialog>

    <DocumentContentComparisonDialog
      v-model:isVisible="showComparisonDialog"
      :currentContent="currentContent"
      :historyContent="historyContent"
    />

    <!-- 新增目錄對話框 -->
    <AddFolderDialog
      :directoryTree="directoryTree"
      v-model:isVisible="showAddFolderDialog"
      v-model:folderName="newFolderName"
      v-model:selectedParentFolderId="selectedParentFolderId"
      @save-folder="createFolder"
      @before-close="beforeClose"
    />

    <RenameFolderDialog
      v-model:showRenameFolderDialog="showRenameFolderDialog"
      v-model:renameFolderName="renameFolderName"
      @rename-folder="renameFolder"
      @before-close="beforeClose"
    />

    <DocumentDialog
      v-model:isVisible="showAddDocumentDialog"
      :document="newDocument"
      :isEditing="isEditing"
      :authors="authors"
      :directoryTree="directoryTree"
      @save-document="saveDocument"
      @upload-image="handleUploadImage"
      @before-close="beforeClose"
      @fetch-document-history="fetchDocumentHistory"
    />

    <DocumentPreviewDialog
      v-model:isVisible="showPreviewDialog"
      :previewDocumentData="previewDocumentData"
    />

    <!-- 文檔預覽對話框 -->
  </div>
</template>

<script>
import Sidebar from "@/components/document/Sidebar.vue";
import DocumentTable from "@/components/document/DocumentTable.vue";
import AddFolderDialog from "@/components/document/AddFolderDialog.vue";
import RenameFolderDialog from "@/components/document/RenameFolderDialog.vue";
import DocumentDialog from "@/components/document/DocumentDialog.vue";
import DocumentPreviewDialog from "@/components/document/DocumentPreviewDialog.vue";
import DocumentContentComparisonDialog from "@/components/document/DocumentContentComparisonDialog.vue";
import { ElMessageBox } from "element-plus";

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
  fetchDocumentHistory,
} from "@/api/document";

export default {
  components: {
    Sidebar,
    DocumentTable,
    AddFolderDialog,
    RenameFolderDialog,
    DocumentDialog,
    DocumentPreviewDialog,
    DocumentContentComparisonDialog,
  },
  data() {
    return {
      showAddDocumentDialog: false, // 用於綁定 v-model:isVisible
      newDocument: {
        title: "",
        author: "",
        date: "",
        folderId: null,
        content: "",
      }, // 確保初始化時不是 null
      directoryTree: [], // 目錄樹的結構數據
      currentFolder: null, // 當前選中的目錄
      currentFiles: [], // 當前目錄中的文件列表
      newFolderName: "",
      renameFolderName: "",
      folderToRename: null,
      selectedParentFolderId: null, // 選擇的父目錄 ID
      authors: ["Author1", "Author2", "Author3"],
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
      showPreviewDialog: false,
      previewDocumentData: {
        title: "",
        author: "",
        date: "",
        folderName: "",
        content: "",
      },
      showOperations: false,
      showHistoryDialog: false, // 控制歷史對話框的顯示
      documentHistory: [], // 儲存文件歷史數據
      showComparisonDialog: false,
      currentContent: {
        title: "",
        author: "",
        date: "",
        folderName: "",
        content: "",
      },
      historyContent: {
        editor: "",
        edit_time: "",
        content: "",
      },
    };
  },
  created() {
    this.fetchFolders();
  },
  methods: {
    // async fetchDocumentHistory(documentId) {
    //   try {
    //     const response = await fetchDocumentHistory(documentId);
    //     this.documentHistory = response.data;
    //     console.log("Fetched History Data:", this.documentHistory); // 檢查歷史數據是否正確
    //     this.showHistoryDialog = true; // 顯示歷史對話框
    //     console.log("Dialog Visibility:", this.showHistoryDialog); // 檢查對話框狀態
    //   } catch (error) {
    //     console.error("Error fetching document history:", error);
    //   }
    // },

    async fetchDocumentHistory(documentId) {
      try {
        const response = await fetchDocumentHistory(documentId);
        this.documentHistory = response.data;
        console.log("Fetched History Data:", this.documentHistory); // 檢查歷史數據是否正確
        this.showHistoryDialog = true; // 顯示歷史對話框
      } catch (error) {
        console.error("Error fetching document history:", error);
      }
    },
    async showDetail(record) {
      try {
        // 獲取當前文件的詳細資料
        const response = await fetchDocumentDetail(record.document_id);
        this.currentContent = {
          title: response.data.title,
          author: response.data.author,
          date: response.data.date,
          content: response.data.content,
          folderName: "未知目錄", // 可以根據需要查找具體文件夾名稱
        };

        // 設置歷史版本的內容
        this.historyContent = {
          editor: record.editor,
          edit_time: record.edit_time,
          content: record.content,
        };

        // 打開比較對話框
        this.showComparisonDialog = true;
      } catch (error) {
        console.error("Error fetching current document detail:", error);
      }
    },
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
      console.log("Edit mode toggled:", this.editMode);
    },
    openAddFolderDialog() {
      this.showAddFolderDialog = true;
      // 默認選擇當前目錄作為父目錄
      this.selectedParentFolderId = this.currentFolder
        ? this.currentFolder._id
        : null;
    },
    handleCreateFolder({ newFolderName, selectedParentFolderId }) {
      // 將創建文件夾的邏輯放在這裡
      this.newFolderName = newFolderName;
      this.selectedParentFolderId = selectedParentFolderId;
      this.createFolder(); // 可以將原來的方法搬過來使用
    },
    async createFolder() {
      try {
        // 顯示確認提示框
        await ElMessageBox.confirm("是否確定要新增這個目錄？", "確認", {
          confirmButtonText: "確定",
          cancelButtonText: "取消",
          type: "warning",
        });
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

        // 重置對話框數據
        this.showAddFolderDialog = false;
        this.newFolderName = "";
        this.selectedParentFolderId = null;
      } catch (error) {
        if (error === "cancel") {
          // 如果用戶取消操作，則不進行任何操作
          console.log("新增目錄操作已取消");
        } else {
          console.error("Error creating folder:", error);
        }
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
        await this.fetchFolders();
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
        // 根據 isEditing 狀態來設置提示訊息
        const actionMessage = this.isEditing
          ? "是否確定要儲存這份文件的變更？"
          : "是否確定要新增這份文件？";
        await ElMessageBox.confirm(actionMessage, "確認", {
          confirmButtonText: "確定",
          cancelButtonText: "取消",
          type: "warning",
        });

        console.log("Saving document:", this.newDocument);
        const documentData = { ...this.newDocument };
        documentData.date = documentData.date.split("T")[0]; // 只保留日期部分

        if (this.isEditing) {
          await updateDocument(this.newDocument._id, documentData);
        } else {
          await createDocument(documentData);
        }
        this.handleNodeClick(this.currentFolder);
        this.showAddDocumentDialog = false;
      } catch (error) {
        console.error("Error saving document:", error);
      }
    },

    async deleteDocument(documentId) {
      try {
        await deleteDocument(documentId);
        this.currentFiles = this.currentFiles.filter(
          (file) => file._id !== documentId
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
    async previewDocument(document) {
      try {
        const response = await fetchDocumentDetail(document._id);
        this.previewDocumentData.title = response.data.title;
        this.previewDocumentData.author = response.data.author;
        this.previewDocumentData.date = response.data.date;
        this.previewDocumentData.content = response.data.content;

        // 获取文件所在目录的名称
        const folder = this.findFolderById(response.data.folderId);
        this.previewDocumentData.folderName = folder
          ? folder.label
          : "未知目錄";

        this.showPreviewDialog = true;
      } catch (error) {
        console.error("Error fetching document details:", error);
      }
    },
    beforeClose(done) {
      ElMessageBox.confirm("您有未保存的更改。是否確定要退出？", "確認", {
        confirmButtonText: "確定",
        cancelButtonText: "取消",
        type: "warning",
      })
        .then(() => {
          done();
        })
        .catch(() => {
          // 如果用戶取消，則什麼都不做
        });
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
.button-row {
  display: flex;
  justify-content: space-between; /* 按鈕水平排列並均勻分布 */
}

.button-row .el-button {
  flex: 1;
}

.button-group {
  display: flex;
  flex-direction: column; /* 確保按鈕區域也是垂直排列 */
  gap: 10px;
  margin-bottom: 10px;
}

.content {
  flex: 1;
}

.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.action-button {
  margin-right: 1px;
}
</style>
