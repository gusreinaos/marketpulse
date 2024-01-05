//Author: Michael Larsson, Oscar Reina

import { useEffect, useRef, useState } from "react";
import { Col, Row } from "react-bootstrap";
import { MarketTrendPredictionRequest } from "../../../domain/entities/marketTrendPrediction";
import styles from "./sentiment-card-component.module.scss"

const SentimentCardComponent = ({ requestData }: { requestData: MarketTrendPredictionRequest }) => {
    return (
      <Col xs={12} sm={12} md={12} className={styles.container}>
        <Row className={styles.title}>
          <Col xs={12} sm={12} md={12} className={styles.title_container}>
            <p>Current sentiment</p>
          </Col>
        </Row>
        <Row className={styles.main_container}>
          <Col xs={12} sm={12} md={12} className={styles.trend_container}>
            <div id="progress "className={styles.progress}>
              <div id="barOverflow" className={styles.barOverflow}>
                <div id="bar" className={styles.bar}></div>
              </div>
              <span>60</span>%
            </div>
          </Col>
        </Row>
        
      </Col>
    );
  };
  
  export default SentimentCardComponent;
  