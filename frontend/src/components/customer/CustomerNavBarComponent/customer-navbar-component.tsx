import React, { useContext, useState } from 'react';
import styles from './customer-navbar-component.module.scss';
import { routes } from './routes';
import arrowRight from '../../../assets/arrow-right.png';
import { AuthContext } from '../../../contexts/authContext';
import { useNavigate } from 'react-router-dom';

const CustomerNavbarComponent = ({ userId }: { userId?: string }) => {
  const [isMenuOpen, setMenuOpen] = useState(false);
  const authContext = useContext(AuthContext);
  const navigate = useNavigate()

  const toggleMenu = () => {
    setMenuOpen(!isMenuOpen);
  };

  const handleLogout = () => {
    authContext?.logout();
    navigate('/');
  };

  return (
    <>
      <nav>
        <div className={styles.navbar_container}>
          <a href="/"><div className={styles.marketpulse}>MarketPulse</div></a>
          <div className={`${styles.navbar} ${isMenuOpen ? styles.active : ''}`}>
            <div className={styles.navbar_menu}>
            {routes.map((route: any) => (
              <a
                key={route.name}
                href={route.href.replace(':customerId', userId || '')}
                className="navbar__link"
              >
                {route.name}
              </a>
            ))}
          </div>
          <div className={styles.user_section}>
            <a className={styles.login}>Profile page</a>
            <button className={styles.logout_button} onClick={handleLogout}>
              Log out
              <img className={styles.arrow} src={arrowRight} alt="Arrow right" />
            </button>
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

export default CustomerNavbarComponent;
