//Author: Oscar Reina, Michael Larsson
import { useContext, useEffect, useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import CustomerNavbarComponent from '../../../components/customer/CustomerNavBarComponent/customer-navbar-component';
import SearchBarComponent from '../../../components/customer/SearchBarComponent/search-bar-component';
import styles from './discover-page.module.scss'
import { AuthContext } from '../../../contexts/authContext';
import CompanyInfoComponent from '../../../components/customer/CompanyInfoComponent/company-info-component';
import CompanyService from '../../../services/companyService';

import rightArrow from '../../../assets/slide-right.png'
import leftArrow from '../../../assets/slide-left.png'


const DiscoverPage: React.FC = () => {
  const { customerId } = useParams();
  const navigate = useNavigate();

  const contextValue = useContext(AuthContext);
  const user = contextValue?.user;

  const [companyInfo, setCompanyInfo] = useState([{
    company_code: '',
    company_info: '',
    company_name: '',
    company_logo: ''
  }])

  const [leftSlideNum, setLeftSlideNum] = useState(0);
  const [rightSlideNum, setRightSlideNum] = useState(1);

  const [leftSlide, setLeftSlide] = useState(companyInfo[leftSlideNum])
  const [rightSlide, setRightSlide] = useState(companyInfo[rightSlideNum])

  useEffect(() => {
    if (!user) {
      navigate('/');
    }

    const handleCompanyInfo = async () => {
      try {
        const companyInfo = await CompanyService.getCompanyInfo('AAPL')
        setCompanyInfo(companyInfo)

        setLeftSlide(companyInfo[leftSlideNum]);
        setRightSlide(companyInfo[rightSlideNum]);
      } catch (error) {
        console.error('Error fetching company info:', error);
      }
    };

    handleCompanyInfo()
  }, [user, navigate, leftSlideNum, rightSlideNum]);

  const handleNextSlide = () => {
    setLeftSlideNum((prevSlide) => (prevSlide + 2) % 6);
    setRightSlideNum((prevSlide) => (prevSlide + 2) % 6);

    setLeftSlide(companyInfo[leftSlideNum]);
    setRightSlide(companyInfo[rightSlideNum]);
  };

  const handlePrevSlide = () => {
    setLeftSlideNum((prevSlide) =>
      prevSlide - 1 < 0 ? 6 - 2 : prevSlide - 2
    );
    
    setRightSlideNum((prevSlide) =>
      prevSlide - 2 < 0 ? 6 - 1 : prevSlide - 2
    );

    setLeftSlide(companyInfo[leftSlideNum]);
    setRightSlide(companyInfo[rightSlideNum]);
  };


  return (
    <div className={styles.page}>
      <CustomerNavbarComponent userId={customerId}/>
      <div className={styles.wrapper}>
        <div className={styles.page__container}>
          <div className={styles.page__title}>
            Discover the market trend of your favorite NASDAQ company!
          </div>
          <div className={styles.searchbar__container}>
            <SearchBarComponent customerId={String(customerId)} />
          </div>
          <div className={styles.company_info_title}>Favorite companies of our users!</div>
        </div>
        <div className={styles.company_info_container}>
            <div className={styles.slide}>
              <CompanyInfoComponent data={leftSlide} />
            </div>
            <div className={styles.slide}>
              <CompanyInfoComponent data={rightSlide} />
            </div>
          </div>
          <div className={styles.controls_container}>
            <button onClick={handlePrevSlide} className={styles.controls}><img src={leftArrow}></img></button>
            <button onClick={handleNextSlide} className={styles.controls}><img src={rightArrow}></img></button>
          </div>
      </div>
    </div>
  );
};

export default DiscoverPage;