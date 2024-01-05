//Author: Oscar Reina, John Berntsson
import React, { useState } from 'react';
import { Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import customerService from '../../../services/customerService';
import styles from './sign-up-component.module.scss';

const SignupComponent: React.FC = () => {
  const navigate = useNavigate()
  const [formData, setFormData] = useState({
    id: '',
    username: '',
    email: '',
    password: '',
  });

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignup = async () => {
    try {
      const newCustomer = await customerService.createCustomer(formData);
      if(newCustomer) {
        navigate('/login');
      }

    } catch (error) {
      console.error('Error creating customer:', error);
    }
  };

  return (
    <div className={styles.signupContainer}>
      <Col xs={12} sm={12} md={12}>
        <form>
          <input className={styles.signup_label} type="text" name="username" placeholder="Full name" value={formData.username} onChange={handleInputChange} />
          <input className={styles.signup_label} type="email" name="email" placeholder="Email" value={formData.email} onChange={handleInputChange} />
          <input className={styles.signup_label} type="password" name="password" placeholder="Password" value={formData.password} onChange={handleInputChange} />
        </form>
        <button type="button" onClick={handleSignup} className={styles.button} >
          <p>Sign up</p>
        </button>
      </Col>
    </div>
  );
};

export default SignupComponent;
