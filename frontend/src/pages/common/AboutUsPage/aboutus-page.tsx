//Author: John Berntsson
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
          <p className={styles.introduction}>Welcome to MarketPulse, where innovation meets insight in the dynamic world of financial markets. At MarketPulse, we are passionate about decoding the complexities of market trends, empowering you to make informed decisions.

Our cutting-edge software harnesses the power of sentiment data to predict market movements with unparalleled accuracy. We understand that in the fast-paced world of trading, having a competitive edge is crucial. That's why MarketPulse is here—to provide you with a strategic advantage.

What sets us apart is our commitment to innovation and precision. MarketPulse employs state-of-the-art algorithms and advanced analytics, transforming raw sentiment data into actionable insights. Whether you're a seasoned trader or a novice investor, our user-friendly platform ensures that market predictions are not just reserved for experts.

Why choose MarketPulse?

Accurate Predictions: Our software analyzes sentiment data from diverse sources, allowing you to stay ahead of market shifts.

User-Friendly Interface: Navigate the complex world of trading with ease. MarketPulse is designed to be intuitive, ensuring that you can make data-driven decisions effortlessly.

Innovation at its Core: We are at the forefront of technological advancements, continuously refining our algorithms to adapt to the ever-changing landscape of financial markets.

Transparent and Reliable: Trust is the foundation of our relationship with users. MarketPulse provides transparent insights, giving you the confidence to navigate the markets with clarity.

At MarketPulse, we believe in empowering you to take control of your financial destiny. Join us on this journey, where technology and expertise converge to redefine the way you approach the markets.

Discover the power of prediction with MarketPulse—because your success is our mission.</p>
      </div>
      </div>
      
      
    </div>
    </div>
    
  );
};

export default AboutUsPage;
