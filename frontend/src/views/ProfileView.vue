<template>
  <div class="bg-slate-50 w-full h-full flex items-center justify-center">
    <div class="container flex flex-col items-center w-3/4 bg-white p-4 rounded shadow-md">
      <h2>User Logs</h2>
      <ProgressSpinner v-if="loading" class="mb-5 mt-5" style="width: 35px; height: 35px" />

      <DataTable v-else :value="logs" class="w-full" scrollable scrollHeight="400px">
        <Column field="model_result" header="Result"></Column>
        <Column field="image_name" header="Image Name"></Column>
        <Column field="user_id" header="User Id"></Column>
        <Column field="username" header="Username"></Column>
      </DataTable>
    </div>
  </div>
</template>

<script>
import ProgressSpinner from 'primevue/progressspinner'
import { useUserStore } from '@/stores/user'
import { mapState } from 'pinia'

import DataTable from 'primevue/datatable'
import Column from 'primevue/column'

export default {
  name: 'LogsView',
  components: { ProgressSpinner, DataTable, Column },
  data() {
    return {
      loading: false,
      logs: []
    }
  },
  mounted() {
    this.loading = true

    this.axios(`${import.meta.env.VITE_API_URL}/upload/history?token=${this.token}`, {
      method: 'GET'
    })
      .then(({ data }) => {
        this.logs = data.result
      })
      .catch((error) => {
        console.error(error)
      })
      .finally(() => {
        this.loading = false
      })
  },
  computed: {
    ...mapState(useUserStore, {
      token: (state) => state.token
    })
  }
}
</script>

<style lang="scss" scope></style>
