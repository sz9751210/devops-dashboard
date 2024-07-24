<template>
  <div>
    <el-table :data="operationLogs" style="width: 100%">
      <el-table-column prop="username" label="Username" width="150" />
      <el-table-column prop="method" label="Method" width="100" />
      <el-table-column prop="path" label="Path" width="250" />
      <el-table-column prop="ip" label="IP Address" width="150" />
      <el-table-column prop="location" label="Location" width="250" />
      <el-table-column prop="timestamp" label="Timestamp" width="200" />
    </el-table>

    <el-pagination
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pageSize"
      layout="total, prev, pager, next"
      :total="totalLogs"
    />
  </div>
</template>

<script>
import { fetchOperationLogs } from "@/api/operation-logs";

export default {
  data() {
    return {
      operationLogs: [],
      currentPage: 1,
      pageSize: 20,
      totalLogs: 0,
    };
  },
  created() {
    this.fetchLogs();
  },
  methods: {
    async fetchLogs() {
      try {
        const response = await fetchOperationLogs(this.currentPage, this.pageSize);
        console.log("operation logs", response);
        console.log("response code", response.code);
        console.log("response data", response.data);
        // 正確解析後端返回的數據結構
        if (response && response.data && response.code === 200 && Array.isArray(response.data)) {
          this.operationLogs = response.data;
          this.totalLogs = response.total || response.data.length;
        } else {
          console.error("Unexpected response format:", response);
        }
      } catch (error) {
        console.error("Error fetching operation logs:", error);
      }
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.fetchLogs();
    },
  },
};
</script>
