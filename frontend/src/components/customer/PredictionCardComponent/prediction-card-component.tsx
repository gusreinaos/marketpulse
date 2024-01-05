import React from 'react';
import { Col, Row } from 'react-bootstrap';
import styles from './prediction-card-component.module.scss';
import arrowUpImage from '../../../assets/arrow_up.png';
import arrowDownImage from '../../../assets/arrow_down.png';
import arrowUpSmall from '../../../assets/arrow_up_small.png';
import arrowDownSmall from '../../../assets/arrow_down_small.png';
import neutral from '../../../assets/neutral.png'

const PredictionCardComponent = (props: any) => {

  const getTrendImage = (value: number) => {
    return value >= 0 ? arrowUpSmall : arrowDownSmall;
  };

  return (
    <Col xs={12} sm={12} md={12} className={styles.container}>
      <Row className={styles.title}>
        <Col xs={12} sm={12} md={12} className={styles.title_container}>
          <p>Predicted Market Trend</p>
        </Col>
      </Row>
      <Row className={styles.main_container}>
        {props.requestData.prediction ? (
          <Col xs={6} sm={6} md={6}>
            <div className={styles.trend_container}>
            {props.requestData.prediction === 0 ? (
              <>
                <img src={arrowDownImage} alt="Arrow Down" className={styles.arrow} />
                <div className={styles.trend_value_container}>
                  <p className={styles.trend_value}>Downtrend</p>
                </div>
              </>
            ) : props.requestData.prediction === 1 ? (
              <>
                <img src={neutral} alt="Neutral Arrow" className={styles.arrow} />
                <div className={styles.trend_value_container}>
                  <p className={styles.trend_value}>Neutral</p>
                </div>
              </>
            ) : (
              <>
                <img src={arrowUpImage} alt="Arrow Up" className={styles.arrow} />
                <div className={styles.trend_value_container}>
                  <p className={styles.trend_value}>Uptrend</p>
                </div>
              </>
            )}
            </div>
          </Col>
        ) : (
          <Col xs={12} sm={12} md={12} className={styles.error_container}>
            <p>Data could not be found 😞</p>
          </Col>
        )}
        {props.requestData.prediction && (
          <Col xs={6} sm={6} md={6}>
            <div className={styles.trend_information_container}>
              <div className={styles.public_sentiment}>
                <img src={arrowDownSmall} className={styles.arrow_small} />
                Public sentiment
              </div>
              {props.requestData.stockTrend !== undefined && (
                <Col xs={6} sm={6} md={6}>
                  <div className={styles.current_stock}>
                    <img src={getTrendImage(props.requestData.stockTrend)} className={styles.arrow_small} alt={props.requestData.stockTrend >= 0 ? 'Arrow Up' : 'Arrow Down'} />
                      Stock Closing
                  </div>
                </Col>
              )}
              {props.requestData.inflationTrend !== undefined && (
                <Col xs={6} sm={6} md={6}>
                  <div className={styles.current_stock}>
                    <img src={getTrendImage(props.inflationTrend)} className={styles.arrow_small} alt={props.inflationTrend >= 0 ? 'Arrow Up' : 'Arrow Down'} />
                      Inflation Rate
                  </div>
                </Col>
              )}
            </div>
          </Col>
        )}
      </Row>
    </Col>
    );
  };

export default PredictionCardComponent;
