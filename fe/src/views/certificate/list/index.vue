<template>
  <div>
    <!-- header -->
    <div class="header"></div>

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
        prop="update_time"
        label="更新時間"
        width="150"
        sortable
      />
      <el-table-column prop="check" label="狀態" width="100" />
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
import { fetchDomain } from "@/api/certificate";

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
              check: subdomain.check,
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
      let sortedData = [...this.domainData];

      if (this.sortColumn) {
        sortedData.sort((a, b) => {
          let result = 0;
          if (a[this.sortColumn] < b[this.sortColumn]) {
            result = -1;
          } else if (a[this.sortColumn] > b[this.sortColumn]) {
            result = 1;
          }
          return this.sortOrder === "ascending" ? result : -result;
        });
      }

      const start = (this.currentPage - 1) * this.pageSize;
      const end = start + this.pageSize;
      this.pagedData = sortedData.slice(start, end);
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
