// src/components/customer/SignupComponent.tsx
import React, { useContext, useState } from 'react';
import { Col } from 'react-bootstrap';
import { useNavigate } from 'react-router-dom';
import AuthService from '../../../services/authService';
import styles from './sign-in-component.module.scss';
import NavbarComponent from '../NavBarComponent/navbar-component';

import { AuthContext } from '../../../contexts/authContext';

const SignInComponent: React.FC = () => {
  const navigate = useNavigate();
  const [formData, setFormData] = useState({
    username: '',
    password: '',
  });

  const authContext = useContext(AuthContext);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSignin = async () => {
    try {
      const user = await AuthService.signIn(formData.username, formData.password);
      
      authContext?.login(user);

      if(user!.is_superuser) {
        navigate(`/admins/${user.id}/train`);
      }
      else {
        navigate(`/customers/${user.id}/discover`);
      }
    } catch (error) {
      console.error('Error signing in:', error);
    }
  };

  return (
    <div className={styles.signin_container}>
      <Col xs={12} sm={12} md={12}>
        <form>
          <input
            className={styles.signin_label}
            type="username"
            name="username"
            placeholder="Username"
            value={formData.username}
            onChange={handleInputChange}
          />
          <input
            className={styles.signin_label}
            type="password"
            name="password"
            placeholder="Password"
            value={formData.password}
            onChange={handleInputChange}
          />
        </form>
        <button type="button" onClick={handleSignin} className={styles.button}>
          <p>Sign in</p>
        </button>
      </Col>
    </div>
  );
};

export default SignInComponent;
