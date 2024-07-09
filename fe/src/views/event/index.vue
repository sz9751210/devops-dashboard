<template>
  <div>
    <!-- header -->
    <div class="header">
      <el-button type="primary" icon="plus" @click="openDialog"
        >新增事件</el-button
      >
    </div>

    <!-- table -->
    <el-table :data="Event" style="width: 100%">
      <el-table-column prop="title" label="Title" width="230" />
      <el-table-column prop="date" label="Date" width="230" />
      <el-table-column prop="description" label="Desc" width="300" />
      <el-table-column label="Operations" width="300">
        <template v-slot="scope">
          <el-button
            class="action-button"
            size="mini"
            type="primary"
            @click="editEvent(scope.row)"
            >Edit</el-button
          >
          <el-popconfirm
            title="delete this event?"
            @confirm="confirmDelete(scope.row._id)"
            @cancel="cancelDelete"
          >
            <template #reference>
              <el-button class="action-button" size="mini" type="danger"
                >Delete</el-button
              >
            </template>
          </el-popconfirm>
          <el-button
            class="action-button"
            size="mini"
            @click="viewDetail(scope.row)"
            >Detail</el-button
          >
        </template>
      </el-table-column>
    </el-table>

    <!-- dialog for adding/editing event -->
    <!-- close-on-click-modal：關閉對話框時不關閉父層，false表示防止點擊對話框時對話框消失 -->
    <el-dialog
      :title="editingEventId ? 'Edit' : 'Add'"
      v-model="showDialog"
      close-on-click-modal="false"
      @close="handleDialogClose"
      :before-close="beforeClose"
    >
      <el-form ref="eventForm" :model="newEvent" label-width="80px">
        <el-form-item label="Title">
          <el-input v-model="newEvent.title" />
        </el-form-item>
        <el-form-item label="Date">
          <el-date-picker
            v-model="newEvent.date"
            type="date"
            placeholder="Pick a date"
            value-format="YYYY-MM-DD"
          />
        </el-form-item>
        <el-form-item label="Desc">
          <el-input v-model="newEvent.description" />
        </el-form-item>
        <el-form-item label="Question">
          <el-input
            type="textarea"
            rows="10"
            v-model="newEvent.question"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="Answer">
          <el-input
            type="textarea"
            rows="10"
            v-model="newEvent.answer"
            style="width: 100%"
          />
        </el-form-item>
        <el-form-item label="Image">
          <el-upload
            action="#"
            list-type="picture-card"
            :on-preview="handlePictureCardPreview"
            :on-remove="handleRemove"
            :on-change="handleImageChange"
            :file-list="fileList"
            :auto-upload="false"
            multiple
          >
            <el-icon class="avatar-uploader-icon"><Plus /></el-icon>
          </el-upload>

          <el-dialog v-model="dialogVisible">
            <img width="100%" :src="dialogImageUrl" alt="preview image" />
          </el-dialog>
        </el-form-item>
        <el-form-item>
          <el-button type="primary" @click="submitEvent">提交</el-button>
          <el-popconfirm
            title="確定取消？"
            @confirm="cancelDialog"
            @cancel="popoverCancelVisible = false"
          >
            <template #reference>
              <el-button>取消</el-button>
            </template>
          </el-popconfirm>
        </el-form-item>
      </el-form>
    </el-dialog>

    <!-- dialog for viewing detail -->
    <el-dialog
      title="Event Details"
      v-model="showDetailDialog"
    >
      <el-form label-width="80px">
        <el-form-item label="Title">
          <span>{{ detailEvent.title }}</span>
        </el-form-item>
        <el-form-item label="Date">
          <span>{{ detailEvent.date }}</span>
        </el-form-item>
        <el-form-item label="Desc">
          <span>{{ detailEvent.description }}</span>
        </el-form-item>
        <el-form-item label="Question">
          <span class="pre-wrap">{{ detailEvent.question }}</span>
        </el-form-item>
        <el-form-item label="Answer">
          <span class="pre-wrap">{{ detailEvent.answer }}</span>
        </el-form-item>

        <!-- preview-src-list：支持點擊預覽 -->
        <el-form-item label="Images">
          <el-row :gutter="20">
            <!-- <div v-if="detailEvent.imageUrls && detailEvent.imageUrls.length"> -->
            <el-col
              v-for="(url, index) in detailEvent.imageUrls"
              :key="index"
              :span="6"
            >
              <el-image
                :src="url"
                :preview-src-list="detailEvent.imageUrls"
                class="avatar"
                fit="cover"
              />
            </el-col>
            <!-- </div> -->
          </el-row>
        </el-form-item>

        <el-form-item>
          <el-button @click="showDetailDialog = false">Close</el-button>
        </el-form-item>
      </el-form>
    </el-dialog>

    <el-dialog v-model="dialogVisible">
      <img width="100%" :src="dialogImageUrl" alt="preview image" />
    </el-dialog>
  </div>
</template>

<script>
import { fetchEvent, createEvent, updateEvent, deleteEvent } from "@/api/event"; // 調整路徑以符合你的專案結構
import { ElMessage, ElMessageBox } from "element-plus";

export default {
  data() {
    return {
      Event: [],
      showDialog: false,
      showDetailDialog: false,
      dialogImageUrl: "",
      dialogVisible: false,
      fileList: [],
      newEvent: {
        title: "",
        date: "",
        description: "",
        question: "",
        answer: "",
        imageUrls: [],
      },
      detailEvent: {
        title: "",
        date: "",
        description: "",
        question: "",
        answer: "",
        imageUrls: [],
      },
      editingEventId: null,
      deleteEventId: null,
    };
  },
  created() {
    this.fetchEvent();
  },
  methods: {
    async fetchEvent() {
      try {
        const response = await fetchEvent();
        this.Event = response.data;
      } catch (error) {
        console.error("Error fetching Event:", error);
      }
    },
    openDialog() {
      this.editingEventId = null;
      this.newEvent = {
        title: "",
        date: "",
        question: "",
        answer: "",
        description: "",
        imageUrls: [],
      };
      this.fileList = [];
      this.showDialog = true;
    },
    async submitEvent() {
      try {
        let response;
        const eventData = { ...this.newEvent };
        eventData.date = eventData.date.split("T")[0]; // 只保留日期部分
        console.log("Event data:", eventData);
        if (this.editingEventId) {
          delete eventData._id;
          console.log("Event data:", eventData);
          await updateEvent(this.editingEventId, eventData);
        } else {
          await createEvent(eventData);
        }
        console.log("Submit response:", response);
        this.fetchEvent();
        this.showDialog = false;
        this.$refs.eventForm.resetFields();
        ElMessage({
          message: this.editingEventId ? "更新成功" : "提交成功",
          type: "success",
          duration: 5 * 1000,
        });
      } catch (error) {
        console.error("Error submitting event:", error);
        ElMessage({
          message: "提交失败",
          type: "error",
          duration: 5 * 1000,
        });
      }
    },
    editEvent(event) {
      this.newEvent = { ...event };
      this.editingEventId = event._id;
      this.showDialog = true;
    },
    async deleteEvent(eventId) {
      try {
        const response = await deleteEvent(eventId);
        console.log("Delete response:", response);
        this.fetchEvent();
        ElMessage({
          message: "删除成功",
          type: "success",
          duration: 5 * 1000,
        });
      } catch (error) {
        console.error("Error deleting event:", error);
        ElMessage({
          message: "删除失败",
          type: "error",
          duration: 5 * 1000,
        });
      }
    },
    confirmDelete(eventId) {
      console.log("confirmDelete called with eventId:", eventId); // 日誌
      this.deleteEvent(eventId);
    },
    cancelDelete() {
      console.log("cancelDelete called"); // 日誌
      ElMessage({
        message: "取消操作",
        type: "info",
        duration: 3 * 1000,
      });
    },
    viewDetail(event) {
      this.detailEvent = { ...event };
      this.showDetailDialog = true;
    },
    handleDialogClose() {
      if (this.$refs.eventForm.$el.contains(document.activeElement)) {
        return;
      }
    },
    cancelDialog() {
      this.showDialog = false;
      this.$refs.eventForm.resetFields();
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
    // 上傳圖片
    handleUploadSuccess(response, file, fileList) {
      const url = URL.createObjectURL(file.raw);
      file.url = url; // 添加这行
      this.newEvent.imageUrls.push(url);
      this.fileList = fileList;
    },
    handlePictureCardPreview(file) {
      this.dialogImageUrl = file.url;
      this.dialogVisible = true;
    },
    handleRemove(file, fileList) {
      const url = file.url;
      const index = this.newEvent.imageUrls.indexOf(url);
      if (index !== -1) {
        this.newEvent.imageUrls.splice(index, 1);
      }
      this.fileList = fileList;
    },
    handleImageChange(file, fileList) {
      const reader = new FileReader();
      reader.readAsDataURL(file.raw);
      reader.onload = () => {
        file.url = reader.result;
        if (!this.newEvent.imageUrls) {
          this.newEvent.imageUrls = [];
        }
        this.newEvent.imageUrls.push(file.url);
        this.fileList = fileList;
      };
    },
  },
};
</script>

<style scoped>
.header {
  display: flex;
  justify-content: flex-end;
  margin-bottom: 20px;
}
.pre-wrap {
  white-space: pre-wrap;
}
.action-button {
  margin-right: 5px;
}
.avatar {
  width: 100%;
  height: 100%;
  /* display: block; */
  cursor: pointer;
}
.avatar-uploader .el-upload {
  border: 1px dashed var(--el-border-color);
  border-radius: 6px;
  cursor: pointer;
  position: relative;
  overflow: hidden;
  transition: var(--el-transition-duration-fast);
}

.avatar-uploader .el-upload:hover {
  border-color: var(--el-color-primary);
}

.el-icon.avatar-uploader-icon {
  font-size: 28px;
  color: #8c939d;
  width: 178px;
  height: 178px;
  text-align: center;
}
</style>
