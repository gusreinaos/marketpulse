//Author: Michael Larsson
import React, { useEffect, useRef, useState } from 'react';
import { Button, Col, Overlay, Row, Tooltip } from 'react-bootstrap';
import { useLocation, useNavigate, useParams } from 'react-router-dom';
import styles from './value-card-component.module.scss';  
import information from '../../../assets/information.png';
import refreshButton from '../../../assets/refresh-icon.png'
import ModelService from '../../../services/modelService';

interface ValueCardProps {
  sentiment: number;
}

const ValueCardComponent: React.FC<ValueCardProps> = (props) => {
  const location = useLocation();
  const searchParams = new URLSearchParams(location.search);
  const companyName = searchParams.get('name');
  const timestamp = Date.now()
  const [sentiment, setSentiment] = useState(props.sentiment);
  const [loading, setLoading] = useState(false);

  console.log(props);

  useEffect(() => {
    setSentiment(props.sentiment);
  }, [props.sentiment]);

  const refreshPrediction = async () => {
    try {
      setLoading(true)
      const newPrediction = await ModelService.getRefreshedPredictions(companyName!, timestamp)
      setSentiment(newPrediction.avg_sentiment)
    } catch (error) {
      console.error('Error fetching new prediction', error);
    } finally {
      setLoading(false)
    }
  };

  const [show, setShow] = useState(false);
  const target = useRef(null);

  const handleMouseEnter = () => {
    setShow(true);
  };

  const handleMouseLeave = () => {
    setShow(false);
  };


  return (
    <Col xs={12} sm={12} md={12} className={styles.container}>
      <Row className={styles.title}>
        <Col xs={10} sm={10} md={10} className={styles.title__container}>
          <p>Latest Sentiment Value</p>
        </Col>
        <Col xs={2} sm={2} md={2} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
          <img ref={target} src={information} alt="Information" className={styles.infoButton} />
          <Overlay target={target.current} show={show} placement="right">
            {(props) => (
              <Tooltip id='tooltip' {...props} className={styles.customTooltip}>
                <div>
                  <p>
                    The sentiment value ranges from -1 to 1. A value of -1 indicates a more negative outlook, while a value of 1 suggests a more positive outlook.
                  </p>
                  <p>
                    -1 is considered the lowest sentiment, and 1 is considered the highest sentiment.
                  </p>
                </div>
              </Tooltip>
            )}
          </Overlay>
        </Col>
      </Row>
      <Row className={styles.main__container}>
        <Col xs ={12} sm={12} md={3} className={styles.trend__container}>
          <button onClick={refreshPrediction} className={styles.refreshButton}><img src={refreshButton}></img></button>
        </Col>
        
        <Col xs={12} sm={12} md={9} className={sentiment >  0 ? styles.greenText : styles.redText}>
          {loading ? 'Loading...' : sentiment !== undefined ? sentiment.toFixed(4) : 'N/A'}
        </Col>
      </Row>
    </Col>
  );
};

export default ValueCardComponent;
