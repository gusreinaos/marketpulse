import React from 'react';
import styles from './Footer.module.scss';

const Footer: React.FC = () => {
  return (
    <footer className={styles.footer}>
      {/* Your footer content goes here */}
      <p>&copy; 2023 Market Pulse. All rights reserved.</p>
    </footer>
  );
};

export default Footer;
