//Author: Oscar Reina, Wojciech Pechmann
import React, { useState } from 'react';
import styles from './navbar-component.module.scss';
import { routes } from './routes';
import arrowRight from '../../../assets/arrow-right.png';

const NavbarComponent = () => {
  const [isMenuOpen, setMenuOpen] = useState(false);

  const toggleMenu = () => {
    setMenuOpen(!isMenuOpen);
  };

  return (
    <>
      <nav>
        <div className={styles.navbar_container}>
          <a href="/"><div className={styles.marketpulse}>MarketPulse</div></a>
          <div className={`${styles.navbar} ${isMenuOpen ? styles.active : ''}`}>
            <div className={styles.navbar_menu}>
            {routes.map((route: any) => (
              <a key={route.name} href={route.href} className="navbar__link">
                {route.name}
              </a>
            ))}
          </div>
          <div className={styles.login_signup}>
            <a href='/login' className={styles.login}>Log in</a>
            <a href='/signup' className={styles.signup}>
              <button className={styles.signup_button}>Become a member</button>
              <img className={styles.arrow} src={arrowRight} alt="Arrow right" />
            </a>
          </div>
          </div>
          <div className={styles.hamburger_menu} onClick={toggleMenu}>
            <div className={`${styles.bar} ${isMenuOpen ? styles.bar1 : ''}`}></div>
            <div className={`${styles.bar} ${isMenuOpen ? styles.bar2 : ''}`}></div>
            <div className={`${styles.bar} ${isMenuOpen ? styles.bar3 : ''}`}></div>
          </div>
        </div>
      </nav>
    </>
  );
};

export default NavbarComponent;
