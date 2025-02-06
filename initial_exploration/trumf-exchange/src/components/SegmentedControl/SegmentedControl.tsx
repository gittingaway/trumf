import { useState } from "react";
import { motion } from "framer-motion";
import styles from "./SegmentedControl.module.css";

const SegmentedControl = ({ options, defaultIndex = 0, onChange }) => {
  const [selectedIndex, setSelectedIndex] = useState(defaultIndex);

  const handleSelect = (index) => {
    setSelectedIndex(index);
    if (onChange) onChange(options[index]);
  };

  return (
    <div className={styles.container}>
      <motion.div
        className={styles.slider}
        layoutId="segmentedControl"
        transition={{
          type: "smooth",
          stiffness: 300,
          damping: 20,
          bounceDamping: 300,
        }}
        style={{
          width: `${100 / options.length}%`,
          height: "100%",
          top: 0,
          left: `${(100 / options.length) * selectedIndex}%`,
        }}
      />
      {options.map((option, index) => (
        <button
          key={option}
          className={`${styles.button} ${selectedIndex === index ? styles.selected : ""}`}
          onClick={() => handleSelect(index)}
        >
          {option}
        </button>
      ))}
    </div>
  );
};

export default SegmentedControl;
