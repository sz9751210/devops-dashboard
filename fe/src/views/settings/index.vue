<template>
  <div>
    <el-card class="box-card">
      <div slot="header" class="clearfix">
        <span>設定</span>
        <el-button
          class="action-button"
          type="primary"
          @click="toggleEdit"
          style="float: right"
        >
          {{ isEditing ? "取消" : "編輯" }}
        </el-button>
      </div>
      <el-form
        ref="settingsForm"
        :model="settings"
        label-width="150px"
        class="settings-form"
      >
        <div class="section-header">Cloudflare</div>
        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item label="API Key">
              <template v-if="isEditing">
                <el-input
                  v-model="settings.cloudflareApiKey"
                  class="input-field"
                />
              </template>
              <template v-else>
                <span v-if="settings.cloudflareApiKey">
                  <span v-if="isCloudflareApiKeyVisible">
                    {{ settings.cloudflareApiKey }}
                  </span>
                  <span v-else>••••••••</span>
                </span>
              </template>
            </el-form-item>
          </el-col>
          <el-col :span="6" class="button-group">
            <el-button @click="toggleVisibility('isCloudflareApiKeyVisible')">
              <el-icon><component :is="isCloudflareApiKeyVisible ? 'Hide' : 'View'" /></el-icon>
            </el-button>
            <el-button @click="copyToClipboard(settings.cloudflareApiKey)">
              <el-icon><DocumentCopy /></el-icon>
            </el-button>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item label="Email">
              <template v-if="isEditing">
                <el-input
                  v-model="settings.cloudflareEmail"
                  class="input-field"
                />
              </template>
              <template v-else>
                <span v-if="settings.cloudflareEmail">
                  <span v-if="isCloudflareEmailVisible">{{
                    settings.cloudflareEmail
                  }}</span>
                  <span v-else>••••••••</span>
                </span>
              </template>
            </el-form-item>
          </el-col>
          <el-col :span="6" class="button-group">
            <el-button @click="toggleVisibility('isCloudflareEmailVisible')">
              <el-icon><component :is="isCloudflareEmailVisible ? 'Hide' : 'View'" /></el-icon>
            </el-button>
            <el-button @click="copyToClipboard(settings.cloudflareEmail)">
              <el-icon><DocumentCopy /></el-icon>
            </el-button>
          </el-col>
        </el-row>

        <div class="section-header">Telegram Notify</div>

        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item label="Bot Token">
              <template v-if="isEditing">
                <el-input
                  v-model="settings.telegramBotToken"
                  class="input-field"
                />
              </template>
              <template v-else>
                <span v-if="settings.telegramBotToken">
                  <span v-if="isTelegramBotTokenVisible">{{
                    settings.telegramBotToken
                  }}</span>
                  <span v-else>•••••••• </span>
                </span>
              </template>
            </el-form-item>
          </el-col>
          <el-col :span="6" class="button-group">
            <el-button @click="toggleVisibility('isTelegramBotTokenVisible')">
              <el-icon><component :is="isTelegramBotTokenVisible ? 'Hide' : 'View'" /></el-icon>
            </el-button>
            <el-button @click="copyToClipboard(settings.telegramBotToken)">
              <el-icon><DocumentCopy /></el-icon>
            </el-button>
          </el-col>
        </el-row>

        <el-row :gutter="20">
          <el-col :span="18">
            <el-form-item label="Chat ID">
              <template v-if="isEditing">
                <el-input
                  v-model="settings.telegramChatId"
                  class="input-field"
                />
              </template>
              <template v-else>
                <span v-if="settings.telegramChatId">

                <span v-if="isTelegramChatIdVisible">{{
                  settings.telegramChatId
                }}</span>
                <span v-else>••••••••
                </span>
                </span>
              </template>
            </el-form-item>
          </el-col>
          <el-col :span="6" class="button-group">
            <el-button @click="toggleVisibility('isTelegramChatIdVisible')">
              <el-icon><component :is="isTelegramChatIdVisible ? 'Hide' : 'View'" /></el-icon>
            </el-button>
            <el-button @click="copyToClipboard(settings.telegramChatId)">
              <el-icon><DocumentCopy /></el-icon>
            </el-button>
          </el-col>
        </el-row>

        <el-form-item v-if="isEditing">
          <div class="button-group"></div>
          <el-button
            class="action-button"
            type="primary"
            @click="confirmSubmitSettings"
            >保存</el-button
          >
          <el-button
            class="action-button"
            type="danger"
            @click="confirmDeleteSettings"
            v-if="settings._id"
            >刪除</el-button
          >
        </el-form-item>
      </el-form>
    </el-card>
    <el-loading :loading="loading">
      <span v-if="loading">加載中...</span>
    </el-loading>
  </div>
</template>

<script>
import {
  fetchSettings,
  addSetting,
  updateSetting,
  deleteSetting,
} from "@/api/settings";
import { ElMessage, ElMessageBox } from "element-plus";
import { View, CopyDocument, DocumentCopy } from "@element-plus/icons-vue";
export default {
  data() {
    return {
      settings: {
        cloudflareApiKey: "",
        cloudflareEmail: "",
        telegramBotToken: "",
        telegramChatId: "",
      },
      isEditing: false,
      loading: false,
      isCloudflareApiKeyVisible: false,
      isCloudflareEmailVisible: false,
      isTelegramBotTokenVisible: false,
      isTelegramChatIdVisible: false,
    };
  },
  created() {
    this.fetchSettings();
  },
  methods: {
    async fetchSettings() {
      this.loading = true;
      try {
        const response = await fetchSettings();
        console.log(response);
        if (response.data && response.data.length > 0) {
          this.settings = response.data[0];
        } else {
          this.settings = {
            cloudflareApiKey: "",
            cloudflareEmail: "",
            telegramBotToken: "",
            telegramChatId: "",
          };
        }
      } catch (error) {
        console.error("Error fetching settings:", error);
        ElMessage({
          message: "設定加載失敗",
          type: "error",
          duration: 5 * 1000,
        });
      } finally {
        this.loading = false;
      }
    },
    toggleEdit() {
      this.isEditing = !this.isEditing;
    },
    async confirmSubmitSettings() {
      try {
        await ElMessageBox.confirm("你確定要保存這些變更嗎？", "確認", {
          confirmButtonText: "確定",
          cancelButtonText: "取消",
          type: "warning",
        });
        this.submitSettings();
      } catch (error) {
        console.log("保存取消");
      }
    },
    async submitSettings() {
      this.$refs.settingsForm.validate(async (valid) => {
        if (valid) {
          try {
            let response;
            if (this.settings._id) {
              response = await updateSetting(this.settings._id, this.settings);
            } else {
              response = await addSetting(this.settings);
              if (response.data && response.data.setting_id) {
                this.settings._id = response.data.setting_id;
              }
            }
            ElMessage({
              message: "設定保存成功",
              type: "success",
              duration: 5 * 1000,
            });
            this.isEditing = false;
          } catch (error) {
            console.error("Error saving settings:", error);
            ElMessage({
              message: "設定保存失敗",
              type: "error",
              duration: 5 * 1000,
            });
          }
        }
      });
    },
    async confirmDeleteSettings() {
      try {
        await ElMessageBox.confirm("你確定要刪除此設定嗎？", "警告", {
          confirmButtonText: "確定",
          cancelButtonText: "取消",
          type: "warning",
        });
        this.deleteSettings();
      } catch (error) {
        console.log("刪除取消");
      }
    },
    async deleteSettings() {
      if (!this.settings._id) {
        ElMessage({
          message: "無法刪除，設置尚未保存",
          type: "error",
          duration: 5 * 1000,
        });
        return;
      }
      this.loading = true;
      try {
        await deleteSetting(this.settings._id);
        this.settings = {
          cloudflareApiKey: "",
          cloudflareEmail: "",
          telegramBotToken: "",
          telegramChatId: "",
        };
        ElMessage({
          message: "設定刪除成功",
          type: "success",
          duration: 5 * 1000,
        });
        this.isEditing = false;
      } catch (error) {
        console.error("Error deleting settings:", error);
        ElMessage({
          message: "設定刪除失敗",
          type: "error",
          duration: 5 * 1000,
        });
      } finally {
        this.loading = false;
      }
    },
    toggleVisibility(field) {
      this[field] = !this[field];
    },
    copyToClipboard(value) {
      navigator.clipboard.writeText(value).then(
        () => {
          ElMessage({
            message: "已複製到剪貼簿",
            type: "success",
            duration: 2 * 1000,
          });
        },
        (err) => {
          ElMessage({
            message: "複製失敗",
            type: "error",
            duration: 2 * 1000,
          });
        }
      );
    },
  },
};
</script>

<style scoped>
.box-card {
  margin: 20px;
}
.settings-form .el-form-item {
  display: flex;
  align-items: center;
}
.settings-form .el-form-item__label {
  flex: 0 0 150px;
  text-align: left;
}
.settings-form .el-form-item__content {
  flex: 1;
}
.action-button {
  width: 100px;
}
.input-field {
  width: 400px;
}
.section-header {
  font-size: 20px;
  font-weight: bold;
  margin-top: 20px;
  margin-bottom: 10px;
}
.button-group {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}
</style>
