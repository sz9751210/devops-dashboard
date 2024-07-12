<template>
  <div>
    <!-- header -->
    <div class="header">
      <el-input 
        v-model="domainInput" 
        placeholder="請輸入域名" 
        @keyup.enter="fetchCertificate" 
        style="width: 250px;"></el-input>
      <el-button type="primary" @click="fetchCertificate" style="margin-left: 5px;">Check</el-button>
      <el-button @click="clearInput" style="margin-left: 5px;">Clear</el-button>
    </div>

    <!-- certificate info -->
    <div v-if="certificateData" class="certificate-info">
      <el-card>
        <div>
          <span>域名：</span><strong>{{ certificateData.domain }}</strong>
        </div>
        <div>
          <span>簽發給：</span><strong>{{ certificateData.issuedTo }}</strong>
        </div>
        <div>
          <span>簽發者：</span><strong>{{ certificateData.issuedBy }}</strong>
        </div>
        <div>
          <span>有效期從：</span><strong>{{ certificateData.validFrom }}</strong>
        </div>
        <div>
          <span>有效期至：</span><strong>{{ certificateData.validUntil }}</strong>
        </div>
      </el-card>
    </div>

    <!-- Error message -->
    <div v-if="errorMessage" class="error-message">
      {{ errorMessage }}
    </div>
  </div>
</template>

<script>
import { fetchCertificate } from "@/api/certificate"; // 修改這行，確保路徑正確

export default {
  data() {
    return {
      domainInput: '',
      certificateData: null,
      errorMessage: ''
    };
  },
  methods: {
    async fetchCertificate() {
      this.certificateData = null; // 清除之前的數據
      this.errorMessage = ''; // 清除之前的錯誤消息
      try {
        const response = await fetchCertificate(this.domainInput);
        if (response.data.error) {
          this.errorMessage = response.data.error;
        } else {
          this.certificateData = response.data;
        }
      } catch (error) {
        console.error("Error fetching certificate data:", error);
        this.errorMessage = "獲取憑證數據時發生錯誤，請稍後再試。";
      }
    },
    clearInput() {
      this.domainInput = '';
      this.certificateData = null;
      this.errorMessage = '';
    }
  }
};
</script>

<style scoped>
.header {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}
.certificate-info {
  margin-bottom: 20px;
}
.error-message {
  color: red;
}
</style>
