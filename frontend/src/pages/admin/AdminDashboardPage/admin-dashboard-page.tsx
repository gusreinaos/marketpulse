//Author: Aditya Kadkhikar, Burak Askan, Michael Larsson
import React from 'react';
import styles from './admin-dashboard-page.module.scss';
import { ModelsListComponent } from '../../../components/admin/ModelsListComponent/models-list-component';
import { Col, Row} from 'react-bootstrap';
import AdminNavbarComponent from '../../../components/admin/AdminNavbarComponent/admin-navbar-component';
import { useParams } from 'react-router-dom';

const AdminDashboardPage: React.FC = () => {

  const { adminId } = useParams();

  return (
    <>
      <AdminNavbarComponent adminId={adminId}/>
      <Row>
        <h2 style={{textAlign: 'center', color: 'white'}}>Welcome to your Dashboard, Admin!</h2>
        <Col xs = {12} sm = {12} md = {6}>
          <div className={styles.adminDashboard}>
            {/* Your dashboard content goes here */}
            <ModelsListComponent modelName='Sentiment Model'/>
          </div>
        </Col>
        <Col xs = {12} sm = {12} md = {6}>
          <div className={styles.adminDashboard}>
            {/* Your dashboard content goes here */}
            <ModelsListComponent modelName='Market Trend Model'/>
          </div>
        </Col>
      </Row>
    </>
  );
};

export default AdminDashboardPage;