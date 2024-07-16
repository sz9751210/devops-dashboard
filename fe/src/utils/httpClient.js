// src/utils/httpClient.js
import axios from "axios";
import { ElMessage } from "element-plus";

const httpClient = axios.create({
  validateStatus(status) {
    // 當status不在200~504之間時，則表示為失敗
    return status >= 200 && status < 504;
  },
  timeout: 10000,
});

httpClient.defaults.retry = 3; // 重試次數
httpClient.defaults.retryDelay = 1000; // 重試間隔
httpClient.defaults.shouldRetry = true; // 是否重試

httpClient.interceptors.request.use(
  (config) => {
    // 設置headers
    config.headers = {
      "Content-Type": "application/json",
      "Accept-Language": "zh-TW",
      Authorization: localStorage.getItem("token"),
    };
    if (config.method === "post") {
      if (!config.data) {
        config.data = {};
      }
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

httpClient.interceptors.response.use(
  (response) => {
    if (response.status !== 200 && response.status !== 201) {
      ElMessage.error(response.data.message || "Error");
      return Promise.reject(response.data);
    }
    return response.data;
  },
  (error) => {
    ElMessage.error(error.message || "Error");
    return Promise.reject(error);
  }
);

export default httpClient;
