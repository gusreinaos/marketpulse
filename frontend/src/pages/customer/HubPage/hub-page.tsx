//Author: Wojciech Pechmann
import React, { useContext, useEffect, useState } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import CustomerNavbarComponent from '../../../components/customer/CustomerNavBarComponent/customer-navbar-component';
import SortButton from '../../../components/customer/SortButtonComponent/sort-button-component';
import FavButton from '../../../components/customer/FavButtonComponent/fav-button-component';
import { MarketTrendPredictionRequest } from '../../../domain/entities/marketTrendPrediction';
import companyService from '../../../services/companyService';
import styles from './hub-page.module.scss';
import CompanyService from '../../../services/companyService';
import ModelService from '../../../services/modelService';
import { AuthContext } from '../../../contexts/authContext';
import customerService from '../../../services/customerService';
import { CompanyPrediction } from '../../../domain/entities/companyPrediction';
import { SortState } from '../../../domain/entities/sortState';
import CompactStockCardComponent from '../../../components/customer/CompactStockCardComponent/compact-stock-card-component';
import SortUtils from '../../../components/customer/sorting_utl'
import arrowUp from '../../../assets/arrow-up-mono.png';
import arrowDown from '../../../assets/arrow-down-mono.png';



const HubPage: React.FC = () => {
 
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


  
  
  const [companies, setCompanies] = useState([] as CompanyPrediction[]);
  const [hasRun, setRun] = useState(false);
  const [renderList, setRender] = useState([] as JSX.Element[]);
  const[selected,setSelected] = useState({
    column: "Name",
    nextInReverse: true
  } as SortState)

  const handleSelected = (clicked_column: String) => {
    if(clicked_column === selected.column){
      const newSelected = {column: clicked_column, nextInReverse: !selected.nextInReverse} as SortState;
      setSelected(newSelected);
    } else {
      console.log("NOT MATCH")
      const newSelected = {column: clicked_column, nextInReverse: true} as SortState;
      setSelected(newSelected);
    }
  }
 
  const updateOrder = (comps: CompanyPrediction[]) => {
    const rList = comps.map(company => (<div className={styles.padding}><div > <CompactStockCardComponent companyInfo={company} /></div></div>))

    setRender(rList)    
  }

  const getCompanyData = async () => {
    try {
      const list_companies = await ModelService.getLatestPredictions(id?id:'');

      setCompanies(list_companies)

      const rList = list_companies.map(company => (<div className={styles.padding}><div > <CompactStockCardComponent companyInfo={company} /></div></div>))

      setRender(rList)      

      setRun(true)

    } catch (error) {
      console.error('Error while fetching predictions:', error);
    }
  };

  const chooseArrow = (name: string) => {
    if(name === selected.column){
      return !selected.nextInReverse? (<img src={arrowUp} className={styles.arrow}></img>):(<img src={arrowDown} className={styles.arrow}></img>) 
    }
    
  }


  if(!hasRun){
    getCompanyData();
  }
  


  

  return (
    <div className={styles.page}>
      <CustomerNavbarComponent userId={id} />
      <div className={styles.wrapper}>
        
        <Container className={styles.main_container}>
          <Col xs={12} sm={12} md={12} >
          <Row>
          <div className={styles.top_container}>
            <Col >
            <div className={styles.col_row}>
            <SortButton data={{sort_func: SortUtils.name_sort, list: companies, update_func: updateOrder, name: 'Name', callback: () => {handleSelected("Name")}, list_state: selected}}/>
            {chooseArrow('Name') }
            </div>
            </Col>
            <Col>
            <div className={styles.col_row}>
            <SortButton data={{sort_func: SortUtils.stock_sort, list: companies, update_func: updateOrder, name: 'Stock', callback: () => {handleSelected("Stock")}, list_state: selected}}/>
            {chooseArrow('Stock') }
            </div>
            </Col>
            <Col>
            <div className={styles.col_row}>
            <SortButton data={{sort_func: SortUtils.tweet_rate_sort, list: companies, update_func: updateOrder, name: 'Popularity', callback: () => {handleSelected("Popularity")}, list_state: selected}}/>
            {chooseArrow('Popularity') }
            </div>
            </Col>
            <Col>
            <div className={styles.col_row}>
            <SortButton data={{sort_func: SortUtils.sentiment_sort, list: companies, update_func: updateOrder, name: 'Sentiment', callback: () => {handleSelected("Sentiment")}, list_state: selected}}/>
            {chooseArrow('Sentiment') }
            </div>
            </Col>
            
          </div>
          </Row>
          <Row className={styles.main_container}>
          <Col xs={12} lg={12} md={12}>
            <div>
              <Col xs={12} sm={12} md={12} className={styles.render_list}>
                {renderList}
              </Col>
            </div>
          </Col>
        </Row>
        </Col>
        </Container>
        </div>
        
    </div>
  );
};

export default HubPage;
