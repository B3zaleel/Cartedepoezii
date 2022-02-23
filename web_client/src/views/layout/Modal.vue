<template>
  <div
    :class="{'modal-view': true, hidden: !modalOpen}"
    @mousedown.self="closeDialog"
  >
    <div>
      <div class="header">
        <div>
          <b>{{ modalTitle }}</b>
        </div>
        <div>
          <button @click="closeDialog" class="close-btn">
            <CloseIcon />
          </button>
        </div>
      </div>

      <div class="content">
        <slot name="modal-body"></slot>
      </div>

      <div class="footer">
        <slot name="modal-action-panel"></slot>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import CloseIcon from '@/assets/icons/Close.vue';

@Component({
  components: {
    CloseIcon,
  },
}) export default class MainLayout extends Vue {
  @Prop() modalOpen!: boolean;

  @Prop() modalTitle!: string;

  @Prop() hasHeader!: boolean;

  @Prop() hasFooter!: boolean;

  closeDialog(ev: Event): void {
    ev.preventDefault();
    ev.stopPropagation();
    this.$emit('request-close');
  }
}
</script>

<style lang="scss">
.modal-view {
  position: fixed;
  display: flex;
  top: 0;
  left: 0;
  right: 0;
  width: 100%;
  height: 100%;
  align-items: center;
  justify-content: center;
  justify-items: center;
  z-index: 600;
  background: hsla(0, 0%, 80%, 0.4);

  > div {
    position: relative;
    display: flex;
    flex-flow: column;
    width: fit-content;
    max-width: 80%;
    height: clamp(100px, 100%, calc(100% - 2 * 20px));
    max-width: 600px;
    background: white;
    border-radius: 10px;
    box-shadow: 0 0 2px 2px var(--shadow-color);

    > .header {
      display: grid;
      grid-template-columns: calc(100% - 60px) 60px;
      box-shadow: 0px 0px 1px 2px rgba(220, 220, 220, 0.767);
      border-top-left-radius: inherit;
      border-top-right-radius: inherit;

      b {
        font-size: 14pt;
      }

      > div:nth-child(2) {
        display: flex;
        justify-content: flex-end;
      }

      > div:nth-child(1) {
        display: flex;
        align-items: center;
        justify-items: flex-start;
        padding: 5px 10px;
      }

      > div:nth-child(2) {
        display: flex;
        align-items: center;
        justify-items: center;
        padding: 5px 10px;
      }

      &.hidden {
        display: none;
      }
    }

    .close-btn {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      padding: 2.5px;
      background: gray;
      border: none;
      border-radius: 50%;
      cursor: pointer;

      &:hover {
        background: gainsboro;
        color: white;
        fill: var(--primary-color-full);
      }

      > svg {
        width: 25px;
        height: 25px;
      }
    }

    > .content {
      padding: 10px;
      overflow: auto;
    }

    > .footer {
      display: flex;
      justify-content: flex-end;
      box-shadow: 0px 0px 1px 2px var(--shadow-color);
      border-bottom-left-radius: inherit;
      border-bottom-right-radius: inherit;

      &.hidden {
        display: none;
      }
    }
  }

  &.hidden {
    display: none;
  }
}
</style>
