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
      <el-button type="primary" @click="handleSearch">搜尋</el-button>
    </div>

    <!-- table -->
    <el-table
      :data="pagedData"
      style="width: 100%"
      @sort-change="handleSortChange"
    >
      <el-table-column prop="domain" label="域名" width="180" />
      <el-table-column prop="subdomain" label="子域名" width="180" />
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
import { fetchDomain, updateDomainStatus } from "@/api/certificate";
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
              update_time: subdomain.update_time || "N/A",
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
      let filteredData = this.domainData.filter(item => item.expiry_date === "N/A");

      if (this.searchDomain) {
        filteredData = filteredData.filter((item) =>
          item.domain.includes(this.searchDomain)
        );
      }

      if (this.searchStatus !== null) {
        filteredData = filteredData.filter(
          (item) => item.status === this.searchStatus
        );
      }

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
      this.currentPage = 1;
      this.sortAndPageData();
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
.status-select {
  margin-right: 5px;
  width: 180px;
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
