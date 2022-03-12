<template>
  <div class="poem-edit">
    <div class="title">
      <div class="txb-label-over">
        <input
          name="title"
          type="text"
          :id="inputId"
          v-model="poem.title"
          :maxlength="titleLimit"
          @focus="titleInputFocus"
          @blur="titleInputBlur"
        />
        <label
          :class="{label: true, 'roll-up': canRollUpTitleLabel}"
          :for="inputId"
        >
          <div>
            <span>Title</span>
            <span
              class="status"
              v-show="titleCount > 0"
            >
              {{ titleCount }} / {{ titleLimit }}
            </span>
          </div>
        </label>
      </div>
    </div>

    <span class="verses-header">Verses</span>

    <div class="verses-pane">
      <div class="input-pane">
        <textarea
          class="cdp-txb"
          v-model="poem.verses[currentVerse - 1]"
          rows="5"
        />
      </div>

      <div class="nav-pane">
        <button class="cdp-btn icon" @click="moveLeft">
          <ArrowLeftIcon/>
        </button>
        <span class="page-status">
          {{ currentVerse }} / {{ poem.verses.length }}
        </span>
        <button class="cdp-btn icon" @click="moveRight">
          <ArrowRightIcon/>
        </button>
      </div>

      <div class="mod-pane">
        <button class="cdp-btn icon danger" @click="removeVerse">
          <DeleteIcon/>
        </button>
        <button class="cdp-btn icon" @click="addVerse">
          <PlusCircleOutlineIcon/>
        </button>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { EditPoemForm } from '@/assets/scripts/types/interfaces';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import ArrowRightIcon from '@/assets/icons/ArrowRight.vue';
import PlusCircleOutlineIcon from '@/assets/icons/PlusCircleOutline.vue';
import DeleteIcon from '@/assets/icons/Delete.vue';

@Component({
  name: 'PoemEditComponent',
  computed: {
    titleCount() {
      return this.$props.poem.title?.length || 0;
    },
    canRollUpTitleLabel() {
      return ((this.$props.poem?.title.length || 0) > 0) || this.$data.inputFocused;
    },
  },
  components: {
    ArrowLeftIcon,
    ArrowRightIcon,
    PlusCircleOutlineIcon,
    DeleteIcon,
  },
})
export default class PoemEditComponent extends Vue {
  @Prop() poem!: EditPoemForm;

  @Prop({ default: `${new Date().toISOString()}` }) inputId!: string;

  titleLimit = 256;

  currentVerse = 1;

  inputFocused = false;

  titleInputFocus(): void {
    this.inputFocused = true;
  }

  titleInputBlur(): void {
    this.inputFocused = false;
  }

  addVerse(): void {
    this.$emit('add-verse', this.currentVerse - 1);
  }

  removeVerse(): void {
    this.$emit('remove-verse', this.currentVerse - 1);
    if (this.currentVerse > this.poem.verses.length) {
      this.currentVerse = this.poem.verses.length;
    }
  }

  moveLeft(): void {
    if (this.currentVerse > 1) {
      this.currentVerse -= 1;
    }
  }

  moveRight(): void {
    if (this.currentVerse < this.poem.verses.length) {
      this.currentVerse += 1;
    }
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/textboxes';
@use '@/assets/styles/components/poem_edit';
</style>
