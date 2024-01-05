//Author: Oscar Reina, John Berntsson
import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../../../components/common/NavBarComponent/navbar-component';
import SignupComponent from '../../../components/customer/SignUpComponent/sign-up-component';// Import your SignUp component
import styles from './sign-up-page.module.scss';

const SignUpPage: React.FC = () => {
  return (
      <div>
          <Navbar/>
          <div className={styles.landingPage}>
      <h1>Welcome to Market Pulse</h1>
      <p>Discover the latest market trends and insights.</p>
      <SignupComponent />
    </div>
      </div>
    
  );
};

export default SignUpPage;
