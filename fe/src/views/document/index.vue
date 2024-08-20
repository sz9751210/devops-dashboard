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
              :key="folder.id"
              :label="folder.label"
              :value="folder.id"
            ></el-option>
          </el-select>
        </el-form-item>
      </el-form>
      <el-button type="primary" @click="saveDocument">確定</el-button>
    </el-dialog>
  </div>
</template>

<script>
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
  methods: {
    handleNodeClick(node) {
      this.currentFolder = node;
      this.currentFiles = node.files || [];
    },
    toggleEditMode() {
      this.editMode = !this.editMode;
    },
    openAddFolderDialog() {
      this.showAddFolderDialog = true;
    },
    createFolder() {
      if (this.addFolderLevel === "current" && this.currentFolder) {
        this.currentFolder.children = this.currentFolder.children || [];
        this.currentFolder.children.push({
          id: Date.now(),
          label: this.newFolderName,
          children: [],
          files: [],
        });
      } else {
        this.directoryTree.push({
          id: Date.now(),
          label: this.newFolderName,
          children: [],
          files: [],
        });
      }
      this.showAddFolderDialog = false;
      this.newFolderName = "";
      this.addFolderLevel = "root";
    },
    openRenameFolderDialog() {
      this.renameFolderName = this.currentFolder.label;
      this.showRenameFolderDialog = true;
    },
    renameFolder() {
      if (this.currentFolder) {
        this.currentFolder.label = this.renameFolderName;
      }
      this.showRenameFolderDialog = false;
      this.renameFolderName = "";
    },
    deleteCurrentFolder() {
      const removeNode = (nodes, folder) => {
        const index = nodes.findIndex((node) => node.id === folder.id);
        if (index !== -1) {
          nodes.splice(index, 1);
          return true;
        }
        for (let node of nodes) {
          if (node.children && node.children.length > 0) {
            const removed = removeNode(node.children, folder);
            if (removed) return true;
          }
        }
        return false;
      };
      removeNode(this.directoryTree, this.currentFolder);
      this.currentFolder = null;
    },
    openAddDocumentDialog() {
      this.isEditing = false;
      this.newDocument = {
        title: "",
        author: "",
        date: "",
        folderId: null, // 預設為 null，讓用戶選擇目錄
        originalFolderId: null, // 預設為 null
      };
      this.showAddDocumentDialog = true;
    },
    editDocument(document) {
      this.isEditing = true;
      this.newDocument = {
        ...document,
        originalFolderId: this.currentFolder.id,
      };
      this.showAddDocumentDialog = true;
    },
    saveDocument() {
      if (this.isEditing) {
        // 編輯模式下，更新文件位置和其他屬性
        const originalFolder = this.findFolderById(
          this.newDocument.originalFolderId
        );
        const targetFolder = this.findFolderById(this.newDocument.folderId);

        if (originalFolder && targetFolder) {
          const fileIndex = originalFolder.files?.findIndex(
            (file) => file.id === this.newDocument.id
          );

          if (fileIndex !== -1 && fileIndex !== undefined) {
            // 更新文件內容
            const updatedFile = {
              ...originalFolder.files[fileIndex],
              title: this.newDocument.title,
              author: this.newDocument.author,
              date: this.newDocument.date,
            };

            // 如果目錄改變，移動文件
            if (originalFolder !== targetFolder) {
              // 將文件從原來的目錄中移除
              originalFolder.files.splice(fileIndex, 1);
              // 添加到新目錄
              targetFolder.files = targetFolder.files || [];
              targetFolder.files.push(updatedFile);
            } else {
              // 只更新文件屬性，不移動
              originalFolder.files.splice(fileIndex, 1, updatedFile);
            }
          } else {
            console.error("文件未找到，無法更新");
          }
        } else {
          console.error("目錄未找到，無法更新文件");
        }
      } else {
        // 新增模式下，直接保存文件
        const targetFolder = this.findFolderById(this.newDocument.folderId);
        if (targetFolder) {
          targetFolder.files = targetFolder.files || [];
          targetFolder.files.push({ ...this.newDocument, id: Date.now() });
        } else {
          console.error("目錄未找到，無法保存文件");
        }
      }

      // 重置狀態並關閉對話框
      this.showAddDocumentDialog = false;
      this.newDocument = {
        title: "",
        author: "",
        date: "",
        folderId: null,
        originalFolderId: null,
      };
      this.handleNodeClick(this.currentFolder);
    },

    deleteDocument(document) {
      const index = this.currentFiles.indexOf(document);
      if (index !== -1) {
        this.currentFiles.splice(index, 1);
      }
    },
    findFolderById(id) {
      const findInTree = (nodes) => {
        for (let node of nodes) {
          if (node.id === id) return node;
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
          result.push({ id: node.id, label: node.label });
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
