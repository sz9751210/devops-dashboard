const { defineConfig } = require("@vue/cli-service");
module.exports = defineConfig({
  devServer: {
    host: "0.0.0.0",
    port: 7070,
    open: true, // 啟動後自動打開頁面
    proxy: {
      "/api": {
        target: "http://backend:9090",
        changeOrigin: true,
        // pathRewrite: { "^/api": "" },
      },
    },
    headers: {
      "Access-Control-Allow-Origin": "*",
    },
  },
  transpileDependencies: true, // 忽略警告
  lintOnSave: false, // 禁用eslint, 關閉語法檢查
});
