<template>
  <v-container class="register-container">
    <v-row justify="center" align="center" class="min-height-screen">
      <v-col>
        <v-card class="pa-6 border-radius-large box-shadow-1">
          <div class="text-center mb-6">
            <h1 class="text-h4 mb-2">Регистрация</h1>
            <p class="text-body-2 text-grey">Создайте новый аккаунт</p>
          </div>

          <v-alert
            v-if="error"
            type="error"
            variant="tonal"
            class="mb-4"
            closable
            @click:close="error = ''"
          >
            {{ error }}
          </v-alert>

          <v-form @submit.prevent="handleRegister">
            <v-text-field
              v-model="name"
              label="Имя"
              prepend-inner-icon="mdi-account"
              variant="outlined"
              class="mb-4"
              :rules="nameRules"
              required
            />

            <v-text-field
              v-model="email"
              label="Email"
              type="email"
              prepend-inner-icon="mdi-email"
              variant="outlined"
              class="mb-4"
              :rules="emailRules"
              required
            />

            <v-text-field
              v-model="password"
              label="Пароль"
              type="password"
              prepend-inner-icon="mdi-lock"
              variant="outlined"
              class="mb-4"
              :rules="passwordRules"
              required
            />

            <v-btn
              type="submit"
              color="primary"
              size="large"
              block
              :loading="loading"
              class="mb-4"
            >
              Зарегистрироваться
            </v-btn>
          </v-form>

          <div class="text-center">
            <p class="text-body-2 text-grey">
              Уже есть аккаунт?
              <router-link to="/login" class="text-primary text-decoration-none">
                Войти
              </router-link>
            </p>
          </div>
        </v-card>
      </v-col>
    </v-row>
  </v-container>
</template>

<script setup lang="ts">
import { ref, nextTick } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()

const name = ref('')
const email = ref('')
const password = ref('')
const error = ref('')
const loading = ref(false)

const nameRules = [
  (v: string) => !!v || 'Имя обязательно',
  (v: string) => v.length >= 1 || 'Имя должно быть не менее 1 символа',
  (v: string) => v.length <= 100 || 'Имя должно быть не более 100 символов'
]

const emailRules = [
  (v: string) => !!v || 'Email обязателен',
  (v: string) => /.+@.+\..+/.test(v) || 'Email должен быть валидным'
]

const passwordRules = [
  (v: string) => !!v || 'Пароль обязателен',
  (v: string) => v.length >= 8 || 'Пароль должен быть не менее 8 символов'
]

const handleRegister = async () => {
  error.value = ''
  loading.value = true

  try {
    await userStore.register(email.value, password.value, name.value)
    await nextTick()
    router.push('/main')
  } catch (err: any) {
    error.value = err.response?.data?.detail || err.message || 'Ошибка регистрации. Попробуйте снова.'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.register-container {
  min-height: 100vh;
}

.min-height-screen {
  min-height: calc(100vh - 120px);
}
</style>

