<template>
  <div class="login-container">
    <div class="login-box">
      <h2>Login</h2>
      <form @submit.prevent="login">
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
        <button type="submit" class="login-button">Login</button>
      </form>
      <p v-if="message" class="error-message">{{ message }}</p>
      <p class="register-message">
        Don't have an account? <a @click="goToRegister">Register</a>
      </p>
    </div>
  </div>
</template>

<script>
import { loginUser } from "@/api/auth";

export default {
  data() {
    return {
      username: "",
      password: "",
      message: "",
    };
  },
  methods: {
    async login() {
      try {
        const response = await loginUser({
          username: this.username,
          password: this.password,
        });
        console.log(response);
        if (response.code === 200) {
          localStorage.setItem("token", response.token);

          // 確保返回到之前用戶想訪問的頁面或首頁
          const redirect = this.$route.query.redirect || "/";
          this.$router.push(redirect);
        } else {
          this.message = response.message;
        }
      } catch (error) {
        console.error(error);
        this.message = "登入過程中發生錯誤";
      }
    },
    goToRegister() {
      this.$router.push({ name: "Register" });
    },
  },
};
</script>

<style scoped>
.login-container {
  display: flex;
  justify-content: center;
  align-items: center;
  height: 100vh;
  background-color: #f5f5f5;
}

.login-box {
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

.login-button {
  width: 100%;
  padding: 0.5em;
  background-color: #1976d2;
  color: #ffffff;
  border: none;
  border-radius: 4px;
  cursor: pointer;
}

.login-button:hover {
  background-color: #1565c0;
}

.error-message {
  color: red;
  margin-top: 1em;
}

.register-message {
  margin-top: 1em;
  color: #3A3A3A;
}

.register-message a {
  color: #1976D2;
  cursor: pointer;
  text-decoration: none;
}

.register-message a:hover {
  text-decoration: underline;
}
</style>
