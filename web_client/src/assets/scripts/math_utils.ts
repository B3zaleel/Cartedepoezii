export default class MathUtils {
  static formatNumber = (num: number, withDecimal = false): string => {
    const ranks = ['', 'K', 'M', 'B', 'T'];
    let idx = 0;
    let rem = 0;
    let total = num;
    const base = 1000;

    while (total > base) {
      rem = Math.floor((total % base) / 100);
      total = Math.floor(total / base);
      idx += 1;
    }
    return withDecimal ? `${total}.${rem}${ranks[idx]}` : `${total}${ranks[idx]}`;
  };
}
