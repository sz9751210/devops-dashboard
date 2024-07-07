<template>
  <div>
    <h4>Grafana</h4>
    <el-table :data="tableData" border style="width: 100%">
      <el-table-column label="Website" width="180">
        <template v-slot="scope">
          <a :href="scope.row.link" target="_blank" class="custom-link">{{
            scope.row.name
          }}</a>
        </template>
      </el-table-column>
      <el-table-column width="250" prop="username" label="UserName" />
      <el-table-column label="PassWord">
        <template v-slot="scope">
          <div style="display: flex; align-items: center">
            <span>{{
              scope.row.showPassword ? scope.row.password : "******"
            }}</span>
            <el-icon
              @click="togglePassword(scope.row)"
              style="margin-left: 10px; cursor: pointer"
            >
              <component :is="scope.row.showPassword ? 'hide' : 'view'" />
            </el-icon>
            <el-button
              @click="copyPassword(scope.row.password)"
              style="
                margin-left: 10px;
                border: none;
                background-color: transparent;
              "
              icon="copy-document"
            >
            </el-button>
          </div>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script>
import common from "../common/Config.js";
import httpClient from "../../utils/httpClient.js";
export default {
  data() {
    return {
      tableData: [],
      linkListUrl: common.linkListUrl,
    };
  },
  mounted() {
    this.getLinkList();
  },
  methods: {
    getLinkList() {
      httpClient
        .get(this.linkListUrl)
        .then((response) => {
          this.tableData = response.data;
        })
        .catch((error) => {
          console.log(error);
        });
    },
    togglePassword(row) {
      row.showPassword = !row.showPassword;
    },
    async copyPassword(password) {
      try {
        await navigator.clipboard.writeText(password);
        this.$message({
          message: "Password copied to clipboard",
          type: "success",
        });
      } catch (err) {
        this.$message({
          message: "Failed to copy password",
          type: "error",
        });
      }
    },
  },
};
</script>
<style scoped>
.custom-link {
  color: #409eff; /* Element Plus primary color */
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s ease;
}

.custom-link:hover {
  color: #66b1ff;
  text-decoration: underline;
}
</style>
