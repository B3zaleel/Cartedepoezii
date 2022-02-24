export default class MathUtils {
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
    return useDecimal ? `${total}.${rem}${ranks[idx]}` : `${total}${ranks[idx]}`;
  };
}
