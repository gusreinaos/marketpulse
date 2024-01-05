//Author: Oscar Reina, John Berntsson
import React, { useContext, useState, useEffect } from 'react';
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
  const [errorMessage, setErrorMessage] = useState('');

  //Transform the API response to match the AuthContext user object
 
  const authContext = useContext(AuthContext);

  const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };
  useEffect(() => {
  if (authContext?.user) {
    if (authContext?.user?.is_superuser) {
      navigate(`/admins/${authContext?.user?.id}/train`);
    } else {
      navigate(`/customers/${authContext?.user?.id}/discover`);
    }
  }
}, [authContext?.user, navigate]);
  const handleSignin = async () => {
    try {
      const user = await AuthService.signIn(formData.username, formData.password);
      authContext?.login(user);
    } catch (error) {
      console.error('Error signing in:', error);
      setErrorMessage('Invalid username or password');
    }
  };
 
  return (
    <div className={styles.signin_container}>
      <Col xs={12} sm={12} md={12}>
         {/* Display error message if it exists */}
    {errorMessage && <div className={styles.error_message}>{errorMessage}</div>}

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
