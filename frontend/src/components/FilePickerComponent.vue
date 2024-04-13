<template>
  <div class="file-picker flex items-center content-center flex-col mt-7">
    <FileUpload
      name="image"
      accept="image/*"
      chooseLabel="Select Image"
      mode="basic"
      @uploader="onImageSelect"
      :auto="true"
      :customUpload="true"
    />

    <ButtonPrime v-if="!loading" class="mt-5" @click="submitImage" :disabled="!imageUrl"
      >Submit the image</ButtonPrime
    >
    <ProgressSpinner v-if="loading" style="width: 35px; height: 35px" class="mt-4" />

    <template v-if="imageUrl">
      <div class="mt-4 w-2/3">
        <img :src="imageUrl" alt="Selected Image" class="max-w-full h-auto" />
      </div>
    </template>

    <template v-if="result !== null">
      <p class="font-bold">
        According to the scan you have provided, we think that
        {{ result === false ? 'there is no cancer' : 'there IS a cancer' }}
      </p>
    </template>
  </div>
</template>

<script>
import axios from 'axios'
import FileUpload from 'primevue/fileupload'
import { mapState } from 'pinia'
import { useUserStore } from '@/stores/user'
import ButtonPrime from 'primevue/button'
import ProgressSpinner from 'primevue/progressspinner'

export default {
  components: {
    FileUpload,
    ButtonPrime,
    ProgressSpinner
  },
  data() {
    return {
      imageUrl: null,
      result: null,
      loading: false,
      files: []
    }
  },
  computed: {
    ...mapState(useUserStore, {
      token: (state) => state.token
    })
  },
  methods: {
    submitImage() {
      if (this.files.length > 0) {
        const formData = new FormData()

        formData.append('file', this.files[0])
        this.loading = true

        console.log(this.token)

        axios({
          method: 'post',
          url: `${import.meta.env.VITE_API_URL}/upload/image?token=${this.token}`,
          data: formData,
          headers: { 'Content-Type': 'multipart/form-data' }
        })
          .then(({ data }) => {
            this.result = data.result.model_result
            this.$emit('updateResult', this.result)
          })
          .catch((error) => {
            console.error('Error:', error)
          })
          .finally(() => {
            this.loading = false
          })
      }
    },

    onImageSelect(event) {
      this.files = event.files
      const reader = new FileReader()

      reader.onload = (e) => {
        this.imageUrl = e.target.result
      }

      if (this.files.length > 0) {
        reader.readAsDataURL(this.files[0])
      }
    }
  }
}
</script>
