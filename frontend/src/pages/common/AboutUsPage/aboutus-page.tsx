import React from 'react';
import NavbarComponent from '../../../components/common/NavBarComponent/navbar-component';
import styles from './aboutus-page.module.scss';
import { AuthContext } from '../../../contexts/authContext';
import { useContext } from 'react';
import CustomerNavbarComponent from '../../../components/customer/CustomerNavBarComponent/customer-navbar-component';
const AboutUsPage: React.FC = () => {
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
      return <CustomerNavbarComponent />;
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
        <h1 className={styles.welcome_text}>About
          <br></br>Market Pulse</h1>
          <p className={styles.introduction}>Placeholder text. We are not giving financial advice.</p>
      </div>
      </div>
      
      
    </div>
    </div>
    
  );
};

export default AboutUsPage;
