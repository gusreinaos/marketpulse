//Author: Oscar Reina
import React, { useContext, useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import styles from './search-bar-component.module.scss';
import { MarketTrendPredictionRequest } from '../../../domain/entities/marketTrendPrediction';

import discoverImage from '../../../assets/discover.png'
import { AuthContext } from '../../../contexts/authContext';

interface SearchBarProps {
  customerId: string
}

const SearchBarComponent: React.FC<SearchBarProps> = ({customerId}) => {
  const [searchTerm, setSearchTerm] = useState<string>('');
  const navigate = useNavigate();

  const contextValue = useContext(AuthContext);
  const user = contextValue?.user

  console.log("user", user)

  useEffect(() => {
    if (!user) {
      navigate('/'); 
    }
  }, [contextValue?.user]);

  const handleSearchChange = (event: React.ChangeEvent<HTMLInputElement>) => {
    setSearchTerm(event.target.value);
  };

  const handleSearchSubmit = async (event: React.FormEvent) => {
    
    event.preventDefault();

    if (searchTerm.trim() === '') {
      console.log('Search term is empty. Please enter a valid search term.');
      return;
    }
    
    const modelRequestData: MarketTrendPredictionRequest = {
      requestTimeStamp: new Date(),
      requestCompany: searchTerm,
    }
    setSearchTerm('');
    navigate(`/customers/${customerId}/companies?name=${searchTerm}`);
    
  };

  return (
    <div className={styles.searchBar}>
      <form className={styles.form} onSubmit={handleSearchSubmit}>
        <input
          className={styles.input}
          type="text"
          placeholder="Search..."
          value={searchTerm}
          onChange={handleSearchChange}
        />
        <button className={styles.button} type="submit">
          <img className={styles.img} src={discoverImage} alt="Discover icon" />
        </button>
      </form>
    </div>
  );
};

export default SearchBarComponent;
