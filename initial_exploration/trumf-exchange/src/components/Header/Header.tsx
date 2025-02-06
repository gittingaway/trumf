import { useEffect, useState } from "react";
import styles from "./Header.module.css";

export default function Header() {
  const [logoPath, setLogoPath] = useState("/trumf_logo.svg");

  useEffect(() => {
    const updatePath = () => {
      console.log("updatePath");
      if (window.innerWidth < 720) {
        setLogoPath("/trumf_logo_small.svg");
      } else {
        setLogoPath("/trumf_logo.svg");
      }
    };
    console.log("useEffect");
    updatePath();
    window.addEventListener("resize", updatePath);
    return () => window.removeEventListener("resize", updatePath);
  }, []);

  return (
    <header className={styles.header}>
      <nav className={styles.nav}>
        <a href="/" className={styles.logo}>
          <img src={logoPath} alt="Astro logo" height="48" />
          <h4>Børsen</h4>
        </a>
      </nav>
    </header>
  );
}
