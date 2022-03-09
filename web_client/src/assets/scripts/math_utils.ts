import { Point2D } from '@/assets/scripts/types/interfaces';

/**
 * A collection of mathematical functions.
 */
export default class MathUtils {
  /**
   * Converts an angle in degrees to radians.
   * @param deg The angle in degrees.
   * @returns number
   */
  static degToRad = (deg: number): number => ((deg % 360) / 180) * Math.PI;

  /**
   * Rotates a point in the clockwise direction about a given angle.
   * @param {Point2D} pivot - The center of rotation.
   * @param radius - The radius of the rotation track.
   * @param angle - The angle of the clockwise rotation in degrees.
   */
  static rotatePoint = (pivot: Point2D, radius: number, angle: number): Point2D => {
    let acuteAngle = 0;
    const directions = { x: 0, y: 0 };
    if ((angle > 0) && (angle <= 90)) {
      acuteAngle = 90 - angle;
      directions.x = 1;
      directions.y = 1;
    } else if ((angle > 90) && (angle <= 180)) {
      acuteAngle = angle - 90;
      directions.x = 1;
      directions.y = -1;
    } else if ((angle > 180) && (angle <= 270)) {
      acuteAngle = 270 - angle;
      directions.x = -1;
      directions.y = -1;
    } else if ((angle > 270) && (angle <= 360)) {
      acuteAngle = angle - 270;
      directions.x = -1;
      directions.y = 1;
    }
    const radAngle = -MathUtils.degToRad(acuteAngle);
    const s = Math.sin(radAngle);
    const c = Math.cos(radAngle);
    const xExt = radius * c;
    const yExt = radius * s;
    const newPt = {
      x: xExt * directions.x + pivot.x,
      y: yExt * directions.y + pivot.y * (angle !== 0 ? 1 : 0),
    };
    return newPt;
  };

  static formatNumber = (num: number, withDecimal = false): string => {
    const ranks = ['', 'K', 'M', 'B', 'T'];
    let idx = 0;
    let rem = 0;
    let total = num;
    const base = 1000;
    let useDecimal = withDecimal;

    while (total > base) {
      rem = Math.floor((total % base) / 100);
      total = Math.floor(total / base);
      idx += 1;
    }
    if (!rem) {
      useDecimal = false;
    }
    return useDecimal
      ? `${total}.${rem}${ranks[idx]}`
      : `${total}${ranks[idx]}`;
  };
}
