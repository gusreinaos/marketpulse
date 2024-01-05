//Author: John Berntsson
import React, { useContext, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { Link } from 'react-router-dom';
import Navbar from '../../../components/common/NavBarComponent/navbar-component';
import styles from './customer-profile-page.module.scss';
import { AuthContext } from '../../../contexts/authContext';
import AuthService from '../../../services/authService';
import { render } from '@testing-library/react';
import CustomerNavbarComponent from '../../../components/customer/CustomerNavBarComponent/customer-navbar-component';
import AdminNavbarComponent from '../../../components/admin/AdminNavbarComponent/admin-navbar-component';
import CustomerService from '../../../services/customerService';
import { Col, Row } from 'react-bootstrap';
import { userInfo } from 'os';
import { ToastContainer, toast } from 'react-toastify';
import 'react-toastify/dist/ReactToastify.css';


const CustomerProfilePage: React.FC = () => {
   const {customerId} = useParams();
    const [formData, setFormData] = useState({
        email: '',
        password: '',
      });

      
    const authContext = useContext(AuthContext);
    const current_user = authContext?.user;
    const [currentUser, setCurrentUser] = useState('');
    const handleInputChange = (e: React.ChangeEvent<HTMLInputElement>) => {
      setFormData({ ...formData, [e.target.name]: e.target.value });
       
    };

    const getUserData = async () => {
        try {
          if (current_user){
          const user = await CustomerService.getCustomerById(current_user.id);
          authContext?.setUser(user.data);
          }
        } catch (error) {
          console.error('Error:', error);
        } 
    }
    const notify = (m:string) => toast(m);
    const [errorMessage, setErrorMessage] = useState('');
    interface UpdateData {
      email?: string;
      password?: string;
    }
    const handleUpdateUser = async () => {
      try {
        let updateData: UpdateData = {};
    
        if (formData.email && formData.email.trim() !== '') {
          updateData.email = formData.email;
        }
    
        if (formData.password && formData.password.trim() !== '') {
          updateData.password = formData.password;
        }
        
        if (formData.password && formData.password.trim() === '') {
          setErrorMessage('Enter a valid password');
        }
        
    
        if (Object.keys(updateData).length > 0 && current_user) {
          const updated_user = await CustomerService.updateCustomer(current_user.id, updateData);
          if (updated_user) {
            setErrorMessage('');
            authContext?.setUser(updated_user);
            notify('Profile updated successfully!');
            setFormData({
              email: '',
              password: '',
            });
          }
        }
      } catch (error: any) {
        console.log(error.errors);
        setErrorMessage(error?.email || error?.password || 'Error updating profile.');
        console.error('Error updating customer:', error);
      }
    };
    
    const navbar = () => {
      if (authContext?.user) {
        if (authContext?.user?.is_superuser) {
          return <AdminNavbarComponent />;
        }
        return <CustomerNavbarComponent />;
      } 
    };


  return (
    <div className={styles.page}>
       {navbar()}
        <div className={styles.wrapper}>
        <h2 style={{textAlign: 'center', color: 'white', paddingTop: 50}}>Welcome to your profile {current_user?.username}</h2>
        <div className={styles.page__container}>
          
        <div className={styles.page__title}>
        <div>
      
      <svg xmlns="http://www.w3.org/2000/svg" height="64" viewBox="64 -896 896 896" width="64"><path d="M234-276q51-39 114-61.5T480-360q69 0 132 22.5T726-276q35-41 54.5-93T800-480q0-133-93.5-226.5T480-800q-133 0-226.5 93.5T160-480q0 59 19.5 111t54.5 93Zm246-164q-59 0-99.5-40.5T340-580q0-59 40.5-99.5T480-720q59 0 99.5 40.5T620-580q0 59-40.5 99.5T480-440Zm0 360q-83 0-156-31.5T197-197q-54-54-85.5-127T80-480q0-83 31.5-156T197-763q54-54 127-85.5T480-880q83 0 156 31.5T763-763q54 54 85.5 127T880-480q0 83-31.5 156T763-197q-54 54-127 85.5T480-80Zm0-80q53 0 100-15.5t86-44.5q-39-29-86-44.5T480-280q-53 0-100 15.5T294-220q39 29 86 44.5T480-160Zm0-360q26 0 43-17t17-43q0-26-17-43t-43-17q-26 0-43 17t-17 43q0 26 17 43t43 17Zm0-60Zm0 360Z"/></svg>
      
    <p>{current_user?.username} </p>
    {current_user?.email}
    </div>
        
        <div className={styles.user_data}>
        
      </div>
        
        </div>
       <div className={styles.verticalLine}></div>
        <div className={styles.info_container}>
        <Row xs={12} sm={12} md={12} style={{textAlign:'center'}}>
        <form>
        {errorMessage && <div className={styles.error_message}>{errorMessage}</div>}

        
          <input
            className={styles.info_label}
            type="email"
            name="email"
            placeholder="New email"
            value={formData.email}
            onChange={handleInputChange}
          />
          <div>
        
          </div>
          <input
            className={styles.info_label}
            type="password"
            name="password"
            placeholder="New password"
            value={formData.password}
            onChange={handleInputChange}
          /><button type="button" onClick={handleUpdateUser} className={styles.button}>
          <p>Update</p>
        </button>
        </form>
        
        
      </Row>
          </div>
        </div>
      </div>
      <ToastContainer/>
        </div>
    
 );
};

export default CustomerProfilePage;
