import React from 'react';
import styles from './Header.module.scss';

const Header: React.FC = () => {
  return (
    <header className={styles.header}>
      {/* Your header content goes here */}
      <h1>Market Pulse</h1>
    </header>
  );
};

export default Header;
