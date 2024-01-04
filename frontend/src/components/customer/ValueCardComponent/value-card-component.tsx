import React, { useRef, useState } from 'react';
import { Col, Overlay, Row, Tooltip } from 'react-bootstrap';
import styles from './value-card-component.module.scss';  
import information from '../../../assets/information.png';

interface ValueCardProps {
  prediction: number;
}

const ValueCardComponent: React.FC<ValueCardProps> = (props) => {
  console.log(props.prediction);

  const [show, setShow] = useState(false);
  const target = useRef(null);

  const handleMouseEnter = () => {
    setShow(true);
  };

  const handleMouseLeave = () => {
    setShow(false);
  };


  const roundedPrediction = props.prediction !== undefined ? props.prediction.toFixed(4) : 'N/A';

  return (
    <Col xs={12} sm={12} md={12} className={styles.container}>
      <Row className={styles.title}>
        <Col xs={10} sm={10} md={10} className={styles.title__container}>
          <p>Latest Prediction Value</p>
        </Col>
        <Col xs={2} sm={2} md={2} onMouseEnter={handleMouseEnter} onMouseLeave={handleMouseLeave}>
          <img ref={target} src={information} alt="Information" className={styles.infoButton} />
          <Overlay target={target.current} show={show} placement="right">
            {(props) => (
              <Tooltip id='tooltip' {...props} className={styles.customTooltip}>
                <div>
                  <p>
                    The prediction value ranges from -1 to 1. A value of -1 indicates a more negative or bearish market
                    prediction, while a value of 1 suggests a more positive or bullish prediction.
                  </p>
                  <p>
                    -1 is considered the lowest prediction, and 1 is considered the highest prediction.
                  </p>
                </div>
              </Tooltip>
            )}
          </Overlay>
        </Col>
      </Row>
      <Row className={styles.main__container}>
        <Col xs={12} sm={12} md={12} className={styles.trend__container}>
          {roundedPrediction}
        </Col>
      </Row>
    </Col>
  );
};

export default ValueCardComponent;
