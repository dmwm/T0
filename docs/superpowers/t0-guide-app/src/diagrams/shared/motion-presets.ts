import type { Transition } from "framer-motion";

export const easeOut: Transition = {
  duration: 0.45,
  ease: [0.16, 1, 0.3, 1],
};

export const spring: Transition = {
  type: "spring",
  stiffness: 280,
  damping: 28,
};

export const arrowDraw: Transition = {
  duration: 0.55,
  ease: [0.4, 0, 0.2, 1],
};

export const fadeIn: Transition = {
  duration: 0.3,
  ease: "easeOut",
};

export const NODE_VARIANTS = {
  hidden: { opacity: 0.18, scale: 0.96 },
  active: {
    opacity: 1,
    scale: 1.04,
    transition: spring,
  },
  visited: {
    opacity: 0.85,
    scale: 1,
    transition: easeOut,
  },
};
