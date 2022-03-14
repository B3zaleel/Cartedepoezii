<template>
  <span class="doughnut-status" :title="titleValue">
    <svg
      :width="width"
      :height="width"
      :viewBox="`0 0 ${width} ${width}`"
    >
      <g :class="{track: true, hidden: value < 1, danger: value >= 0.94}">
        <circle class="outer" :r="outerRadius" :cx="outerRadius" :cy="outerRadius"/>
        <circle class="inner" :r="innerRadius" :cx="outerRadius" :cy="outerRadius"/>
      </g>
      <path
        :class="{
          arc: true,
          hidden: value == 0 || value == 1,
          warning: value < 0.94 && value > 0.8,
          danger: value >= 0.94,
        }"
        :d="getArcPath()"
      />
    </svg>
  </span>
</template>

<script lang="ts">
import { Component, Prop, Vue } from 'vue-property-decorator';
import MathUtils from '@/assets/scripts/math_utils';

@Component({
  name: 'DoughnutStatusIcon',
  computed: {
    innerRadius() {
      return this.$props.width / 2 - this.$props.thickness;
    },
    outerRadius() {
      return this.$props.width / 2;
    },
  },
})
export default class DoughnutStatusIcon extends Vue {
  @Prop({ default: 0 }) value!: number;

  @Prop({ default: 20 }) width!: number;

  @Prop({ default: 2 }) thickness!: number;

  @Prop({ default: '' }) titleValue!: string;

  MathUtils = MathUtils;

  getArcPath(): string {
    const radius = {
      inner: this.width / 2 - this.thickness,
      outer: this.width / 2,
    };
    const angle = Math.floor(this.value * 360);
    const largeFlag = angle >= 180 ? 1 : 0;
    const center = {
      x: this.width / 2,
      y: this.width / 2,
    };
    const outerEndPt = this.MathUtils.rotatePoint(center, radius.outer, angle);
    const innerEndPt = this.MathUtils.rotatePoint(center, radius.inner, angle);
    const pathData = [
      `M ${center.x} ${this.thickness}`,
      `L ${center.x} ${0}`,
      `A ${radius.outer} ${radius.outer} `,
      `${angle} ${largeFlag} 1 ${outerEndPt.x} ${outerEndPt.y}`,
      `M ${center.x} ${this.thickness}`,
      `A ${radius.inner} ${radius.inner} `,
      `${angle} ${largeFlag} 1 ${innerEndPt.x} ${innerEndPt.y}`,
      `L ${outerEndPt.x} ${outerEndPt.y}`,
    ].join('');
    return pathData;
  }
}
</script>

<style lang="scss">
@use "@/assets/styles/animated_icons/doughnut_status";
</style>
