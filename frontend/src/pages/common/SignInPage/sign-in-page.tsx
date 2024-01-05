//Author: Oscar Reina, John Berntsson
import React from 'react';
import { Link } from 'react-router-dom';
import Navbar from '../../../components/common/NavBarComponent/navbar-component';
import SignInComponent from '../../../components/common/SignInComponent/sign-in-component';
import styles from './sign-in-page.module.scss';

const SignInPage: React.FC = () => {
  return (
    <div>
        <Navbar/>
        <div className={styles.signin_page}>
            <h1>Log in to your account</h1>
            <SignInComponent />
        </div>
    </div>
    
  );
};

export default SignInPage;
