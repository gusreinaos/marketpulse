//Author: Michael Larsson, Wojciech Pechmann, Oscar Reina
import React, { useContext, useEffect, useState } from 'react';
import { Col, Row } from 'react-bootstrap';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import CustomerNavbarComponent from '../../../components/customer/CustomerNavBarComponent/customer-navbar-component';
import PredictionCardComponent from '../../../components/customer/PredictionCardComponent/prediction-card-component';
import FavButton from '../../../components/customer/FavButtonComponent/fav-button-component';
import ValueCardComponent from '../../../components/customer/ValueCardComponent/value-card-component';
import GraphComponent from '../../../components/customer/GraphComponent/graph-component';
import { MarketTrendPredictionRequest } from '../../../domain/entities/marketTrendPrediction';
import MediaPostComponent from '../../../components/customer/MediaPostComponent/media-post-component';

import companyService from '../../../services/companyService';
import styles from './company-dashboard-page.module.scss';
import CompanyService from '../../../services/companyService';
import ModelService from '../../../services/modelService';
import { AuthContext } from '../../../contexts/authContext';


const CompanyDashboardPage: React.FC = () => {
  const location = useLocation();
  const navigate = useNavigate();
  const { customerId } = useParams();
  const searchParams = new URLSearchParams(location.search);

  const contextValue = useContext(AuthContext);

  const companyName = searchParams.get('name');
  const user = contextValue?.user;

  const [messageData, setMessageData] = useState([
      {
      message: '',
      user: '',
      time: ''
      }
  ])

  const requestData: MarketTrendPredictionRequest = {
    requestCompany: companyName || "",
    requestTimeStamp: new Date()
  };
  const [dynamicChartData, setDynamicChartData] = useState([
    { time: '2023-11-24', value: 0 },
  ]);
  const [prediction, setPrediction] = useState<number | undefined>(undefined);
  const [stockTrend, setStockTrend] = useState<number | undefined>(undefined);
  const [inflationTrend, setInflationTrend] = useState<number | undefined>(undefined);
  const [sentimentVal, setSentimentVal] = useState<number>();

  const [isLoading, setIsLoading] = useState(true);

  useEffect(() => {
    if (!user) {
      navigate('/');
      return;
    }

    try{

      const handleCompanySearch = async () => {
        try {
          const companyHistorySearch = await companyService.getCompanyHistory(
            companyName ?? '')
          const arrayFormat = Object.values(companyHistorySearch) as { time: string; value: number; }[];
          setDynamicChartData(arrayFormat);
        } catch (error) {
          console.error('Error fetching company history:', error);
        }
      };
  
      const handleMessageRetrieval = async () => {
        try{
          const messages = await companyService.getCompanyTestimonials(
            companyName ?? '')
            const topMessages = messages.slice(0, 5).map((message: { body: any; user: any; created_at: any; }) => ({
              message: message.body,
              user: message.user.username,
              time: message.created_at
            }));
          setMessageData(topMessages)
        } catch (error) {
          console.error('Error searching for testimonials of company')
        }
      }
  
  
      const fetchPrediction = async () => {
        try {
          const predictionResult = await ModelService.getCurrentModelPrediction(
            predictionRequestData.requestCompany
          );
          setPrediction(predictionResult.prediction_value);
          setSentimentVal(predictionResult.avg_sentiment);
        } catch (error) {
          console.error('Error fetching prediction:', error);
        }
      };
  
      const fetchStockTrend = async () => {
        try {
          const stockTrend = await CompanyService.getCurrentStockTrend(
            predictionRequestData.requestCompany
          );
          setStockTrend(stockTrend);
        } catch (error) {
          console.error('Error fetching stock trend:', error);
        }
      };
  
      const fetchInflationTrend = async () => {
        try {
          const inflationTrend = await CompanyService.getCurrentInflationTrend();
          setInflationTrend(inflationTrend);
        } catch (error) {
          console.error('Error fetching inflation trend:', error);
        }
      };
  
      handleCompanySearch()
      handleMessageRetrieval()
      fetchPrediction();
      fetchStockTrend();
      fetchInflationTrend();
    }
    catch(error) {
      console.log(error)
    }
    finally {
    
      setTimeout(() => {
        setIsLoading(false);
      }, 10000);
    }

  }, [contextValue?.user, companyName, setDynamicChartData, setMessageData])



  const predictionRequestData: any = {
    requestCompany: companyName || '',
    prediction: prediction,
    stockTrend: stockTrend,
    inflationTrend: inflationTrend,
    requestTimeStamp: new Date(),
    sentimentVal: sentimentVal
  };

  if (isLoading) {
    return (
      <div className={styles.loading__screen}>
        <CustomerNavbarComponent userId={customerId} />
        <div className={styles.loading__screen__title__container}>
          <p className={styles.loading__screen__title}>Loading our most recent information!</p>
        </div>
        <span className={styles.loader}></span>
      </div>
    );
  }

  return (
    <div className={styles.page}>
      <CustomerNavbarComponent userId={customerId} />
      <div className={styles.wrapper}>
        <div className={styles.top_container}>
          {predictionRequestData.requestCompany} Analysis 
        <FavButton data={ {company_id:companyName?companyName:''} }></FavButton>
          
        </div>
        <Row className={styles.main_container}>
          <Col xs={12} lg={7}>
            <Row className={styles.left_container}>
              <Col xs={12} sm={6} md={6} className={styles.left_card}>
                <PredictionCardComponent requestData={predictionRequestData} />
              </Col>
              <Col xs={12} sm={6} md={6} className={styles.right_card}>
                <ValueCardComponent sentiment={predictionRequestData.sentimentVal} />
              </Col>
            </Row>
            <div className={styles.chartContainer}>
              <Col xs={12} sm={12} md={12}>
                <GraphComponent data={dynamicChartData} />
              </Col>
            </div>
          </Col>
          <Col xs={12} sm={12} md={5} className={styles.right_container}>
            <div>
              <h4 className={styles.mediaTitle}>Media Posts</h4>
              {messageData.length > 0 ? (
                messageData.map((message, index) => (
                  <MediaPostComponent key={index} data={message}></MediaPostComponent>
                ))
              ) : (
                <p>No media posts available</p>
              )}
            </div>
          </Col>
        </Row>
      </div>
    </div>
  );
};

export default CompanyDashboardPage;
