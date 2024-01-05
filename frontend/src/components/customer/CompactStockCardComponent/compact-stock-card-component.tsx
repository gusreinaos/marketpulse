//Author: Wojciech Pechmann

import { Col, Row, Container } from "react-bootstrap";
import { usePredictionContext } from "../../../contexts/predictionContext";
import { MarketTrendPredictionRequest } from "../../../domain/entities/marketTrendPrediction";
import styles from "./compact-stock-card-component.module.scss"
import {CompanyPrediction} from  '../../../domain/entities/companyPrediction'
import FavButton from "../FavButtonComponent/fav-button-component";
import arrowUpImage from '../../../assets/arrow_up_small.png';
import arrowDownImage from '../../../assets/arrow_down_small.png';
import arrowUpSmall from '../../../assets/arrow_up_small.png';
import arrowDownSmall from '../../../assets/arrow_down_small.png';
import neutral from '../../../assets/neutral.png';

const CompactStockCardComponent = ({ companyInfo }: { companyInfo: CompanyPrediction }) => {
  

  const removeTrailingZeros = (company : CompanyPrediction) => {
    
  }

  const evalSentiment = (sentiment: number) =>{
    if(sentiment>=1.33){
      if(sentiment>=1.66){
        return (<img src={arrowUpImage} className={styles.arrow}></img> )
      }
      return (<img src={arrowUpSmall} className={styles.arrow_small}></img> )
    } else if (sentiment<=0.66) {
      if(sentiment<=0.33){
        return (<img src={arrowDownImage} className={styles.arrow}></img> )
      }
      return (<img src={arrowDownSmall} className={styles.arrow_small}></img> )
    } else {
      return (<img src={neutral} className={styles.neutral}></img> )
    }
  }
  const evalMarket = (market: number) => {
    if(market>=1.33){
      if(market>=1.66){
        return (<img src={arrowUpImage} className={styles.arrow}></img> )
      }
      return (<img src={arrowUpSmall} className={styles.arrow_small}></img> )
    } else if (market<=0.66) {
      if(market<=0.33){
        return (<img src={arrowDownImage} className={styles.arrow}></img> )
      }
      return (<img src={arrowDownSmall} className={styles.arrow_small}></img> )
    } else {
      return (<img src={neutral} className={styles.neutral}></img> )
    }
  }

  return (
    <div className={styles.padding}>
    <div className={styles.cc}>

    <Container>
      
      <Row>
        <Col id={styles.title_container}>
          <p>{companyInfo.company_name}</p>
        </Col>
      </Row>
      
      <Row>
        <Col  className={styles.market_container}>
          <p>Market prediction: {evalMarket(companyInfo.prediction_value)} </p>
        </Col>
        <Col  className={styles.sentiment_container}>
          <p>Public sentiment: {evalSentiment(companyInfo.avg_sentiment)}</p>
        </Col>
        <Col  className={styles.sentiment_container}>
          <p>Stock price: {companyInfo.stock_val.toFixed(2)}</p>
        </Col>
      </Row>
    </Container>
      
    </div>
    </div>
  );
};
  
export default CompactStockCardComponent;
  