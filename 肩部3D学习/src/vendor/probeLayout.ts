export type ScreenPoint = { x: number; y: number };

export type ProbeCalloutLayoutInput = {
  /** Screen position each callout points at. */
  targets: readonly ScreenPoint[];
  /** Every projected point of the probe, used to keep labels clear of it. */
  extent: readonly ScreenPoint[];
  heights: readonly number[];
  width: number;
  viewport: { width: number; height: number };
  /** Screen width kept free on the right (the docked annotation column). */
  reservedRight: number;
  /** Screen height kept free at the top and bottom (captions, help text). */
  reservedTop?: number;
  reservedBottom?: number;
};

export type ProbeCalloutLayout = {
  side: 'left' | 'right';
  x: number;
  /** Top edge of each label, in the order of `targets`. */
  ys: number[];
};

const MARGIN = 8;
const GAP = 4;
const OFFSET = 26;

/**
 * Stack callout labels in one column beside a projected probe. Labels never overlap one
 * another; their order follows the probe on screen so that leader lines do not cross.
 */
export function layoutProbeCallouts(input: ProbeCalloutLayoutInput): ProbeCalloutLayout {
  const { targets, heights, width, viewport } = input;
  const extent = input.extent.length ? input.extent : targets;
  const top = MARGIN + (input.reservedTop ?? 0);
  const bottom = viewport.height - MARGIN - (input.reservedBottom ?? 0);
  const xs = extent.map(point => point.x);
  const minX = Math.min(...xs), maxX = Math.max(...xs);
  const rightLimit = Math.max(MARGIN + width, viewport.width - input.reservedRight);
  const leftRoom = minX - OFFSET - MARGIN;
  const rightRoom = rightLimit - (maxX + OFFSET);
  const side: 'left' | 'right' = leftRoom >= width || leftRoom >= rightRoom ? 'left' : 'right';
  const rawX = side === 'left' ? minX - OFFSET - width : maxX + OFFSET;
  const x = Math.min(Math.max(rawX, MARGIN), Math.max(MARGIN, rightLimit - width));

  // Order labels along the probe as it appears on screen.
  const ys = extent.map(point => point.y);
  const mostlyVertical = Math.max(...ys) - Math.min(...ys) >= maxX - minX;
  const order = targets.map((_, i) => i).sort((a, b) => {
    if (mostlyVertical) return targets[a].y - targets[b].y || a - b;
    // Horizontal probe: the target farthest from the label column gets the top label.
    const distance = (i: number) => Math.abs(targets[i].x - (side === 'left' ? x + width : x));
    return distance(b) - distance(a) || a - b;
  });
  const placed = new Array<number>(targets.length).fill(0);
  let cursor = -Infinity;
  for (const i of order) {
    const ideal = targets[i].y - heights[i] / 2;
    placed[i] = Math.max(ideal, cursor);
    cursor = placed[i] + heights[i] + GAP;
  }
  if (order.length) {
    const first = order[0], last = order[order.length - 1];
    const overflow = placed[last] + heights[last] - bottom;
    if (overflow > 0) order.forEach(i => { placed[i] -= overflow; });
    const underflow = top - placed[first];
    if (underflow > 0) order.forEach(i => { placed[i] += underflow; });
  }
  return { side, x, ys: placed };
}
