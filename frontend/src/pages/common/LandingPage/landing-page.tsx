//Author: Oscar Reina, John Berntsson
import React from 'react';
import NavbarComponent from '../../../components/common/NavBarComponent/navbar-component';
import styles from './landing-page.module.scss';
import arrowImage from '../../../assets/arrow-right.png'
import { AuthContext } from '../../../contexts/authContext';
import { useContext } from 'react';
import CustomerNavbarComponent from '../../../components/customer/CustomerNavBarComponent/customer-navbar-component';
import AdminNavbarComponent from '../../../components/admin/AdminNavbarComponent/admin-navbar-component';

const LandingPage: React.FC = () => {
  const authContext = useContext(AuthContext);
  const redirect = () => {
    if (authContext?.user) {
      if (authContext?.user?.is_superuser) {
        return `/admins/${authContext?.user.id}/train`;
      } else {
        return `/customers/${authContext?.user.id}/discover`;
      }
    }
    else {
      return '/signup';
    }
  }
  const navbar = () => {
    if (authContext?.user) {
      if (authContext?.user?.is_superuser) {
        return <AdminNavbarComponent />;
      }
      else return <CustomerNavbarComponent />;
    } else {
      return <NavbarComponent />;
    }
  };
  
  return (
    <div className={styles.page}>
      <div className={styles.landing_page}>
      <div>
      {navbar()} 
     
    </div>
      <div className={styles.page_container}>
        <div className={styles.main_container}>
        <h1 className={styles.welcome_text}>Welcome to 
          <br></br>Market Pulse</h1>
          <p className={styles.introduction}>Discover the latest market trends and insights.</p>
          <div className={styles.button_container}>
            <a className={styles.button} href={redirect()}>
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
