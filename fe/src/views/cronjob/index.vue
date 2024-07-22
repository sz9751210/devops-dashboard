<template>
  <div>
    <div class="header">
      <el-button type="primary" icon="el-icon-plus" @click="openDialog">新增 Cronjob</el-button>
    </div>

    <!-- table -->
    <el-table :data="cronjobs" style="width: 100%">
      <el-table-column prop="expression" label="Cron 表達式" width="180" />
      <el-table-column prop="description" label="描述" width="230" />
      <el-table-column prop="task" label="任務" width="180" />
      <el-table-column label="操作" width="150">
        <template v-slot="scope">
          <el-button
            class="action-button"
            size="small"
            type="primary"
            @click="editCronjob(scope.row)"
          >編輯</el-button>
          <el-popconfirm
            title="確定刪除此 Cronjob？"
            @confirm="confirmDelete(scope.row._id)"
            @cancel="cancelDelete"
          >
            <template #reference>
              <el-button class="action-button" size="small" type="danger">刪除</el-button>
            </template>
          </el-popconfirm>
        </template>
      </el-table-column>
    </el-table>

    <!-- dialog for adding/editing cronjob -->
    <el-dialog
      :title="editingCronjobId ? '編輯 Cronjob' : '新增 Cronjob'"
      v-model="showDialog"
      close-on-click-modal="false"
      @close="handleDialogClose"
      :before-close="beforeClose"
    >
      <el-form ref="cronjobForm" :model="newCronjob" label-width="150px">
        <el-form-item label="Cron 表達式">
          <el-input v-model="newCronjob.expression" class="input-field" placeholder="例如：0 0 * * *"></el-input>
        </el-form-item>
        <el-form-item label="描述">
          <el-input v-model="newCronjob.description" class="input-field"></el-input>
        </el-form-item>
        <el-form-item label="任務">
          <el-select v-model="newCronjob.task" placeholder="選擇任務" class="input-field">
            <el-option
              v-for="item in tasks"
              :key="item.value"
              :label="item.label"
              :value="item.value"
            />
          </el-select>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitCronjob">提交</el-button>
          <el-button @click="cancelDialog">取消</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>
  </div>
</template>

<script>
import { ElMessage, ElMessageBox } from "element-plus";
import { addCronjob, editCronjob, fetchCronjobs, deleteCronjob } from "@/api/cronjob";

export default {
  data() {
    return {
      cronjobs: [],
      showDialog: false,
      newCronjob: {
        expression: "",
        description: "",
        task: "",
      },
      tasks: [
        { value: "sync_cloudflare", label: "同步 Cloudflare" },
        { value: "check_subdomains", label: "檢查子域名" },
      ],
      editingCronjobId: null,
      loading: false,
    };
  },
  created() {
    this.fetchCronjobs();
  },
  methods: {
    async fetchCronjobs() {
      this.loading = true;
      try {
        const response = await fetchCronjobs();
        this.cronjobs = response.data;
      } catch (error) {
        console.error("Error fetching cronjobs:", error);
        ElMessage({
          message: "Cronjobs 加載失敗",
          type: "error",
          duration: 5 * 1000,
        });
      } finally {
        this.loading = false;
      }
    },
    openDialog() {
      this.editingCronjobId = null;
      this.newCronjob = {
        expression: "",
        description: "",
        task: "",
      };
      this.showDialog = true;
    },
    async submitCronjob() {
      this.loading = true;
      try {
        if (this.editingCronjobId) {
          await editCronjob(this.editingCronjobId, this.newCronjob);
        } else {
          await addCronjob(this.newCronjob);
        }
        this.fetchCronjobs();
        this.showDialog = false;
        ElMessage({
          message: this.editingCronjobId ? "Cronjob 更新成功" : "Cronjob 已保存",
          type: "success",
          duration: 5 * 1000,
        });
      } catch (error) {
        console.error("Error saving cronjob:", error);
        ElMessage({
          message: "Cronjob 保存失敗",
          type: "error",
          duration: 5 * 1000,
        });
      } finally {
        this.loading = false;
      }
    },
    editCronjob(cronjob) {
      this.newCronjob = { ...cronjob };
      this.editingCronjobId = cronjob._id;
      this.showDialog = true;
    },
    async deleteCronjob(cronjobId) {
      this.loading = true;
      try {
        await deleteCronjob(cronjobId);
        this.fetchCronjobs();
        ElMessage({
          message: "Cronjob 已刪除",
          type: "success",
          duration: 5 * 1000,
        });
      } catch (error) {
        console.error("Error deleting cronjob:", error);
        ElMessage({
          message: "Cronjob 刪除失敗",
          type: "error",
          duration: 5 * 1000,
        });
      } finally {
        this.loading = false;
      }
    },
    confirmDelete(cronjobId) {
      this.deleteCronjob(cronjobId);
    },
    cancelDelete() {
      ElMessage({
        message: "取消操作",
        type: "info",
        duration: 3 * 1000,
      });
    },
    handleDialogClose() {
      if (this.$refs.cronjobForm.$el.contains(document.activeElement)) {
        return;
      }
    },
    cancelDialog() {
      this.showDialog = false;
      this.$refs.cronjobForm.resetFields();
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
.header {
  display: flex;
  justify-content: space-between;
  margin-bottom: 20px;
}
.action-button {
  margin-right: 1px;
}
</style>
