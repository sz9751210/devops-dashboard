<template>
  <div>
    <!-- header -->
    <div class="header">
      <div class="inputs">
        <el-input
          v-model="searchDomain"
          placeholder="輸入域名"
          clearable
          class="search-input"
          @keyup.enter="handleSearch"
        ></el-input>
        <el-input
          v-model.number="maxDaysLeft"
          placeholder="最多剩餘天數"
          type="number"
          clearable
          class="days-input"
          @keyup.enter="handleSearch"
        ></el-input>
        <el-select
          v-model="searchStatus"
          placeholder="選擇狀態"
          clearable
          class="status-select"
          @keyup.enter="handleSearch"
        >
          <el-option label="開啟" :value="true"></el-option>
          <el-option label="關閉" :value="false"></el-option>
        </el-select>
      </div>
      <div class="buttons">
        <el-button type="primary" @click="handleSearch">搜尋</el-button>
        <el-button type="success" @click="syncCloudflare"
          >同步 Cloudflare</el-button
        >
        <el-button type="warning" @click="checkAllSubdomains"
          >檢查所有子域名</el-button
        >
      </div>
    </div>

    <!-- table -->
    <el-table
      :data="pagedData"
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      <el-table-column prop="domain" label="域名" width="180" />
      <el-table-column prop="subdomain" label="子域名" width="180" />
      <el-table-column
        prop="expiry_date"
        label="到期時間"
        width="150"
        sortable
      />
      <el-table-column
        prop="update_date"
        label="更新時間"
        width="150"
        sortable
      />
      <el-table-column prop="status" label="狀態" width="100">
        <template v-slot="scope">
          <el-switch
            v-model="scope.row.status"
            :active-value="true"
            :inactive-value="false"
            active-color="#13ce66"
            inactive-color="#dcdfe6"
            @change="handleStatusChange(scope.row)"
          ></el-switch>
        </template>
      </el-table-column>
      <el-table-column prop="days_left" label="剩餘天數" width="150" sortable>
        <template v-slot="scope">
          <span :class="getDaysLeftClass(scope.row.days_left)">
            {{ scope.row.days_left }}
          </span>
        </template>
      </el-table-column>
    </el-table>

    <!-- pagination -->
    <el-pagination
      @current-change="handleCurrentChange"
      :current-page="currentPage"
      :page-size="pageSize"
      layout="total, prev, pager, next"
      :total="totalSubdomains"
    >
    </el-pagination>
  </div>
</template>

<script>
import {
  fetchDomain,
  updateDomainStatus,
  syncCloudflareRecords,
  checkSubdomains,
} from "@/api/certificate";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      domainData: [],
      pagedData: [],
      currentPage: 1,
      pageSize: 20,
      totalSubdomains: 0,
      sortColumn: "",
      sortOrder: "",
      searchDomain: "",
      maxDaysLeft: null,
      searchStatus: null,
    };
  },
  created() {
    this.fetchDomain();
  },
  methods: {
    async fetchDomain() {
      try {
        const response = await fetchDomain();
        if (response.data) {
          console.log("Fetched domain data:", response.data);
          const formattedData = this.formatDomainData(response.data);
          this.totalSubdomains = formattedData.length;
          this.domainData = formattedData;
          this.calculateDaysLeft();
          this.sortAndPageData();
        } else {
          console.error("Unexpected response format:", response.data);
        }
      } catch (error) {
        console.error("Error fetching domain data:", error);
      }
    },
    formatDomainData(data) {
      if (!Array.isArray(data)) {
        console.error("Expected data to be an array, but got:", data);
        return [];
      }
      const formattedData = [];
      data.forEach((domain) => {
        if (Array.isArray(domain.subdomains)) {
          domain.subdomains.forEach((subdomain) => {
            formattedData.push({
              domain: domain.domain,
              subdomain: subdomain.name,
              expiry_date: subdomain.expiry_date || "N/A",
              update_date: subdomain.update_date || "N/A",
              status: subdomain.status,
              days_left: 0,
            });
          });
        }
      });
      return formattedData;
    },
    calculateDaysLeft() {
      const today = new Date();
      this.domainData.forEach((item) => {
        if (item.expiry_date !== "N/A") {
          const expiryDate = new Date(item.expiry_date);
          const timeDiff = expiryDate - today;
          const daysDiff = Math.ceil(timeDiff / (1000 * 60 * 60 * 24));
          item.days_left = daysDiff;
        } else {
          item.days_left = "N/A";
        }
      });
    },
    getDaysLeftClass(daysLeft) {
      if (daysLeft === "N/A") {
        return "";
      } else if (daysLeft < 15) {
        return "red-text";
      } else if (daysLeft >= 15 && daysLeft <= 30) {
        return "yellow-text";
      } else {
        return "green-text";
      }
    },
    handleCurrentChange(newPage) {
      this.currentPage = newPage;
      this.sortAndPageData();
    },
    handleSortChange({ column, prop, order }) {
      this.sortColumn = prop;
      this.sortOrder = order;
      this.sortAndPageData();
    },
    sortAndPageData() {
      // let sortedData = [...this.domainData];

      let filteredData = this.domainData;

      if (this.searchDomain) {
        filteredData = filteredData.filter((item) =>
          item.domain.includes(this.searchDomain)
        );
      }

      if (this.maxDaysLeft !== null) {
        filteredData = filteredData.filter(
          (item) =>
            item.days_left !== "N/A" && item.days_left <= this.maxDaysLeft
        );
      }

      if (this.searchStatus !== null) {
        filteredData = filteredData.filter(
          (item) => item.status === this.searchStatus
        );
      }

      // 確保過濾掉 days_left 是 "N/A" 的域名
      filteredData = filteredData.filter((item) => item.days_left !== "N/A");

      if (this.sortColumn) {
        filteredData.sort((a, b) => {
          let result = 0;
          if (a[this.sortColumn] < b[this.sortColumn]) {
            result = -1;
          } else if (a[this.sortColumn] > b[this.sortColumn]) {
            result = 1;
          }
          return this.sortOrder === "ascending" ? result : -result;
        });
      }

      // 更新 totalSubdomains
      this.totalSubdomains = filteredData.length;

      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.pagedData = filteredData.slice(start, end);
    },
    async handleStatusChange(row) {
      try {
        const data = {
          domain: row.domain,
          subdomain: row.subdomain,
          status: row.status,
        };
        await updateDomainStatus(data);
        ElMessage({
          message: row.status ? "域名狀態啟用成功" : "域名狀態關閉成功",
          type: "success",
        });
      } catch (error) {
        console.log("Error updating domain status:", error);
        ElMessage({
          message: "域名狀態更新失敗",
          type: "error",
        });
      }
    },
    handleSearch() {
      if (
        !this.searchDomain &&
        this.maxDaysLeft === null &&
        this.searchStatus === null
      ) {
        this.currentPage = 1;
        this.totalSubdomains = this.domainData.filter(
          (item) => item.days_left !== "N/A"
        ).length;
        this.pagedData = this.domainData
          .filter((item) => item.days_left !== "N/A")
          .slice(0, this.pageSize);
      } else {
        this.sortAndPageData();
      }
    },

    async syncCloudflare() {
      try {
        ElMessage({
          message: "開始同步 Cloudflare",
          type: "info",
          duration: 0, // 持续时间为0，表示消息不会自动消失，需要手动关闭
        });
        const response = await syncCloudflareRecords();
        ElMessage.closeAll();
        if (response.code === 200) {
          ElMessage({
            message: "同步 Cloudflare 成功",
            type: "success",
            duration: 3000,
          });
          console.log("同步成功，開始抓取域名數據");
          await this.fetchDomain();
        } else {
          ElMessage({
            message: "同步 Cloudflare 失敗",
            type: "error",
            duration: 3000,
          });
        }
      } catch (error) {
        console.error("Error syncing Cloudflare:", error);
        ElMessage({
          message: "同步 Cloudflare 失敗",
          type: "error",
          duration: 3000,
        });
      }
    },
    async checkAllSubdomains() {
      try {
        const response = await checkSubdomains();
        console.log("response: ", response);
        if (response.code === 200) {
          ElMessage({
            message: "子域名檢查成功",
            type: "success",
            duration: 3000,
          });
        } else {
          ElMessage({
            message: "子域名檢查失敗",
            type: "error",
            duration: 3000,
          });
        }
      } catch (error) {
        console.error("Error checking subdomains:", error);
        ElMessage({
          message: "子域名檢查失敗",
          type: "error",
          duration: 3000,
        });
      }
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
.inputs {
  display: flex;
}
.search-input,
.days-input,
.status-select {
  margin-right: 5px;
  width: 180px;
}
.buttons {
  display: flex;
  gap: 5px;
}
.red-text {
  color: red;
}
.yellow-text {
  color: rgb(171, 171, 58);
}
.green-text {
  color: green;
}
</style>
