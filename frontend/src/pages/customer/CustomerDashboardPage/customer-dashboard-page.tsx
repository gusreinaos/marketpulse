//Author: Wojciech Pechmann
import React, { useContext, useEffect, useState } from 'react';
import { Col, Row } from 'react-bootstrap';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import CustomerNavbarComponent from '../../../components/customer/CustomerNavBarComponent/customer-navbar-component';
import CompactStockCardComponent from '../../../components/customer/CompactStockCardComponent/compact-stock-card-component';
import FavButton from '../../../components/customer/FavButtonComponent/fav-button-component';
import { CompanyPrediction } from '../../../domain/entities/companyPrediction';
import styles from './customer-dashboard-page.module.scss';
import ModelService from '../../../services/modelService';
import { AuthContext } from '../../../contexts/authContext';
import customerService from '../../../services/customerService';

const CustomerDashboardPage: React.FC = () => {
 
  const authContext = useContext(AuthContext);
  const navigate = useNavigate();

  const contextValue = useContext(AuthContext);

  const id = contextValue?.user?.id;



  const  cmps =  [
    {
    company_code: "AAPL",
    company_name: "Apple inc.",
    prediction_value: 1.9,
    created_at: "2023-12-02",
    avg_sentiment: 0.5,
    tweet_rate: 5,
    stock_val: 10
  },
  {
    company_code: "META",
    company_name: "Facebook",
    prediction_value: 2,
    created_at: "2023-12-03",
    avg_sentiment: 0.7,
    tweet_rate: 3,
    stock_val: 12
  },
] as CompanyPrediction[]


  
  const [companies, setCompanies] = useState([]);
  const [hasRun, setRun] = useState(false);
  const [renderList, setRender] = useState([] as JSX.Element[]);

 
  const getCompanyData = async () => {
    try {
      const list_companies = await customerService.getCustomerFavorites(id?id:'');

      const rList = list_companies.map(company => (<CompactStockCardComponent companyInfo={company} />))

      setRender(rList)      

      setRun(true)

    } catch (error) {
      console.error('Error while fetching predictions:', error);
    }
  };


  if(!hasRun){
    getCompanyData();
  }
  


  

  return (
    <div className={styles.page}>
      <CustomerNavbarComponent userId={'customerId'} />
      <div className={styles.wrapper}>
        <div className={styles.top_container}>
        Your favorite companies
        </div>
        <Row className={styles.main_container}>
          <Col xs={12} lg={7}>
            <div>
              <Col xs={12} sm={12} md={12} className={styles.render_list}>
                {renderList}
              </Col>
            </div>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default CustomerDashboardPage;
