import React from 'react';
import Navbar from '../../../components/common/NavBarComponent/navbar-component';
import styles from './landing-page.module.scss';
import arrowImage from '../../../assets/arrow-right.png'

const LandingPage: React.FC = () => {

  return (
    <div className={styles.page}>
      <div className={styles.landing_page}>
      <Navbar></Navbar>
      <div className={styles.page_container}>
        <div className={styles.main_container}>
        <h1 className={styles.welcome_text}>Welcome to 
          <br></br>Market Pulse</h1>
          <p className={styles.introduction}>Discover the latest market trends and insights.</p>
          <div className={styles.button_container}>
            <a className={styles.button}>
              Get started
              <img className={styles.arrow} src={arrowImage} alt="Arrow right" />
            </a>
          </div>
      </div>
      </div>
      
      
    </div>
    </div>
    
  );
};

export default LandingPage;
