<template>
  <div class="register-container">
    <div class="register-box">
      <h2>Register</h2>
      <form @submit.prevent="register">
        <input
          type="text"
          v-model="username"
          placeholder="Username"
          required
          class="input-field"
        />
        <input
          type="password"
          v-model="password"
          placeholder="Password"
          required
          class="input-field"
        />
        <button type="submit" class="register-button">Register</button>
      </form>
      <p class="login-message">
        Already have an account? <a @click="goToLogin">Login</a>
      </p>
    </div>
  </div>
</template>

<script>
import { registerUser } from "@/api/auth";
import { ElMessage } from "element-plus";

export default {
  data() {
    return {
      username: "",
      password: "",
      timer: null,
      countdown: 5,
      messageInstance: null,
    };
  },
  methods: {
    async register() {
      try {
        const response = await registerUser({
          username: this.username,
          password: this.password,
        });
        console.log("response", response);
        if (response.code === 201) {
          this.startCountdown();
        } else {
          ElMessage({
            message: response.message,
            type: "error",
          });
        }
      } catch (error) {
        console.log("error", error);
        ElMessage({
          message: "註冊過程中發生錯誤",
          type: "error",
        });
      }
    },
    startCountdown() {
      // 显示初始消息
      this.messageInstance = ElMessage({
        message: `註冊成功，${this.countdown}秒後將跳轉到登錄頁面`,
        type: "success",
        duration: 0, // 消息不会自动消失
        showClose: true, // 显示关闭按钮
      });

      // 每秒更新消息
      this.timer = setInterval(() => {
        this.countdown--;
        if (this.countdown > 0) {
          // 先关闭当前消息实例
          this.messageInstance.close();
          // 然后显示新消息
          this.messageInstance = ElMessage({
            message: `註冊成功，${this.countdown}秒後將跳轉到登錄頁面`,
            type: "success",
            duration: 0,
            showClose: true,
          });
        } else {
          clearInterval(this.timer);
          this.messageInstance.close();
          this.$router.push("/login");
        }
      }, 1000);
    },
    goToLogin() {
      this.$router.push({ name: "Login" });
    },
  },
};
</script>

<style scoped>
.register-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.register-box {
  background-color: #ffffff;
  padding: 2em;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  text-align: center;
  width: 300px;
}

h2 {
  color: #3a3a3a;
  margin-bottom: 1em;
}

.input-field {
  width: 100%;
  padding: 0.5em;
  margin-bottom: 1em;
  border: 1px solid #e0e0e0;
  border-radius: 4px;
  box-sizing: border-box;
}

.register-button {
  width: 100%;
  padding: 0.5em;
  background-color: #1976d2;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.register-button:hover {
  background-color: #1565c0;
}

.login-message {
  margin-top: 1em;
  color: #3a3a3a;
}

.login-message a {
  color: #1976d2;
  cursor: pointer;
  text-decoration: none;
}

.login-message a:hover {
  text-decoration: underline;
}
</style>
