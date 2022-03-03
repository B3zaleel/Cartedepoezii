<template>
  <div class="edit-profile">
    <div class="profile-photo">
      <div>
        <img :src="userProfile.imageURL"/>
        <AccountIcon/>
      </div>
      <div>
        <button class="cdp-btn icon danger" @click="removeImage">
          <DeleteIcon/>
        </button>
        <button class="cdp-btn icon" @click="changeImage">
          <SyncIcon/>
          <input
            class="file-input"
            type="file"
            v-show="false"
            accept="image/png,image/jpeg"
            @change="imageInputChange"
          />
        </button>
      </div>
    </div>

    <div class="email">
      <div class="txb-label-over">
        <input
          name="email"
          id="form-email"
          type="email"
          v-model="userProfile.email"
          @focus="inputFocus(inputTypes.Email)"
          @blur="inputBlur(inputTypes.Email)"
        />
        <label
          :class="{label: true, 'roll-up': rollUpEmailLabel}" for="form-email">
          <div>
            <span>Email</span>
          </div>
        </label>
      </div>
    </div>

    <div class="name">
      <div class="txb-label-over">
        <input
          name="name"
          id="form-name"
          type="text"
          v-model="userProfile.name"
          :maxlength="nameLimit"
          @input="updateNameCount"
          @focus="inputFocus(inputTypes.Name)"
          @blur="inputBlur(inputTypes.Name)"
        />
        <label
          :class="{label: true, 'roll-up': rollUpNameLabel}" for="form-name">
          <div>
            <span>Name</span>
            <span
              class="status"
              v-show="nameCount > 0"
            >
              {{ nameCount }} / {{ nameLimit }}
            </span>
          </div>
        </label>
      </div>
    </div>

    <div class="bio">
      <span>Bio</span>
      <textarea
        class="cdp-txb"
        v-model="userProfile.bio"
        rows="4"
      />
    </div>
  </div>
</template>

<script lang="ts">
import {
  Component,
  Prop,
  Watch,
  Vue,
} from 'vue-property-decorator';
import {
  EditProfileForm,
  FileInputEvent,
  ElementInputEvent,
} from '@/assets/scripts/types/interfaces';
import AccountIcon from '@/assets/icons/Account.vue';
import DeleteIcon from '@/assets/icons/Delete.vue';
import SyncIcon from '@/assets/icons/Sync.vue';

@Component({
  name: 'EditProfileView',
  components: {
    AccountIcon,
    DeleteIcon,
    SyncIcon,
  },
})
export default class EditProfileView extends Vue {
  @Prop() userProfile!: EditProfileForm;

  @Prop() updateView!: boolean;

  nameCount = 0;

  nameLimit = 60;

  imageLoadFailed = false;

  imageSrc = '';

  rollUpEmailLabel = true;

  rollUpNameLabel = true;

  inputTypes = {
    None: 0,
    Email: 1,
    Name: 2,
    Bio: 3,
  };

  @Watch('updateView')
  onUpdateViewChanged(val: boolean): void {
    if (val) {
      this.nameCount = this.userProfile.name.length;
      this.inputBlur(this.inputTypes.Email);
      this.inputBlur(this.inputTypes.Name);
    }
  }

  imageLoadError(): void {
    this.imageLoadFailed = true;
  }

  updateNameCount(): void {
    this.nameCount = this.userProfile.name.length;
    this.rollUpEmailLabel = true;
  }

  inputFocus(inputId: number): void {
    switch (inputId) {
      case this.inputTypes.Email: {
        this.rollUpEmailLabel = true;
        break;
      }
      case this.inputTypes.Name: {
        this.rollUpNameLabel = true;
        break;
      }
      default:
        break;
    }
  }

  inputBlur(inputId: number): void {
    switch (inputId) {
      case this.inputTypes.Email: {
        this.rollUpEmailLabel = this.userProfile.email?.length > 0;
        break;
      }
      case this.inputTypes.Name: {
        this.rollUpNameLabel = this.userProfile.name.length > 0;
        break;
      }
      default:
        break;
    }
  }

  changeImage(ev: ElementInputEvent): void {
    let button = ev.target;
    if (button) {
      if (button.nodeName === 'svg' && button.parentElement) {
        button = button.parentElement;
      } else if (button.nodeName === 'path' && button.parentElement) {
        if (button.parentElement.parentElement) {
          button = button.parentElement.parentElement;
        }
      }
      const inputElement = button.getElementsByTagName('input').item(0);
      if (inputElement) {
        inputElement.click();
      }
    }
    this.imageSrc = '';
  }

  imageInputChange(ev: FileInputEvent): void {
    if (ev && ev.target) {
      const imageFiles = ev.target.files;

      if (imageFiles && imageFiles.length > 0) {
        const reader = new FileReader();
        reader.addEventListener('load', (e) => {
          if (e && e.target && e.target.result) {
            this.$emit('image-uploaded', String(e.target.result));
          }
        });
        reader.readAsDataURL(imageFiles[0]);
      }
    }
  }

  removeImage(): void {
    this.$emit('image-deleted');
  }

  created(): void {
    this.nameCount = this.userProfile.name.length;
    this.inputBlur(this.inputTypes.Email);
    this.inputBlur(this.inputTypes.Name);
  }

  mounted(): void {
    this.nameCount = this.userProfile.name.length;
    this.inputBlur(this.inputTypes.Email);
    this.inputBlur(this.inputTypes.Name);
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/textboxes';
@use '@/assets/styles/views/settings/edit_profile';
</style>
