<template>
  <div class="poem-edit">
    <div class="title">
      <div class="txb-label-over">
        <input
          name="title"
          id="form-title"
          type="text"
          v-model="poem.title"
          :maxlength="titleLimit"
          @input="updateTitleCount"
          @focus="titleInputFocus"
          @blur="titleInputBlur"
        />
        <label
          :class="{label: true, 'roll-up': rollUpTitleLabel}" for="form-title">
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

    <b>Verses</b>

    <div class="verses-pane">
      <textarea class="cdp-txb" v-model="poem.verse[currentVerse - 1]"/>
      <div>
        <button class="cdp-btn icon danger">
          <DeleteIcon/>
        </button>
        <button class="cdp-btn icon">
          <PlusCircleOutlineIcon/>
        </button>
      </div>
    </div>

    <div class="verses-nav-pane">
      <button class="cdp-btn icon">
        <ArrowLeftIcon/>
      </button>
      <span class="page-status">
        {{ currentVerse }} / {{ poem.verses.length }}
      </span>
      <button class="cdp-btn icon">
        <ArrowRightIcon/>
      </button>
      </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import { Poem } from '@/assets/scripts/type_defs';
import ArrowLeftIcon from '@/assets/icons/ArrowLeft.vue';
import ArrowRightIcon from '@/assets/icons/ArrowRight.vue';
import PlusCircleOutlineIcon from '@/assets/icons/PlusCircleOutline.vue';
import DeleteIcon from '@/assets/icons/Delete.vue';

@Component({
  name: 'PoemEditComponent',
  components: {
    ArrowLeftIcon,
    ArrowRightIcon,
    PlusCircleOutlineIcon,
    DeleteIcon,
  },
})
export default class PoemEditComponent extends Vue {
  @Prop() poem!: Poem;

  @Prop() headerTitle!: string;

  titleCount = 0;

  titleLimit = 256;

  currentVerse = 1;

  rollUpTitleLabel = true;

  updateTitleCount(): void {
    this.titleCount = this.poem?.title.length || 0;
    this.rollUpTitleLabel = true;
  }

  titleInputFocus(): void {
    this.rollUpTitleLabel = true;
  }

  titleInputBlur(): void {
    this.rollUpTitleLabel = (this.poem?.title.length || 0) > 0;
  }

  created(): void {
    this.rollUpTitleLabel = this.poem?.title.length > 0 || false;
  }
}
</script>

<style lang="scss">
@use '@/assets/styles/textboxes';
@use '@/assets/styles/components/poem_edit';

</style>
