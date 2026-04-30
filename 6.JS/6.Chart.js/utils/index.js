let seed = Date.now();

const CHART_COLORS = {
  red: "rgb(255, 99, 132)",
  orange: "rgb(255, 159, 64)",
  yellow: "rgb(255, 205, 86)",
  green: "rgb(75, 192, 192)",
  blue: "rgb(54, 162, 235)",
  purple: "rgb(153, 102, 255)",
  grey: "rgb(201, 203, 207)",
};

const COLORS = [
  "#4dc9f6",
  "#f67019",
  "#f53794",
  "#537bc4",
  "#acc236",
  "#166a8f",
  "#00a950",
  "#58595b",
  "#8549ba",
];

const NAMED_COLORS = [
  CHART_COLORS.red,
  CHART_COLORS.orange,
  CHART_COLORS.yellow,
  CHART_COLORS.green,
  CHART_COLORS.blue,
  CHART_COLORS.purple,
  CHART_COLORS.grey,
];

const valueOrDefault = (value, defaultValue) =>
  value === undefined ? defaultValue : value;

const clampCount = (value, defaultValue) => {
  const total = Math.floor(valueOrDefault(value, defaultValue));
  return Math.max(0, total);
};

const hexToRgb = (hex) => {
  const normalized = hex.replace("#", "");
  const expanded =
    normalized.length === 3
      ? normalized
          .split("")
          .map((char) => char + char)
          .join("")
      : normalized;

  const value = Number.parseInt(expanded, 16);

  return {
    r: (value >> 16) & 255,
    g: (value >> 8) & 255,
    b: value & 255,
  };
};

const parseColor = (value) => {
  if (value.startsWith("#")) {
    return hexToRgb(value);
  }

  const match = value.match(/\d+(?:\.\d+)?/g);

  if (!match || match.length < 3) {
    return { r: 0, g: 0, b: 0 };
  }

  return {
    r: Number(match[0]),
    g: Number(match[1]),
    b: Number(match[2]),
  };
};

const Utils = {
  CHART_COLORS,

  srand(seedValue) {
    seed = seedValue;
  },

  rand(min, max) {
    const start = valueOrDefault(min, 0);
    const end = valueOrDefault(max, 0);

    seed = (seed * 9301 + 49297) % 233280;

    return start + (seed / 233280) * (end - start);
  },

  numbers(config = {}) {
    const min = valueOrDefault(config.min, 0);
    const max = valueOrDefault(config.max, 100);
    const from = valueOrDefault(config.from, []);
    const count = clampCount(config.count, 8);
    const decimals = valueOrDefault(config.decimals, 8);
    const continuity = valueOrDefault(config.continuity, 1);
    const factor = 10 ** decimals;
    const data = [];

    for (let index = 0; index < count; index += 1) {
      const value = (from[index] || 0) + this.rand(min, max);

      if (this.rand() <= continuity) {
        data.push(Math.round(factor * value) / factor);
      } else {
        data.push(null);
      }
    }

    return data;
  },

  points(config = {}) {
    const xs = this.numbers(config);
    const ys = this.numbers(config);

    return xs.map((x, index) => ({ x, y: ys[index] }));
  },

  bubbles(config = {}) {
    return this.points(config).map((point) => ({
      ...point,
      r: this.rand(config.rmin, config.rmax),
    }));
  },

  labels(config = {}) {
    const min = valueOrDefault(config.min, 0);
    const max = valueOrDefault(config.max, 100);
    const count = clampCount(config.count, 8);
    const decimals = valueOrDefault(config.decimals, 8);
    const prefix = valueOrDefault(config.prefix, "");
    const factor = 10 ** decimals;
    const step = count === 0 ? 0 : (max - min) / count;
    const values = [];

    if (count === 0) {
      return values;
    }

    for (let index = 0; index < count; index += 1) {
      const value = min + step * index;
      values.push(`${prefix}${Math.round(factor * value) / factor}`);
    }

    return values;
  },

  months({ count = 12, section } = {}) {
    const total = clampCount(count, 12);
    const values = [];

    for (let index = 0; index < total; index += 1) {
      const monthLabel = `${(index % 12) + 1}월`;
      values.push(section ? monthLabel.substring(0, section) : monthLabel);
    }

    return values;
  },

  color(index) {
    return COLORS[index % COLORS.length];
  },

  transparentize(value, opacity) {
    const alpha = opacity === undefined ? 0.5 : 1 - opacity;
    const { r, g, b } = parseColor(value);

    return `rgba(${r}, ${g}, ${b}, ${alpha})`;
  },

  namedColor(index) {
    return NAMED_COLORS[index % NAMED_COLORS.length];
  },

  newDate(days = 0) {
    const date = new Date();
    date.setDate(date.getDate() + days);
    return date;
  },

  newDateString(days = 0) {
    return this.newDate(days).toISOString();
  },

  parseISODate(value) {
    return new Date(value);
  },
};

window.Utils = Utils;
