import { motion } from "framer-motion";
import { arrowDraw, easeOut, spring } from "./motion-presets";

export type NodeState = "hidden" | "active" | "visited";

interface NodeProps {
  x: number;
  y: number;
  width?: number;
  height?: number;
  label: string;
  sublabel?: string;
  state: NodeState;
  variant?: "default" | "db" | "external" | "process";
  onClick?: () => void;
}

const VARIANT_FILL: Record<NonNullable<NodeProps["variant"]>, string> = {
  default: "var(--bg-elevated)",
  db: "var(--accent-soft)",
  external: "var(--code-bg)",
  process: "var(--bg-elevated)",
};

const VARIANT_STROKE: Record<NonNullable<NodeProps["variant"]>, string> = {
  default: "var(--rule)",
  db: "var(--accent)",
  external: "var(--muted)",
  process: "var(--rule)",
};

export function Node({
  x,
  y,
  width = 132,
  height = 56,
  label,
  sublabel,
  state,
  variant = "default",
  onClick,
}: NodeProps) {
  const isActive = state === "active";
  const isVisited = state === "visited";
  return (
    <motion.g
      initial={false}
      animate={{
        opacity: state === "hidden" ? 0.22 : 1,
        scale: isActive ? 1.04 : 1,
      }}
      transition={spring}
      style={{
        cursor: onClick ? "pointer" : "default",
        transformOrigin: `${x + width / 2}px ${y + height / 2}px`,
      }}
      onClick={onClick}
    >
      <motion.rect
        x={x}
        y={y}
        width={width}
        height={height}
        rx={10}
        ry={10}
        fill={VARIANT_FILL[variant]}
        animate={{
          stroke: isActive
            ? "var(--accent)"
            : isVisited
            ? "color-mix(in srgb, var(--accent) 55%, transparent)"
            : VARIANT_STROKE[variant],
          strokeWidth: isActive ? 2.5 : 1.5,
        }}
        transition={easeOut}
      />
      {isActive ? (
        <motion.rect
          x={x - 4}
          y={y - 4}
          width={width + 8}
          height={height + 8}
          rx={14}
          fill="none"
          stroke="var(--accent)"
          strokeWidth={1.5}
          initial={{ opacity: 0.6, scale: 0.96 }}
          animate={{ opacity: [0.5, 0, 0.5], scale: [1, 1.05, 1] }}
          transition={{ duration: 1.6, repeat: Infinity, ease: "easeInOut" }}
          style={{
            transformOrigin: `${x + width / 2}px ${y + height / 2}px`,
          }}
        />
      ) : null}
      <text
        x={x + width / 2}
        y={sublabel ? y + height / 2 - 4 : y + height / 2 + 4}
        textAnchor="middle"
        fontSize={13}
        fontWeight={600}
        fill="var(--fg)"
        style={{ pointerEvents: "none" }}
      >
        {label}
      </text>
      {sublabel ? (
        <text
          x={x + width / 2}
          y={y + height / 2 + 12}
          textAnchor="middle"
          fontSize={10.5}
          fill="var(--muted)"
          style={{ pointerEvents: "none" }}
        >
          {sublabel}
        </text>
      ) : null}
    </motion.g>
  );
}

interface DBNodeProps {
  x: number;
  y: number;
  label: string;
  sublabel?: string;
  state: NodeState;
}

export function DBNode({ x, y, label, sublabel, state }: DBNodeProps) {
  const w = 110;
  const h = 64;
  const ellipseRy = 8;
  const isActive = state === "active";
  return (
    <motion.g
      initial={false}
      animate={{ opacity: state === "hidden" ? 0.22 : 1 }}
      transition={easeOut}
    >
      <motion.path
        d={dbCylinderPath(x, y, w, h, ellipseRy)}
        fill="var(--accent-soft)"
        animate={{
          stroke: isActive ? "var(--accent)" : "color-mix(in srgb, var(--accent) 60%, transparent)",
          strokeWidth: isActive ? 2.4 : 1.4,
        }}
        transition={easeOut}
      />
      <text
        x={x + w / 2}
        y={y + h / 2 + (sublabel ? -2 : 4)}
        textAnchor="middle"
        fontSize={12.5}
        fontWeight={600}
        fill="var(--fg)"
        style={{ pointerEvents: "none" }}
      >
        {label}
      </text>
      {sublabel ? (
        <text
          x={x + w / 2}
          y={y + h / 2 + 12}
          textAnchor="middle"
          fontSize={10}
          fill="var(--muted)"
          style={{ pointerEvents: "none" }}
        >
          {sublabel}
        </text>
      ) : null}
    </motion.g>
  );
}

function dbCylinderPath(x: number, y: number, w: number, h: number, ry: number) {
  const top = `M ${x} ${y + ry} a ${w / 2} ${ry} 0 1 0 ${w} 0 a ${w / 2} ${ry} 0 1 0 ${-w} 0`;
  const sides = `M ${x} ${y + ry} L ${x} ${y + h - ry} a ${w / 2} ${ry} 0 0 0 ${w} 0 L ${x + w} ${y + ry}`;
  return `${top} ${sides}`;
}

interface ArrowProps {
  d: string;
  show: boolean;
  highlight?: boolean;
  label?: string;
  labelPos?: { x: number; y: number };
  delay?: number;
}

export function Arrow({
  d,
  show,
  highlight = false,
  label,
  labelPos,
  delay = 0,
}: ArrowProps) {
  return (
    <>
      <motion.path
        d={d}
        fill="none"
        stroke={highlight ? "var(--accent)" : "var(--muted)"}
        strokeWidth={highlight ? 2.2 : 1.6}
        strokeLinecap="round"
        strokeLinejoin="round"
        markerEnd={highlight ? "url(#arrowhead-active)" : "url(#arrowhead)"}
        initial={{ pathLength: 0, opacity: 0 }}
        animate={{
          pathLength: show ? 1 : 0,
          opacity: show ? 1 : 0,
        }}
        transition={{ ...arrowDraw, delay }}
      />
      {label && labelPos && show ? (
        <motion.text
          x={labelPos.x}
          y={labelPos.y}
          textAnchor="middle"
          fontSize={10.5}
          fontWeight={500}
          fill={highlight ? "var(--accent)" : "var(--muted)"}
          initial={{ opacity: 0, y: labelPos.y - 4 }}
          animate={{ opacity: 1, y: labelPos.y }}
          transition={{ ...arrowDraw, delay: delay + 0.3 }}
        >
          {label}
        </motion.text>
      ) : null}
    </>
  );
}

export function ArrowheadDefs() {
  return (
    <defs>
      <marker
        id="arrowhead"
        viewBox="0 0 10 10"
        refX="8"
        refY="5"
        markerWidth="6"
        markerHeight="6"
        orient="auto-start-reverse"
      >
        <path d="M0,0 L10,5 L0,10 z" fill="var(--muted)" />
      </marker>
      <marker
        id="arrowhead-active"
        viewBox="0 0 10 10"
        refX="8"
        refY="5"
        markerWidth="7"
        markerHeight="7"
        orient="auto-start-reverse"
      >
        <path d="M0,0 L10,5 L0,10 z" fill="var(--accent)" />
      </marker>
    </defs>
  );
}

interface ClusterProps {
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
  show?: boolean;
}

export function Cluster({
  x,
  y,
  width,
  height,
  label,
  show = true,
}: ClusterProps) {
  return (
    <motion.g
      initial={{ opacity: 0 }}
      animate={{ opacity: show ? 1 : 0.25 }}
      transition={easeOut}
    >
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        rx={14}
        fill="color-mix(in srgb, var(--accent) 4%, transparent)"
        stroke="var(--rule)"
        strokeDasharray="4 4"
        strokeWidth={1}
      />
      <text
        x={x + 12}
        y={y + 18}
        fontSize={11}
        fontWeight={600}
        fill="var(--muted)"
        letterSpacing="0.06em"
      >
        {label.toUpperCase()}
      </text>
    </motion.g>
  );
}

interface StateBubbleProps {
  x: number;
  y: number;
  r?: number;
  label: string;
  active: boolean;
  visited?: boolean;
}

export function StateBubble({
  x,
  y,
  r = 36,
  label,
  active,
  visited = false,
}: StateBubbleProps) {
  return (
    <motion.g
      animate={{ scale: active ? 1.1 : 1 }}
      transition={spring}
      style={{ transformOrigin: `${x}px ${y}px` }}
    >
      <motion.circle
        cx={x}
        cy={y}
        r={r}
        fill={active ? "var(--accent-soft)" : "var(--bg-elevated)"}
        animate={{
          stroke: active
            ? "var(--accent)"
            : visited
            ? "color-mix(in srgb, var(--accent) 55%, transparent)"
            : "var(--rule)",
          strokeWidth: active ? 2.5 : 1.5,
        }}
        transition={easeOut}
      />
      <text
        x={x}
        y={y + 4}
        textAnchor="middle"
        fontSize={11}
        fontWeight={600}
        fill="var(--fg)"
        style={{ pointerEvents: "none" }}
      >
        {label}
      </text>
    </motion.g>
  );
}

interface LaneProps {
  x: number;
  y: number;
  width: number;
  height: number;
  label: string;
}

export function Lane({ x, y, width, height, label }: LaneProps) {
  return (
    <g>
      <rect
        x={x}
        y={y}
        width={width}
        height={height}
        fill="none"
        stroke="var(--rule)"
        strokeDasharray="4 4"
      />
      <rect
        x={x}
        y={y}
        width={84}
        height={height}
        fill="var(--code-bg)"
      />
      <text
        x={x + 8}
        y={y + 18}
        fontSize={11}
        fontWeight={600}
        fill="var(--muted)"
        letterSpacing="0.05em"
      >
        {label}
      </text>
    </g>
  );
}
