//Author: Michael Larsson

import styles from './company-info-component.module.scss'
import { Col, Row } from 'react-bootstrap';

interface CompanyInfoProp{
  data: {
    company_name: string,
    company_info: string,
    company_code: string,
    company_logo: string
  }
}


const CompanyInfoComponent: React.FC<CompanyInfoProp> = ({data}) => {
  if (!data) {
    return <p>Loading...</p>;
  }

  return (
    <div className={styles.companyInfoContainer}>
      <Row className={styles.rowContainer}>
        <Col className={styles.left_container} sm={6}>
          <img src={data.company_logo} className={styles.company_logo} alt="Company Logo" />
        </Col>
        <Col className={styles.right_container} sm={6}>
          <p className={styles.text_title}>Description</p>
          <p className={styles.text}>{data.company_info}</p>
        </Col>
      </Row>
    </div>
  );
};

export default CompanyInfoComponent;
